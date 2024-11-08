from pydantic import BaseModel, Field
from enum import Enum


class PlayerRole(str, Enum):
    """Player roles in ultimate frisbee"""

    HANDLER = "Handler"
    CUTTER = "Cutter"
    HYBRID = "Hybrid"


class Player(BaseModel):
    id: str
    name: str
    number: int
    role: PlayerRole


class Team(BaseModel):
    id: str
    name: str
    primary_color: str


class TeamScore(BaseModel):
    team_id: str
    team_name: str
    score: int


class Scores(BaseModel):
    team_1: TeamScore
    team_2: TeamScore


class Game(BaseModel):
    id: str
    team1_id: str
    team2_id: str
    score: Scores = Scores(
        team_1=TeamScore(team_id="", team_name="", score=0),
        team_2=TeamScore(team_id="", team_name="", score=0),
    )


class PullData(BaseModel):
    pulling_player: str | None = None
    pull_location: None | str = None
    catch_or_lift: None | str = None
    brick_called: None | str = None
    receiving_player: None | str = None


class Point(BaseModel):
    id: str
    game_id: str
    scoring_team: str
    players: dict[int, Player]
    pull_data: PullData
