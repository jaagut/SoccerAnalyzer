import pandas as pd

from socceranalyzer.utils.logger import Logger
from socceranalyzer.common.enums.hl_kid import HLKid


class FilterPlayer():
    def __init__(self, df: pd.DataFrame, category, side: str, player_number: int, include_time: bool = False):
        """Filter the dataframe to only contain the given player

        :param df: Dataframe to filter
        :type df: pd.DataFrame
        :param category: Category of the data
        :type category: _type_
        :param side: Side/Team of the player
        :type side: str
        :param player_number: Number of the player
        :type player_number: int
        :param include_time: Whether to include the time column, defaults to False
        :type include_time: bool, optional
        :raises NotImplementedError: Category not implemented
        """
        self.df = df
        self.category = category
        self.side = self._validate_side(side)
        self.player_number = self._validate_player_number(player_number)
        self.include_time = include_time

        self.player_prefix = None
        if self.category is HLKid:
            team = "team1" if side == "l" else "team2"
            self.player_prefix = f"teams.{team}.player{player_number}"
        else:
            raise NotImplementedError

    def _validate_side(self, side):
        if side not in ['l', 'r']:
            raise ValueError(f"Side must be 'l' or 'r', not {side}")
        return side

    def _validate_player_number(self, player_number):
        min_player_number = 1
        max_player_number = 11
        if self.category is HLKid:
            min_player_number = 1
            max_player_number = 4
        if player_number not in range(min_player_number, max_player_number + 1):
            raise ValueError(f"Player number must be between {min_player_number} and {max_player_number}, not {player_number}")
        return player_number

    def filter(self):
        """Filter the dataframe to only contain the player of interest"""
        # Return dataframe with all columns prefixed with the player
        if self.category is HLKid and self.player_prefix is not None:
            regex = f"^{self.player_prefix}"

            if self.include_time:
                regex += "|^time"

            return self.df.filter(regex=regex)
        else:
            raise NotImplementedError


class FilterPlayerNotPenalized(FilterPlayer):
    def __init__(self, df: pd.DataFrame, category, side: str, player_number: int, include_time: bool = False):
        super().__init__(df, category, side, player_number, include_time)

    def filter(self):
        """Filter the dataframe to only contain the player of interest and remove penalized cycles"""
        df = super().filter()
        df = df[df[f'{self.player_prefix}.robot_info.secs_till_unpenalized'] <= 0]
        return df
