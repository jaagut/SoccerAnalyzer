from socceranalyzer.common.abstract.abstract_analysis import AbstractAnalysis
from socceranalyzer.common.enums.sim2d import SIM2D
from socceranalyzer.common.chore.mediator import Mediator

class Stamina(AbstractAnalysis):
    """
        Provides players' stamina attributes over the course of the entire match.

        Attributes
        ----------
            private:
                dataframe : pandas.Dataframe
                    match's log to be analyzed
                category : enum
                    match's category (2D, VSS or SSL)
                l_player_stamina: list[float]
                    a list containing stamina attributes of left team players
                r_player_stamina: list[float]
                    a list containing stamina attributes of right team players

        Methods
        -------
            private:
                _analyze() -> None
                    appends players' stamina to their team list

            public:
                results() -> (list[float], list[float])
                    
            
    """
    def __init__(self, dataframe, category):
        self.__dataframe = dataframe
        self.__category = category
        self.__l_players_stamina = []
        self.__l_players_stamina_mean = 0
        self.__r_players_stamina = []
        self.__r_players_stamina_mean = 0

    @property
    def category(self):
        return self.__category

    @property
    def dataframe(self):
        return self.__dataframe

    def _analyze(self):

        if self.__l_players_stamina is not []:
            self.__l_players_stamina = []

        for stamina_attr in Mediator.players_left_stamina_attr(SIM2D):
            self.__l_players_stamina.append(self.dataframe[stamina_attr].tolist())

        for stamina_attr in Mediator.players_right_stamina_attr(self.dataframe):
            self.__r_players_stamina.append(self.dataframe[stamina_attr].tolist())

    @property
    def stamina_left(self):
        return self.__l_players_stamina

    @property
    def stamina_right(self):
        return self.__r_players_stamina

    def results(self):
        return (self.stamina_left, self.stamina_right)

    def describe(self):
        raise NotImplementedError

    def serialize(self):
        raise NotImplementedError