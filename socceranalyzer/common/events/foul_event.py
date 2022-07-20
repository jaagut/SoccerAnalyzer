from turtle import position
from socceranalyzer.common.geometric.point import Point
from socceranalyzer.common.events.abstract_event import AbstractEvent
from socceranalyzer.common.basic.match import Match

from socceranalyzer.common.basic.team import Team
from socceranalyzer.agent2D.agent import Agent2D


class FoulEvent(AbstractEvent):
    def __init__(self, 
                match: Match,
                cicles: tuple[int, int], 
                players_left: list[Agent2D],
                players_right: list[Agent2D],
                team_actor: Team): 
        """
            A class to represent a Foul Event in the match

            foul_event(match: Match, cicles: tuple[int, int], players_left: list[Agent2D], players_right: list[Agent2D], team_actor: Team)

            Attributes
            ----------
                public through @properties: 
                    cicles: tuple[int, int]
                        The start and end cicles of the event
                    players_left: list[Agent2D]
                        The left players who participate in the event
                    players_right: list[Agent2D]
                        The right players who participate in the event
                    team_actor: Team
                        The team who commited the action
            
            Methods
            -------
            public: 
                position() -> Point
                    returns the position where the foul occurred
                    
        """
        
        self.__match = match
        self.__cicles = cicles
        self.__players_left = players_left
        self.__players_right = players_right
        self.__team_actor = team_actor

    def position(self) -> Point:
        """
        Returns the position of the ball at the time that the fault occurred. Naive approximation of the foul position.
        """
        dataframe = self.__match.dataframe
        category = self.__match.category

        x = dataframe.loc[self.__cicles[0], str(category.BALL_X)]
        y = dataframe.loc[self.__cicles[0], str(category.BALL_Y)]

        return Point(x, y)

    # TODO: check if the foul resulted in a yellow/red card. First we need to capture this information in log
    
    @property
    def cicles(self):
        return self.__cicles
    
    @property
    def players_left(self):
        return self.__players_left
    
    @property
    def players_right(self):
        return self.__players_right
    
    @property
    def team_actor(self):
        return self.__team_actor