from time import time

import pandas as pd

from socceranalyzer.common.analysis.speed import Speed
from socceranalyzer.common.chore.abstract_factory import AbstractFactory
from socceranalyzer.common.basic.match import Match
from socceranalyzer.common.collections.collections import EvaluatorCollection
from socceranalyzer.common.enums.sim2d import SIM2D
from socceranalyzer.common.enums.ssl import SSL
from socceranalyzer.common.enums.vss import VSS
from socceranalyzer.common.enums.hl_kid import HLKid
from socceranalyzer.common.analysis.ball_possession import BallPossession
from socceranalyzer.common.analysis.foul_charge import FoulCharge
from socceranalyzer.common.analysis.playmodes import Playmodes
from socceranalyzer.common.analysis.penalty import Penalty
from socceranalyzer.common.analysis.object_history import ObjectHistory
from socceranalyzer.common.analysis.corners_occurrencies import CornersOcurrencies
from socceranalyzer.common.analysis.passing_accuracy import PassingAccuracy
from socceranalyzer.common.analysis.intercept_counter import InterceptCounter
from socceranalyzer.common.dataframe.filter_self_localization import FilterSelfLocalizationCovariance, FilterBallCovariance
from socceranalyzer.agent2D.analysis.tester_free_kick import TesterFK
from socceranalyzer.common.analysis.time_after_events import TimeAfterEvents
from socceranalyzer.common.analysis.stamina import Stamina
from socceranalyzer.common.analysis.shooting import Shooting
from socceranalyzer.common.analysis.heatmap import Heatmap
from socceranalyzer.common.evaluators.passing import Passing
from socceranalyzer.common.analysis.find_goals import FindGoals
from socceranalyzer.common.analysis.goalkeeper import GoalkeeperAnalysis
from socceranalyzer.common.analysis.base_footprint import BaseFootprint
from socceranalyzer.utils.run_configuration import RunConfiguration
from socceranalyzer.utils.logger import Logger

class MatchAnalyzer(AbstractFactory):
    """
        ==== Add new analysis in this class ====
        - A class that represents a implementation of AbstractFactory. 
        - Acts as a endpoint to connect all created analysis in the framework.
        - Creates analysis objects, run them and then provide secure access to it's computed values.
        - At instantiation, it has no analysis. At runtime, generates analysis set in self._run_analysis().
        
        MatchAnalyzer(math: Match)

        Attributes
        ----------
            public through @properties:
                match: Match
                    Current match being analyzed. Same Match given as parameter.
                ball_possession: BallPossession
                    Object containing ball possession analysis
                tester_free_kick: TesterFK
                    Object containing free kick testing analysis
                foul_charge: FoulCharge
                    Object containing foul occurrences analysis
                penalty: Penalty
                    Object containing penalties analysis
                stamina: Stamina
                    Object containing stamina analysis
                corners: Corners
                    Object containing corners analysis
                playmodes: Playmodes
                    Object containing playmode analysis
                shooting: Shooting
                    Object containing shoots analysis
                category: Enum
                    Returns the Enum of the match category
                analysis_dict: dict
                    Returns a dictionary object with all current analysis and it's values.
            
        Methods
        -------
            public:    
                winner: str
                    String with the name of the game winner
                loser: str
                    String with the nae of the game loser
                final_score: None
                    Prints the result of the game
                available: None
                    Prints the current analysis being done (hardcoded)
                collect_results:
                    Returns a dictionary with built-in type values for usage
                
            private:
                _run_analysis: None
                    Creates analysis classes instances and run them.
                _generate_evaluators: None
                    Generates implemented evaluators



    """
    def __init__(self, match: Match = None, debug: bool = False, run_config: RunConfiguration = None):
        self._DEBUG = debug
        self.__match = match
        self.__cat = match.category
        self.__run_configuration: RunConfiguration = run_config
        self.__evaluators: EvaluatorCollection = None

        try:
            if self.__cat is None:
                raise ValueError('MatchAnalyzer requires a Category as argument and none was given')
        except ValueError as err:
            Logger.error("Match analyzer failed: " + err.args[0])
        else:
            Logger.info(f"Started analyzing.")
            begin: float = time()
            self._run_analysis()
            end: float = time()
            Logger.info(f'Ran all analysis in {end - begin} seconds.')

    @property
    def match(self):
        return self.__match

    @property
    def config(self):
        return self.__run_configuration

    @property
    def category(self):
        return self.__cat

    @property
    def field(self):
        return self.__field
    
    @property
    def ball(self):
        return self.__ball
    
    @property
    def left_team(self):
        return self.__left_team

    @property
    def right_team(self):
        return self.__right_team

    @property
    def left_players(self):
        return self.__left_players
    
    @property
    def right_players(self):
        return self.__right_players

    @property
    def evaluators(self):
        return self.__evaluators.evaluators

    @property
    def ball_possession(self):
        return self.__ball_possession
    
    @property
    def intercept_counter(self):
        return self.__intercept_counter

    @property
    def tester_free_kick(self):
        return self.__tester_free_kick

    @property
    def foul_charge(self):
        return self.__foul_charge

    @property
    def penalty(self):
        return self.__penalty

    @property
    def stamina(self):
        return self.__stamina

    @property
    def corners(self):
        return self.__corners_occurrencies

    @property
    def passing_accuracy(self):
        return self.__passing_accuracy

    @property
    def playmodes(self):
        return self._playmodes

    @property
    def shooting(self):
        return self.__shooting

    @property
    def heatmap(self):
        return self.__heatmap

    @property
    def find_goals(self):
        return self.__find_goals

    @property
    def goalkeeper(self):
        return self.__goalkeeper

    @property
    def ball_history(self):
        return self._ball_history

    @property
    def analysis_dict(self):
        raise NotImplementedError
        # return self.__analysis_dict

    @property
    def ball_holder(self):
        raise NotImplementedError
        # return BallHolder(self.match.dataframe, self.match.category)

    def winner(self) -> str:
        """
        Returns the name of the winning team.
        
                Returns:
                        winning_team (str): Name of the winning team.
        """
        return self.__match.winning_team

    def loser(self) -> str:
        """
        Returns the name of the losing team.
        
                Returns:
                        losing_team (str): Name of the losing team.
        """
        return self.__match.losing_team

    def final_score(self):
        """
        Shows the final score.
        """
        Logger.data(f'{self.__match.team_left_name} {self.__match.score_left} x {self.__match.score_right} {self.__match.team_right_name}')

    def _run_analysis(self):
        if self.__cat is SIM2D:
            if self.config.ball_possession:
                setattr(self, "__ball_possession", None)
                self.__ball_possession = BallPossession(self.__match.dataframe, self.category, self._DEBUG)
            
            if self.config.tester_free_kick:
                setattr(self, "__tester_free_kick", None)
                self.__tester_free_kick = TesterFK(self.__match.dataframe, self.category, self._DEBUG)

            if self.config.foul_charge:
                setattr(self, "__foul_charge", None)
                self.__foul_charge = FoulCharge(self.__match.dataframe, self.category, self._DEBUG)

            if self.config.penalty:
                setattr(self, "__penalty", None)
                self.__penalty = Penalty(self.__match.dataframe, self.category, self._DEBUG)

            if self.config.playmodes:
                setattr(self, "__playmodes", None)
                self._playmodes = Playmodes(self.__match.dataframe, self.category, self._DEBUG)

            if self.config.corners_occurrencies:
                setattr(self, "__corners_occurrencies", None)
                self.__corners_occurrencies = CornersOcurrencies(self.__match.dataframe, self.category, self._DEBUG)

            if self.config.intercept_counter or self.config.passing_accuracy:
                passing = Passing(self.__match.dataframe, self.category, self._DEBUG)
                setattr(self, "__intercept_counter", None)
                self.__intercept_counter = InterceptCounter(self.__match, passing, self._DEBUG)

                setattr(self, "__passing_accuracy", None)
                self.__passing_accuracy = PassingAccuracy(self.__match.dataframe, self.category, passing, self._DEBUG)

            if self.config.time_after_events:
                setattr(self, "__time_after_events", None)
                self.__time_after_events = TimeAfterEvents(self.__match.dataframe, self.category,
                                                        self.__corners_occurrencies.results(),
                                                        self.__foul_charge.results(tuple=True),
                                                        self._DEBUG)

            if self.config.ball_history:
                setattr(self, "__ball_history", None)
                #self._ball_history = ObjectHistory(self.__match.dataframe, self.category, self._DEBUG)

            if self.config.stamina:
                setattr(self, "__stamina", None)
                self.__stamina = Stamina(self.__match.dataframe, self.category, self._DEBUG)

            if self.config.shooting:
                setattr(self, "__shooting", None)
                self.__shooting = Shooting(self.__match.dataframe, self.category, self._DEBUG)

            if self.config.heatmap:
                setattr(self, "__heatmap", None)
                self.__heatmap = Heatmap(self.__match.dataframe, self.category, self._DEBUG)
            
            if self.config.speed:
                setattr(self, "__speed", None)
                self__speed = Speed(self.__match.dataframe, self.category, 9, "left", self._DEBUG)

            if self.config.find_goals:
                setattr(self, "__find_goals", None)
                self.__find_goals = FindGoals(self.__match.dataframe, self.category, self._DEBUG)

            if self.config.goalkeeper:
                setattr(self, "__goalkeeper", None)
                self.__goalkeeper = GoalkeeperAnalysis(self.__match.dataframe, self.category, self._DEBUG)

            #setattr(self, "__time_after_corner", None)
            #self.__time_after_corner = TimeAfterCorner(self.__match.dataframe, self.category)

        elif self.__cat is SSL:
            pass
            # setattr(self, "__heatmap", None)
            # self.__heatmap = Heatmap(self.__match.dataframe, self.category)

        elif self.__cat is VSS:
            raise NotImplementedError
            # add VSS analysis
        
        elif self.__cat is HLKid:
            df = self.__match.dataframe.copy()
            # Single analysis
            self._playmodes = Playmodes(df, self.category, self._DEBUG)
            self._ball_history = ObjectHistory(df, self.category, self._DEBUG, "ball.frame.pose")

            # Analysis for each player
            for team in [('l', 1), ('r', 2)]:
                for player in range(1, 5):
                    df = BaseFootprint(df, self.category, self._DEBUG, team[1], player).results()

            self.left_player_1_history = ObjectHistory(df, self.category, self._DEBUG, "teams.team1.player1.base_footprint")
            self.left_player_2_history = ObjectHistory(df, self.category, self._DEBUG, "teams.team1.player2.base_footprint")
            self.left_player_3_history = ObjectHistory(df, self.category, self._DEBUG, "teams.team1.player3.base_footprint")
            self.left_player_4_history = ObjectHistory(df, self.category, self._DEBUG, "teams.team1.player4.base_footprint")
            self.right_player_1_history = ObjectHistory(df, self.category, self._DEBUG, "teams.team2.player1.base_footprint")
            self.right_player_2_history = ObjectHistory(df, self.category, self._DEBUG, "teams.team2.player2.base_footprint")
            self.right_player_3_history = ObjectHistory(df, self.category, self._DEBUG, "teams.team2.player3.base_footprint")
            self.right_player_4_history = ObjectHistory(df, self.category, self._DEBUG, "teams.team2.player4.base_footprint")

            speed_df = df
            self.left_player_1_speed = Speed(speed_df, self.category, 1, "l", self._DEBUG)
            self.left_player_2_speed = Speed(speed_df, self.category, 2, "l", self._DEBUG)
            self.left_player_3_speed = Speed(speed_df, self.category, 3, "l", self._DEBUG)
            self.left_player_4_speed = Speed(speed_df, self.category, 4, "l", self._DEBUG)
            self.right_player_1_speed = Speed(speed_df, self.category, 1, "r", self._DEBUG)
            self.right_player_2_speed = Speed(speed_df, self.category, 2, "r", self._DEBUG)
            self.right_player_3_speed = Speed(speed_df, self.category, 3, "r", self._DEBUG)
            self.right_player_4_speed = Speed(speed_df, self.category, 4, "r", self._DEBUG)

            # Self-localization
            self.left_player_1_localization = ObjectHistory(df, self.category, self._DEBUG, "teams.team1.player1.team_comm.self_localization.pose", filter=FilterSelfLocalizationCovariance)
            self.left_player_2_localization = ObjectHistory(df, self.category, self._DEBUG, "teams.team1.player2.team_comm.self_localization.pose", filter=FilterSelfLocalizationCovariance)
            self.left_player_3_localization = ObjectHistory(df, self.category, self._DEBUG, "teams.team1.player3.team_comm.self_localization.pose", filter=FilterSelfLocalizationCovariance)
            self.left_player_4_localization = ObjectHistory(df, self.category, self._DEBUG, "teams.team1.player4.team_comm.self_localization.pose", filter=FilterSelfLocalizationCovariance)
            self.right_player_1_localization = ObjectHistory(df, self.category, self._DEBUG, "teams.team2.player1.team_comm.self_localization.pose", mirror=True, filter=FilterSelfLocalizationCovariance)
            self.right_player_2_localization = ObjectHistory(df, self.category, self._DEBUG, "teams.team2.player2.team_comm.self_localization.pose", mirror=True, filter=FilterSelfLocalizationCovariance)
            self.right_player_3_localization = ObjectHistory(df, self.category, self._DEBUG, "teams.team2.player3.team_comm.self_localization.pose", mirror=True, filter=FilterSelfLocalizationCovariance)
            self.right_player_4_localization = ObjectHistory(df, self.category, self._DEBUG, "teams.team2.player4.team_comm.self_localization.pose", mirror=True, filter=FilterSelfLocalizationCovariance)

            # Ball localization
            self.left_player_1_ball_localization = ObjectHistory(df, self.category, self._DEBUG, "teams.team1.player1.team_comm.ball")
            self.left_player_2_ball_localization = ObjectHistory(df, self.category, self._DEBUG, "teams.team1.player2.team_comm.ball")
            self.left_player_3_ball_localization = ObjectHistory(df, self.category, self._DEBUG, "teams.team1.player3.team_comm.ball")
            self.left_player_4_ball_localization = ObjectHistory(df, self.category, self._DEBUG, "teams.team1.player4.team_comm.ball")
            self.right_player_1_ball_localization = ObjectHistory(df, self.category, self._DEBUG, "teams.team2.player1.team_comm.ball", mirror=True)
            self.right_player_2_ball_localization = ObjectHistory(df, self.category, self._DEBUG, "teams.team2.player2.team_comm.ball", mirror=True)
            self.right_player_3_ball_localization = ObjectHistory(df, self.category, self._DEBUG, "teams.team2.player3.team_comm.ball", mirror=True)
            self.right_player_4_ball_localization = ObjectHistory(df, self.category, self._DEBUG, "teams.team2.player4.team_comm.ball", mirror=True)

        else:
            raise ValueError("Invalid category.")


    def collect_results(self):
        raise NotImplementedError
