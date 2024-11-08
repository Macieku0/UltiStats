from __future__ import annotations
from pydantic import BaseModel, Field
from enum import Enum


class PlayerRole(str, Enum):
    """Player roles in ultimate frisbee"""

    HANDLER = "Handler"
    CUTTER = "Cutter"
    HYBRID = "Hybrid"


class GameStatus(str, Enum):
    """Game statuses"""

    NOT_STARTED = "not_started"
    ON_GOING = "on_going"
    FINISHED = "finished"


class Gender(str, Enum):
    """
    Player gender
    """

    MALE = "male"
    FEMALE = "female"


class Division(str, Enum):
    """
    Division of the game
    """

    OPEN = "open"
    MIXED = "mixed"
    WOMEN = "women"


class PullLocation(str, Enum):
    """
    Location of the pull
    """

    IN_BOUNDS = "in_bounds"
    OUT_OF_BOUNDS = "out_of_bounds"


class PullCatchOrLift(str, Enum):
    """
    Catch or lift
    """

    CATCH = "catch"
    LIFT = "lift"


class Player(BaseModel):
    id: str
    name: str
    number: int
    role: PlayerRole
    gender: Gender


class Team(BaseModel):
    id: str
    name: str
    city: str
    disivion: Division
    player_ids: list[int]
    created_at: str
    updated_at: str


class TeamScore(BaseModel):
    team_id: str
    score: int


class Scores(BaseModel):
    team_1: TeamScore
    team_2: TeamScore


class Game(BaseModel):
    id: str
    team1: Team
    team2: Team
    status: GameStatus = Field(default=GameStatus.NOT_STARTED)
    score: Scores = Scores(
        team_1=TeamScore(team_id="", score=0),
        team_2=TeamScore(team_id="", score=0),
    )
    points: dict[str, Point] = Field(default_factory=dict)


class GameViewState(BaseModel):
    """State management for GameView"""

    selected_team1: None | str = None
    selected_team2: None | str = None
    current_game: None | Game = None


class PullData(BaseModel):
    pulling_player: str = Field(description="ID of the player who pulled the disc")
    pulling_team: str = Field(description="ID of the team who pulled the disc")
    pull_location: PullLocation = Field(description="Location of the pull")
    catch_or_lift: PullCatchOrLift = Field(description="Catch or lift")
    brick_called: bool = False
    receiving_player: str = Field(
        description="ID of the player who caught/lift the pull"
    )
    receiving_team: str = Field(description="ID of the team who caught/lift the pull")


class Point(BaseModel):
    id: str
    game_id: str
    scoring_team: str
    scoring_player_id: str
    assisting_player_id: str
    team1_players: list[str] = Field(description="Players on team 1")
    team2_players: list[str] = Field(description="Players on team 2")
    pull_data: PullData
    course_of_the_point: dict[str, Action] = Field(
        default_factory=dict, description="Course of the point"
    )


class DiscEvent(str, Enum):
    """Events that can occur during a point"""

    PASS = "pass"
    DEFENSE = "defense"
    DROP = "drop"
    TURNOVER = "turnover"
    TIMEOUT = "timeout"
    SCORE = "score"
    INJURY = "injury"
    CALL = "call"


class CallType(str, Enum):
    """Types of calls that can be made"""

    FOUL = "foul"
    VIOLATION = "violation"
    TRAVEL = "travel"
    PICK = "pick"
    STRIP = "strip"
    DISC_SPACE = "disc_space"
    STALL = "stall"
    DOUBLE_TEAM = "double_team"
    OUT = "out"
    LOST_CONTROL = "lost_control"
    DANGEORUS_PLAY = "dangerous_play"


class ThrowType(str, Enum):
    """Types of throws in ultimate frisbee"""

    BACKHAND = "backhand"
    FOREHAND = "forehand"
    OTHER = "other"


class CallResult(str, Enum):
    """Possible outcomes of a call"""

    ACCEPTED = "accepted"
    CONTESTED = "contested"
    RETRACTED = "retracted"


class Action(BaseModel):
    """
    Actions that can occur during a point.

    This model is used to keep track of the course of a point.
    It have to cover all the possible actions that can occur during a point.
    And by its id we can determine the order of the actions.
    """
