"""
This module contains the domain repositories for the ultimate frisbee database.
"""

from .repository import JsonRepository
import os
from config.settings import settings


class TeamRepository(JsonRepository[dict]):
    def __init__(self):
        super().__init__(directory_path=str(settings.TEAMS_DIR))

    def create_team(self, name: str, city: str) -> dict:
        """Create a new team"""
        return self.create({"name": name, "city": city, "players": []})

    def add_player_to_team(self, team_id: str, player_id: str) -> dict | None:
        """Add a player to a team"""
        team = self.find_by_id(team_id)
        if team:
            if "players" not in team:
                team["players"] = []
            if player_id not in team["players"]:
                team["players"].append(player_id)
            return self.update(team_id, team)
        return None


class PlayerRepository(JsonRepository[dict]):
    def __init__(self):
        super().__init__(directory_path=os.path.join(settings.DATA_DIR, "players"))

    def create_player(self, name: str, number: int, role: str) -> dict:
        """Create a new player"""
        return self.create(
            {
                "name": name,
                "number": number,
                "role": role,
                "stats": {
                    "games_played": 0,
                    "points_played": 0,
                    "goals": 0,
                    "assists": 0,
                    "blocks": 0,
                },
            }
        )

    def find_by_team_id(self, team_id: str) -> list[dict]:
        """Find all players on a specific team"""
        results = []
        team_repo = TeamRepository()
        team = team_repo.find_by_id(team_id)
        if team and "players" in team:
            for player_id in team["players"]:
                player = self.find_by_id(player_id)
                if player:
                    results.append(player)
        return results


class GameRepository(JsonRepository[dict]):
    def __init__(self):
        super().__init__(directory_path=str(settings.GAMES_DIR))

    def create_game(self, team1_id: str, team2_id: str) -> dict:
        """Create a new game"""
        return self.create(
            {
                "team1_id": team1_id,
                "team2_id": team2_id,
                "team1_score": 0,
                "team2_score": 0,
                "status": "active",
                "points": [],
            }
        )

    def add_point(self, game_id: str, point_data: dict) -> dict | None:
        """Add a point to the game"""
        game = self.find_by_id(game_id)
        if game:
            if "points" not in game:
                game["points"] = []
            game["points"].append(point_data)
            # Update score based on point outcome
            if point_data["scoring_team"] == game["team1_id"]:
                game["team1_score"] += 1
            else:
                game["team2_score"] += 1
            return self.update(game_id, game)
        return None


class PointRepository(JsonRepository[dict]):
    def __init__(self):
        super().__init__(directory_path=os.path.join(settings.DATA_DIR, "points"))

    def create_point(
        self, game_id: str, team1_players: list[str], team2_players: list[str]
    ) -> dict:
        """Create a new point"""
        return self.create(
            {
                "game_id": game_id,
                "team1_players": team1_players,
                "team2_players": team2_players,
                "events": [],
                "status": "active",
                "start_time": None,
                "end_time": None,
            }
        )

    def add_event(self, point_id: str, event_data: dict) -> dict | None:
        """Add an event to the point"""
        point = self.find_by_id(point_id)
        if point:
            if "events" not in point:
                point["events"] = []
            point["events"].append(event_data)
            return self.update(point_id, point)
        return None
