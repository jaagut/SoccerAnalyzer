from enum import Enum
from socceranalyzer.common.geometric import Point, Circle, Rectangle

class HLKid(Enum):
    """
        It's purpose is to map all parameters of Humanoid League 
        (kid size) with the same keys used in other categories.
        The keys are used inside the analysis for them to be 
        category agnostic.
        
        All parameters are strings
    """
    GAME_TIME = "time"
    PLAYMODE = "game_control_data.game_state"
    RUNNING_GAME = "TODO"
    FAULT_COMMITED_L = "TODO"
    FAULT_COMMITED_R = "TODO"
    BALL_X = "ball.frame.pose.position.x"
    BALL_Y = "ball.frame.pose.position.y"
    BALL_Z = "ball.frame.pose.position.z"
    TEAM_LEFT = "TODO"
    TEAM_RIGHT = "TODO"
    TEAM_LEFT_SCORE = "teams.team1.score"
    TEAM_RIGHT_SCORE = "teams.team2.score"
    TEAM_LEFT_CORNER = "TODO"
    TEAM_RIGHT_CORNER = "TODO"
    PENALTY_TO_LEFT = "teams.team1.penalty_shots"
    PENALTY_TO_RIGHT = "teams.team2.penalty_shots"
    FK_LEFT = "TODO"
    FK_RIGHT = "TODO"
    GOAL_SCORED_L = "TODO"
    GOAL_SCORED_R = "TODO"
    LEFT_GOALKEEPER_CATCHES = "TODO"
    RIGHT_GOALKEEPER_CATCHES = "TODO"

    def __str__(self):
        return self.value

class Landmarks:
    # Measurements in meters
    # Taken from the official rules from 2022
    # https://humanoid.robocup.org/wp-content/uploads/RC-HL-2022-Rules-Changes-Marked-3.pdf
    FIELD_LENGTH = 9.0              # A
    FIELD_WIDTH = 6.0               # B
    GOAL_DEPTH = 0.6                # C
    GOAL_WIDTH = 2.6                # D
    GOAL_HEIGHT = 1.2
    GOAL_AREA_LENGTH = 1.0          # E
    GOAL_AREA_WIDTH = 3.0           # F
    PENALTY_MARK_DISTANCE = 1.5     # G
    CENTER_CIRCLE_DIAMETER = 1.5    # H
    BORDER_STRIP_WIDTH = 1.0        # I
    PENALTY_AREA_LENGTH = 2.0       # J
    PENALTY_AREA_WIDTH = 5.0        # K

    CENTER = Point(0.0, 0.0)
    CENTER_CIRCLE = Circle(CENTER_CIRCLE_DIAMETER/2, CENTER)

    FIELD_AREA = Rectangle(
        Point(-FIELD_LENGTH/2, FIELD_WIDTH/2),
        Point(FIELD_LENGTH/2, -FIELD_WIDTH/2)
    )

    FIELD_AREA_WITH_BORDER = Rectangle(
        Point(-FIELD_LENGTH/2 - BORDER_STRIP_WIDTH, FIELD_WIDTH/2 + BORDER_STRIP_WIDTH),
        Point(FIELD_LENGTH/2 + BORDER_STRIP_WIDTH, -FIELD_WIDTH/2 - BORDER_STRIP_WIDTH)
    )

    LEFT_SIDE = Rectangle(
        Point(-FIELD_LENGTH/2, FIELD_WIDTH/2),
        Point(0.0, -FIELD_WIDTH/2)
    )
    LEFT_SIDE_PENALTY_MARK = Point(-FIELD_LENGTH/2 + PENALTY_MARK_DISTANCE, 0.0)
    LEFT_SIDE_GOAL_CENTER = Point(-FIELD_LENGTH/2, 0.0)
    LEFT_SIDE_GOAL_POST_TOP = Point(-FIELD_LENGTH/2, GOAL_WIDTH/2)
    LEFT_SIDE_GOAL_POST_BOTTOM = Point(-FIELD_LENGTH/2, -GOAL_WIDTH/2)
    LEFT_SIDE_GOAL_NET_AREA = Rectangle(
        Point(-FIELD_LENGTH/2 -GOAL_DEPTH, GOAL_WIDTH/2),
        Point(-FIELD_LENGTH/2, -GOAL_WIDTH/2)
    )
    LEFT_SIDE_GOAL_AREA = Rectangle(
        Point(-FIELD_LENGTH/2, GOAL_AREA_WIDTH/2),
        Point(-FIELD_LENGTH/2 + GOAL_AREA_LENGTH, -GOAL_AREA_WIDTH/2)
    )
    LEFT_SIDE_PENALTY_AREA = Rectangle(
        Point(-FIELD_LENGTH/2, PENALTY_AREA_WIDTH/2),
        Point(-FIELD_LENGTH/2 + PENALTY_AREA_LENGTH, -PENALTY_AREA_WIDTH/2)
    )

    RIGHT_SIDE = Rectangle(
        Point(0.0, FIELD_WIDTH/2),
        Point(FIELD_LENGTH/2, -FIELD_WIDTH/2)
    )
    RIGHT_SIDE_PENALTY_MARK = Point(FIELD_LENGTH/2 - PENALTY_MARK_DISTANCE, 0.0)
    RIGHT_SIDE_GOAL_CENTER = Point(FIELD_LENGTH/2, 0.0)
    RIGHT_SIDE_GOAL_POST_TOP = Point(FIELD_LENGTH/2, GOAL_WIDTH/2)
    RIGHT_SIDE_GOAL_POST_BOTTOM = Point(FIELD_LENGTH/2, -GOAL_WIDTH/2)
    RIGHT_SIDE_GOAL_NET_AREA = Rectangle(
        Point(FIELD_LENGTH/2, GOAL_WIDTH/2),
        Point(FIELD_LENGTH/2 + GOAL_DEPTH, -GOAL_WIDTH/2)
    )
    RIGHT_SIDE_GOAL_AREA = Rectangle(
        Point(FIELD_LENGTH/2 - GOAL_AREA_LENGTH, GOAL_AREA_WIDTH/2),
        Point(FIELD_LENGTH/2, -GOAL_AREA_WIDTH/2)
    )
    RIGHT_SIDE_PENALTY_AREA = Rectangle(
        Point(FIELD_LENGTH/2 - PENALTY_AREA_LENGTH, PENALTY_AREA_WIDTH/2),
        Point(FIELD_LENGTH/2, -PENALTY_AREA_WIDTH/2)
    )
