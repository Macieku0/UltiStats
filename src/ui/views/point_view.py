"""
This module contains the PointView class, which is responsible for handling the tracking of individual points in the game.
"""

import flet as ft
from src.ui.views.base_view import BaseView
from src.ui.components.player_circle import (
    PlayerCircleGroup,
    create_draggable_player_circle,
)
from src.database.domain_repositories import (
    TeamRepository,
    PlayerRepository,
    PointRepository,
    GameRepository,
)


class PointView(BaseView):
    """
    Point view - handles tracking of individual points in the game
    """

    def __init__(
        self,
        page: ft.Page,
        navigation_callback,
        game_id: str,
        team1_id: str,
        team2_id: str,
        selected_players: dict[str, list[str]],
        offensive_team: str,
        pull_data: dict,
    ):
        self.game_id = game_id
        self.team1_id = team1_id
        self.team2_id = team2_id
        self.selected_players = selected_players
        self.offensive_team = offensive_team
        self.pull_data = pull_data
        self.team_repo = TeamRepository()
        self.player_repo = PlayerRepository()
        self.point_repo = PointRepository()
        self.game_repo = GameRepository()

        # Field state
        self.field_positions: dict[str, None | str] = {
            f"pos_{i}": None
            for i in range(14)  # 7 positions per team
        }
        self.player_positions: dict[str, None | str] = {}  # player_id: position_id

        super().__init__(page, navigation_callback)

    def initialize_view(self):
        # Load teams
        team1: dict | None = self.team_repo.find_by_id(self.team1_id)
        team2: dict | None = self.team_repo.find_by_id(self.team2_id)

        if not team1 or not team2:
            self.show_error("Teams not found")
            return
        else:
            self.team1: dict = team1
            self.team2: dict = team2

        # Create field view
        field_container = self.create_field_container()

        # Create player benches
        team1_bench = self.create_team_bench(self.team1, "team1")
        team2_bench = self.create_team_bench(self.team2, "team2")

        # Create action buttons
        action_buttons = self.create_action_buttons()

        # Create score display
        score_display = self.create_score_display()

        # Back button
        back_btn = ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            on_click=lambda _: self.navigate_to(
                "setup_point",
                {
                    "game_id": self.game_id,
                    "team1_id": self.team1_id,
                    "team2_id": self.team2_id,
                },
            ),
            tooltip="Back to setup point",
        )

        # Layout
        self.page.add(
            ft.Row(
                [back_btn, ft.Text("Point View", size=30, weight=ft.FontWeight.BOLD)]
            ),
            score_display,
            ft.Row(
                [
                    team1_bench,
                    field_container,
                    team2_bench,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            action_buttons,
        )

    def create_field_container(self) -> ft.Container:
        """Create the ultimate field layout with drop zones"""
        field_rows = []
        positions_per_row = 7

        for row in range(2):  # 2 rows of positions
            position_containers = []
            for pos in range(positions_per_row):
                position_id = f"pos_{row * positions_per_row + pos}"
                drop_target = ft.DragTarget(
                    content=ft.Container(
                        content=None,  # Will be filled when a player is dropped
                        width=60,
                        height=60,
                        border=ft.border.all(1, ft.colors.GREY_400),
                        border_radius=30,
                        alignment=ft.alignment.center,
                    ),
                    on_accept=lambda e, pos_id=position_id: self.handle_player_drop(
                        e, pos_id
                    ),
                )
                position_containers.append(drop_target)

            field_rows.append(
                ft.Row(
                    position_containers,
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                )
            )

        return ft.Container(
            content=ft.Column(
                field_rows,
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                spacing=40,
            ),
            width=600,
            height=300,
            border=ft.border.all(2, ft.colors.GREEN),
            border_radius=10,
            padding=20,
        )

    def create_team_bench(self, team, team_key: str) -> ft.Container:
        """Create a team's bench with draggable player circles"""
        players = [
            self.player_repo.find_by_id(player_id)
            for player_id in self.selected_players[team_key]
        ]

        player_circles = []
        for player in players:
            if player is None:
                self.show_error("Player not found")
                return
            player_number = player.get("number")
            if player_number is None:
                self.show_error("Player number not found")
                return
            player_number = int(player_number)
            draggable = ft.Draggable(
                content=create_draggable_player_circle(
                    number=player_number,
                    bgcolor=team.primary_color
                    if hasattr(team, "primary_color")
                    else ft.colors.BLUE,
                ),
                content_feedback=create_draggable_player_circle(
                    number=player_number,
                    bgcolor=team.primary_color
                    if hasattr(team, "primary_color")
                    else ft.colors.BLUE,
                ),
                data={"player_id": player.get("id"), "team": team_key},
            )
            player_circles.append(draggable)

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(team.get("name"), size=16, weight=ft.FontWeight.BOLD),
                    ft.Column(player_circles, spacing=10),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=10,
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=10,
        )

    def create_score_display(self) -> ft.Row:
        """Create the score display row"""
        return ft.Row(
            [
                ft.Text(
                    f"{self.team1.get("name")}: 0", size=20, weight=ft.FontWeight.BOLD
                ),
                ft.Text(" - ", size=20),
                ft.Text(
                    f"{self.team2.get("name")}: 0", size=20, weight=ft.FontWeight.BOLD
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def create_action_buttons(self) -> ft.Row:
        """Create the action buttons for scoring and turnovers"""
        return ft.Row(
            [
                ft.ElevatedButton(
                    "Score",
                    on_click=self.handle_score,
                    icon=ft.icons.SPORTS_SCORE,
                ),
                ft.ElevatedButton(
                    "Turnover",
                    on_click=self.handle_turnover,
                    icon=ft.icons.SWAP_HORIZ,
                ),
                ft.OutlinedButton(
                    "Reset Positions",
                    on_click=self.reset_positions,
                    icon=ft.icons.REFRESH,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20,
        )

    def handle_player_drop(self, e: ft.DragTargetAcceptEvent, position_id: str):
        """Handle a player being dropped on a field position"""
        player_data = e.data  # Contains player_id and team

        # Remove player from previous position if exists
        if player_data["player_id"] in self.player_positions:
            old_pos = self.player_positions[player_data["player_id"]]
            if old_pos is None:
                raise ValueError("Player position not found")
            self.field_positions[old_pos] = None

        # Update position mappings
        self.field_positions[position_id] = player_data["player_id"]
        self.player_positions[player_data["player_id"]] = position_id

        # Update the visual representation
        player = self.player_repo.find_by_id(player_data["player_id"])
        team = self.team1 if player_data["team"] == "team1" else self.team2

        if player is None:
            self.show_error("Player not found")
            return
        if team is None:
            self.show_error("Team not found")
            return

        player_number = player.get("number")
        if player_number is None:
            self.show_error("Player number not found")
            return
        player_number = int(player_number)

        team_primary_color = team.get("primary_color")
        if team_primary_color is None:
            team_primary_color = ft.colors.BLUE

        e.control.content.content = create_draggable_player_circle(
            number=player_number,
            bgcolor=team_primary_color,
        )
        self.page.update()

    def handle_score(self, e):
        """Handle a scoring event"""
        # Save point data
        point_data = {
            "game_id": self.game_id,
            "scoring_team": self.offensive_team,
            "players": self.player_positions,
            "pull_data": self.pull_data,
        }
        # TODO: Save point data to database

        # Navigate back to setup point
        self.navigate_to(
            "setup_point",
            {
                "game_id": self.game_id,
                "team1_id": self.team1_id,
                "team2_id": self.team2_id,
            },
        )

    def handle_turnover(self, e):
        """Handle a turnover event"""
        # Swap offensive team
        self.offensive_team = "team2" if self.offensive_team == "team1" else "team1"
        # TODO: Record turnover in point data
        self.page.update()

    def reset_positions(self, e):
        """Reset all player positions on the field"""
        self.field_positions = {pos: None for pos in self.field_positions}
        self.player_positions = {}
        self.initialize_view()
