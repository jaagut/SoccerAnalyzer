from typing import List, Optional, Dict

import pandas as pd

from socceranalyzer.common.geometric.point import Point
from socceranalyzer.common.geometric.rectangle import Rectangle
from socceranalyzer.common.basic.field import Field
from socceranalyzer.common.basic.team import Team 
from socceranalyzer.common.basic.ball import Ball
from socceranalyzer.agent2D.agent import Agent2D

from socceranalyzer.common.enums.vss import VSS
from socceranalyzer.common.enums.sim2d import SIM2D, Landmarks as SIM2DLandmarks
from socceranalyzer.common.enums.ssl import SSL
from socceranalyzer.common.enums.hl_kid import HLKid, Landmarks as HLKidLandmarks


class Builder:
    def __init__(self, dataframe: pd.DataFrame, category: SIM2D | SSL | VSS | HLKid, meta_data: Optional[Dict] = None):
        self._df = dataframe
        self._category = category
        self._meta_data = meta_data

    def playerBuilder(self, team: Team) -> List[Agent2D]:
        """
        Returns a list of Agent2D instances representing the players/Robots in the match.

            Parameters:
                team (Team): Team of the players
            Returns:
                players_array (List[Agent2D]): list of Agent2D instances with information about their team
        
        """
        players_array: List[Agent2D] = []
        if self._category == SIM2D:
            for i in range(1, 12):
                players_array.append(Agent2D(team.name, team.identifier, i))
        elif self._category == HLKid:
            if self._meta_data is not None:
                meta_team = None
                for meta_team in self._meta_data['teams'].values():
                    if meta_team['name'] == team.name:
                        break
                if meta_team is None:
                    raise RuntimeError(f"HLKid team with name {team.name} not found in metadata")
                for i in range(1, 5):
                    if f'player{i}' in meta_team.keys():
                        players_array.append(Agent2D(team.name, team.identifier, meta_team[f'player{i}']['id']))
            else:
                raise RuntimeError("HLKid requires metadata to function properly")
        elif self._category == VSS:
            raise NotImplementedError
        elif self._category == SSL:
            raise NotImplementedError
        else:
            raise NotImplementedError
        return players_array

    def teamBuilder(self, identifier: str) -> Team:
        """
        Builds an instance of a Team class representing the team playing the match
            Parameters:
                identifier (str): A string to differentiate between the teams in the match. SIM2D uses 'left' and 'right' while VSS and SSL use colors
                For HLKid, left is team1 and right is team2
            Returns:
                team (Team): Team instance with its identifier
        """
        if self._category == SIM2D:
            if identifier == 'left':
                team_name = self._df.loc[1, str(self._category.TEAM_LEFT)]
                team = Team(team_name, "left")
            else:
                team_name = self._df.loc[1, str(self._category.TEAM_RIGHT)]
                team = Team(team_name, "right")
            return team
        elif self._category == HLKid:
            if self._meta_data is not None:
                if identifier == 'left':
                    team = Team(
                        name=self._meta_data['teams']['team1']['name'],
                        identifier='left'
                    )
                else:
                    team = Team(
                        name=self._meta_data['teams']['team2']['name'],
                        identifier='right'
                    )
                return team
            else:
                raise RuntimeError("HLKid requires metadata to function properly")

        elif self._category == VSS:
            raise NotImplementedError
        elif self._category == SSL:
            raise NotImplementedError
        else:
            raise NotImplementedError

    def ballBuilder(self) -> Ball:
        """
        Returns an instance of a Ball class representing the ball in the field, starting at the center of the field
            Returns:
                ball (Ball): Ball instance starting at position (0,0)
        """
        ball = Ball(0.0, 0.0)

        return ball

    def fieldBuilder(self) -> Field:
        """
        Returns an instance of the Field class representing the field that the game occurred. Passes the field measures depending on the game category.
            Returns:
                field (Field): Field instance with the field measures
        """
        if self._category == SIM2D:
            l_top_left_pen_area = Point(SIM2DLandmarks.LEFT_TOP.x, SIM2DLandmarks.L_PEN_TOP.y)
            r_bottom_right_pen_area = Point(SIM2DLandmarks.RIGHT_BOTTOM.x, SIM2DLandmarks.R_PEN_BOTTOM.y)
            field = Field(68, 105, 
                        SIM2DLandmarks.CENTER,
                        1.0, # TODO
                        Rectangle(l_top_left_pen_area, SIM2DLandmarks.L_PEN_BOTTOM),
                        Rectangle(SIM2DLandmarks.R_PEN_TOP, r_bottom_right_pen_area),
                        Rectangle(Point(-52,-9), Point(-47 , 9)),
                        Rectangle(Point(47,-9), Point(52, 9)),
                        Rectangle(SIM2DLandmarks.L_GOAL_TOP_BAR, SIM2DLandmarks.L_GOAL_BOTTOM_BAR),
                        Rectangle(SIM2DLandmarks.R_GOAL_TOP_BAR, SIM2DLandmarks.R_GOAL_BOTTOM_BAR))
            return field
        elif self._category == HLKid:
            field = Field(
                width=6,
                length=9,
                center=HLKidLandmarks.CENTER,
                center_circle_diameter=HLKidLandmarks.CENTER_CIRCLE_DIAMETER,
                penalty_area_left=HLKidLandmarks.LEFT_SIDE_PENALTY_AREA,
                penalty_area_right=HLKidLandmarks.RIGHT_SIDE_PENALTY_AREA,
                small_penalty_area_left=HLKidLandmarks.LEFT_SIDE_GOAL_AREA,
                small_penalty_area_right=HLKidLandmarks.RIGHT_SIDE_GOAL_AREA,
                goalpost_left=HLKidLandmarks.LEFT_SIDE_GOAL_NET_AREA,
                goalpost_right=HLKidLandmarks.RIGHT_SIDE_GOAL_NET_AREA,
                penalty_mark_left=HLKidLandmarks.LEFT_SIDE_PENALTY_MARK,
                penalty_mark_right=HLKidLandmarks.RIGHT_SIDE_PENALTY_MARK
            )
            return field
        elif self._category == VSS:
            raise NotImplementedError
        elif self._category == SSL:
            raise NotImplementedError
        else:
            raise NotImplementedError
