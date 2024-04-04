from enum import Enum

import numpy as np
import pandas as pd
import transforms3d

from socceranalyzer.common.analysis.abstract_analysis import AbstractAnalysis
from socceranalyzer.utils.logger import Logger


class BaseFootprint(AbstractAnalysis):
    """Calculates the base footprint of the robot based on the sole and base_link frames according to REP 120:
    https://www.ros.org/reps/rep-0120.html
    
    The base_footprint is the representation of the robot position on the floor.
    The floor is usually the level where the supporting leg rests,
    i.e. z = min(l_sole_z, r_sole_z) where l_sole_z and r_sole_z are the left and right sole height respectively.
    The translation component of the frame should be the barycenter of the feet projections on the floor.
    With respect to the odom frame, the roll and pitch angles should be zero and
    the yaw angle should correspond to the base_link yaw angle.
    """
    def __init__(self, dataframe, category: Enum, debug, team_number: int, player_id: int):
        self.df = dataframe
        self.__category = category
        self.__team_number = team_number
        self.__player_id = player_id
        try:
            self._analyze()
        except Exception:
            import traceback
            Logger.error(f"BaseFootprint failed: {traceback.format_exc()}")
            if debug:
                raise
        else:
            Logger.success(f"BaseFootprint for team {team_number}, player {player_id} has results.")
            
    @property
    def dataframe(self):
        return self.df

    @property
    def category(self):
        return self.__category

    def _analyze(self):
        player_prefix = f'teams.team{self.__team_number}.player{self.__player_id}'
        base_link_prefix = f'{player_prefix}.base_link'
        l_sole_prefix = f'{player_prefix}.l_sole'
        r_sole_prefix = f'{player_prefix}.r_sole'
        base_footprint_prefix = f'{player_prefix}.base_footprint'

        def get_base_footprint(
                df: pd.DataFrame,
                base_link_prefix: str,
                l_sole_prefix: str,
                r_sole_prefix: str,
                base_footprint_prefix: str,
                ) -> pd.DataFrame:
            # Position is in the center between the two feet
            df[f'{base_footprint_prefix}.position.x'] = (df[f'{l_sole_prefix}.position.x'] + df[f'{r_sole_prefix}.position.x']) / 2
            df[f'{base_footprint_prefix}.position.y'] = (df[f'{l_sole_prefix}.position.y'] + df[f'{r_sole_prefix}.position.y']) / 2
            df[f'{base_footprint_prefix}.position.z'] = (df[f'{l_sole_prefix}.position.z'] + df[f'{r_sole_prefix}.position.z']) / 2

            # Rotation:
            quat = np.zeros((len(df), 4))

            for i in range(len(df)):
                # Convert base_link quaternion to Euler angles, we only need the yaw angle
                _, _, yaw = transforms3d.euler.quat2euler((
                    df[f'{base_link_prefix}.rotation.w'][i],
                    df[f'{base_link_prefix}.rotation.x'][i],
                    df[f'{base_link_prefix}.rotation.y'][i],
                    df[f'{base_link_prefix}.rotation.z'][i],
                ))

                # Convert back to quaternion, roll and pitch are 0
                quat[i] = transforms3d.euler.euler2quat(0, 0, yaw)

            df[f'{base_footprint_prefix}.rotation.w'] = quat[:, 0]
            df[f'{base_footprint_prefix}.rotation.x'] = quat[:, 1]
            df[f'{base_footprint_prefix}.rotation.y'] = quat[:, 2]
            df[f'{base_footprint_prefix}.rotation.z'] = quat[:, 3]
            return df

        self.df = get_base_footprint(self.df, base_link_prefix, l_sole_prefix, r_sole_prefix, base_footprint_prefix)

    def describe(self):
        Logger.data("No description available")

    def results(self) -> pd.DataFrame:
        return self.df

    def serialize(self):
        raise NotImplementedError
