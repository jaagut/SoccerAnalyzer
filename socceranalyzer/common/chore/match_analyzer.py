from time import time

from socceranalyzer.common.chore.abstract_factory import AbstractFactory
from socceranalyzer.common.chore.builder import Builder

from socceranalyzer.common.basic.match import Match
from socceranalyzer.common.collections.collections import EvaluatorCollection
from socceranalyzer.common.enums.sim2d import SIM2D
from socceranalyzer.common.enums.ssl import SSL
from socceranalyzer.common.enums.vss import VSS
from socceranalyzer.common.analysis.ball_possession import BallPossession
from socceranalyzer.common.analysis.foul_charge import FoulCharge
from socceranalyzer.common.analysis.playmodes import Playmodes
from socceranalyzer.common.analysis.penalty import Penalty
from socceranalyzer.common.analysis.ball_history import BallHistory
from socceranalyzer.common.analysis.corners_occurrencies import CornersOcurrencies
from socceranalyzer.common.analysis.intercept_counter import InterceptCounter
from socceranalyzer.agent2D.analysis.tester_free_kick import TesterFK
from socceranalyzer.common.analysis.time_after_events import TimeAfterEvents
from socceranalyzer.common.analysis.stamina import Stamina
from socceranalyzer.common.analysis.shooting import Shooting
from socceranalyzer.common.analysis.heatmap import Heatmap


class MatchAnalyzer(AbstractFactory):
    """
        ==== Add new analysis in this class ====
        - A class that represents a implementation of AbstractFactory. 
        - Acts as a endpoint to connect all created analysis in the framework.
        - Creates analysis objects, run them and then provide secure acess to it's computed values.
        - At instantiation, it has no analysis. At runtime, generates analysis setted in self._run_analysis().
        
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
    def __init__(self, match: Match = None):
        self.__match = match
        self.__cat = match.category
        self.__analysis_dict: dict[str, None] = {}
        self.__evaluators: EvaluatorCollection = None

        try:
            if self.__cat is None:
                raise ValueError('MatchAnalyzer requires a Category as argument and none was given')
        except ValueError as err:
            print(err)
            raise
        else:
            begin: float = time()
            #self._generate_evaluators()
            self._run_analysis()
            end: float = time()

            print(f'socceranalyzer: Ran all analysis in {end - begin} seconds.')

    @property
    def match(self):
        return self.__match

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
    def playmodes(self):
        return self.__playmodes

    @property
    def shooting(self):
        return self.__shooting

    @property
    def heatmap(self):
        return self.__heatmap

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
        print(f'{self.__match.team_left_name} {self.__match.score_left} x {self.__match.score_right} {self.__match.team_right_name}')

    def available(self):
        """
        Shows currently available analysis.
        """
        BallPossession = ("BallPossession", True)
        FoulCharge = ("FoulCharge", True)
        Playmodes = ("Playmodes", True)
        Corners = ("Corners", True)
        Penalty = ("Penalty", True)
        BallHistory = ("BallHistory", True)
        TesterFK = ("Tester Free Kick", True)
        TimeAfterEvents = ("TimeAfterEvents", False)
        Stamina = ("Stamina", True)
        Shooting = ("Shooting", True)

        analysis = [BallPossession, FoulCharge, Penalty, Stamina, BallHistory,
                    Playmodes, Corners, TesterFK, TimeAfterEvents, Shooting]

        for a in analysis:
            if a[1]:
                print(a[0])

    def _generate_evaluators(self):
        if self.__cat is SIM2D:
            pass
        elif self.__cat is SSL:
            self.__evaluators = EvaluatorCollection(self.match)
        elif self.__cat is VSS:
            raise NotImplementedError

    def _run_analysis(self):
        if self.__cat is SIM2D:
            setattr(self, "__ball_possession", None)
            self.__ball_possession = BallPossession(self.__match.dataframe, self.category)

            setattr(self, "__intercept_counter", None)
            self.__intercept_counter = InterceptCounter(self.__match)

            setattr(self, "__tester_free_kick", None)
            self.__tester_free_kick = TesterFK(self.__match.dataframe, self.category)

            setattr(self, "__foul_charge", None)
            self.__foul_charge = FoulCharge(self.__match.dataframe, self.category)

            setattr(self, "__penalty", None)
            self.__penalty = Penalty(self.__match.dataframe, self.category)

            setattr(self, "__playmodes", None)
            self.__playmodes = Playmodes(self.__match.dataframe, self.category)

            setattr(self, "__corners", None)
            self.__corners_occurrencies = CornersOcurrencies(self.__match.dataframe, self.category)

            setattr(self, "__time_after_events", None)
            self.__time_after_events = TimeAfterEvents(self.__match.dataframe, self.category,
                                                       self.__corners_occurrencies.results(),
                                                       self.__foul_charge.results(tuple=True))

            setattr(self, "__ball_history", None)
            self.__ball_history = BallHistory(self.__match.dataframe, self.category)

            setattr(self, "__stamina", None)
            self.__stamina = Stamina(self.__match.dataframe, self.category)

            setattr(self, "__shooting", None)
            self.__shooting = Shooting(self.__match.dataframe, self.category)

            setattr(self, "__heatmap", None)
            self.__heatmap = Heatmap(self.__match.dataframe, self.category)

            #setattr(self, "__time_after_corner", None)
            #self.__time_after_corner = TimeAfterCorner(self.__match.dataframe, self.category)

        elif self.__cat is SSL:
            pass
            # setattr(self, "__heatmap", None)
            # self.__heatmap = Heatmap(self.__match.dataframe, self.category)

        elif self.__cat is VSS:
            raise NotImplementedError
            # add VSS analysis

    def collect_results(self):
        raise NotImplementedError