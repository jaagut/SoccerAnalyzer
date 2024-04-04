from typing import List

import pandas as pd
import numpy as np

from socceranalyzer.common.analysis.abstract_analysis import AbstractAnalysis
from socceranalyzer.common.enums.sim2d import SIM2D
from socceranalyzer.common.enums.hl_kid import HLKid
from socceranalyzer.common.dataframe.filter_player import FilterPlayerNotPenalized
from socceranalyzer.utils.logger import Logger


class Speed(AbstractAnalysis):
    def __init__(self, dataframe: pd.DataFrame, category, player_number: int, side: str, debug, window_size: int = 16, filter_outliers: bool = True) -> None:
        self.__dataframe = dataframe
        self.__category = category
        self.__player_speed: List | np.ndarray = []
        self.__debug = debug

        try:
            self._analyze(player_number, side, window_size, filter_outliers)
        except Exception as err:
            Logger.error(f"Speed failed: {err.args[0]}")
            if debug:
                raise
        else:
            Logger.success("Speed has results.")

    @property
    def category(self):
        return self.__category

    @property
    def dataframe(self):
        return self.__dataframe

    def results(self):
        return self.__player_speed

    def describe(self):
        raise NotImplementedError

    def serialize(self):
        return NotImplementedError

    def _analyze(self, player_number: int, side: str, window_size: int = 1, filter_outliers: bool = True):

        player_number, side = self.__handle_values(player_number, side)

        if self.__category is SIM2D:
            vx = np.array(self.__dataframe[f'player_{side}{player_number}_vx'].tolist())
            vy = np.array(self.__dataframe[f'player_{side}{player_number}_vy'].tolist())

            velocity_vector = [[x,y] for x, y in zip(vx,vy)]

            self.__player_speed = self._calculate_speed(velocity_vector)
        elif self.__category is HLKid:
            # Filter the DataFrame to only include the player when not penalized
            df = FilterPlayerNotPenalized(self.__dataframe, self.__category, side, player_number, include_time=True).filter()
            self.__player_speed = self._analyze_sliding_window_speed(df, player_number, side, filter_outliers, window_size)
        else:
            raise NotImplementedError

    def _get_direct_speed(self, df: pd.DataFrame, player_number: int, side: str, filter_outliers: bool = True):
        """This calculates speed from differences between each step (no sliding window)"""
        team = 'team1' if side == 'l' else 'team2'
        position_prefix = f'teams.{team}.player{player_number}.base_footprint.position.'

        # Calculate position differences for each axis over time
        # Shift the DataFrame by one row to get the previous positions
        prev_df = df[[position_prefix + 'x', position_prefix + 'y', position_prefix + 'z', 'time']].shift(1)

        # Calculate the time differences
        time_diff = df['time'] - prev_df['time']

        # Calculate the differences in x, y, and z positions
        delta_x = df[position_prefix + 'x'] - prev_df[position_prefix + 'x']
        delta_y = df[position_prefix + 'y'] - prev_df[position_prefix + 'y']
        # delta_z = df[position_prefix + 'z'] - prev_df[position_prefix + 'z']

        # Calculate velocities
        velocity_x = delta_x / time_diff
        velocity_y = delta_y / time_diff
        # velocity_z = delta_z / time_diff

        # Set velocities to NaN where the time difference is larger than 0.064
        velocity_x[time_diff > 0.064] = None
        velocity_y[time_diff > 0.064] = None
        # velocity_z[time_diff > 0.064] = None

        # Calculate the speed from the velocities and remove the NaN values
        speeds_including_NaN = np.array(self._calculate_speed([[x, y] for x, y in zip(velocity_x, velocity_y)]))
        non_nan_indices = np.where(~np.isnan(speeds_including_NaN))
        speeds = speeds_including_NaN[non_nan_indices]

        # Filter outliers
        if filter_outliers:
            # Calculate the mean and standard deviation of the speeds
            mean = np.mean(speeds)
            std = np.std(speeds)

            # Remove all speeds that are more than 3 standard deviations from the mean
            speeds = speeds[np.abs(speeds - mean) <= 3 * std]
        return speeds

    def _analyze_sliding_window_speed(self, df: pd.DataFrame, player_number: int, side: str, filter_outliers: bool = True, window_size: int = 1):
        """This calculates speed from sliding windows of size window_size over the direct speed data"""
        def shift_ndarray(xs: np.ndarray, n: int):
            """Shifts the given ndarray by n places to the right (positive n) or left (negative n)
            Inspired by: https://stackoverflow.com/questions/30399534/shift-elements-in-a-numpy-array
            """
            if n == 0:
                return xs
            elif n >= 0:
                return np.concatenate((np.full(n, np.nan), xs[:-n]))
            else:
                return np.concatenate((xs[-n:], np.full(-n, np.nan)))

        direct_speed = self._get_direct_speed(df, player_number, side, filter_outliers)

        # Add shifted direct speeds together and divide by the window size to average them
        accumulated_speeds = direct_speed.copy()
        for i in range(1, window_size):
            accumulated_speeds += shift_ndarray(direct_speed.copy(), -i)
        speed = accumulated_speeds / window_size

        # Remove the NaN values
        speed = speed[~np.isnan(speed)]
        return speed

    def _calculate_speed(self, velocity_over_time):
        velocity_over_time = np.array(velocity_over_time)
        velocity_scalar = [np.linalg.norm(coordinate) for coordinate in velocity_over_time]
        return velocity_scalar

    def __handle_values(self, player_number, side):
        min_player_number = 0
        max_player_number = 11
        if self.__category is HLKid:
            min_player_number = 1
            max_player_number = 4

        if side[0] != 'l': 
            if side[0] != 'r':
                raise ValueError(f'Value: {side} is not accepted to socceranalyzer.speed.side')
        
        side = side[0]

        if not(min_player_number <= player_number <= max_player_number):
            raise ValueError(f'Value: {player_number} is not accepted to socceranalyzer.speed.player_number')
            
        return player_number, side
