"""
This module contains the PullInfoView class, which is responsible for capturing details about the pull and initial possession.
"""

import flet as ft
from src.ui.views.base_view import BaseView
from src.database.domain_repositories import TeamRepository, PlayerRepository


class PullInfoView(BaseView):
    """
    Pull information view - captures details about the pull and initial possession
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
    ):
        self.game_id: str = game_id
        self.team1_id: str = team1_id
        self.team2_id: str = team2_id
        self.selected_players: dict[str, list[str]] = selected_players
        self.offensive_team = offensive_team
        self.team_repo = TeamRepository()
        self.player_repo = PlayerRepository()
        self.pull_data: dict[str, None | str] = {
            "pulling_player": None,
            "pull_location": None,
            "catch_or_lift": None,
            "brick_called": None,
            "receiving_player": None,
        }
        super().__init__(page, navigation_callback)

    def initialize_view(self):
        # Load teams
        self.team1 = self.team_repo.find_by_id(self.team1_id)
        self.team2 = self.team_repo.find_by_id(self.team2_id)

        # Determine pulling and receiving teams
        pulling_team = self.team2 if self.offensive_team == "team1" else self.team1
        receiving_team = self.team1 if self.offensive_team == "team1" else self.team2

        if not pulling_team or not receiving_team:
            self.show_error("Teams not found")
            return

        # Pulling player selection
        pulling_players: list[dict] = []
        for player_id in self.selected_players[
            "team2" if self.offensive_team == "team1" else "team1"
        ]:
            player = self.player_repo.find_by_id(player_id)
            if player is not None:
                pulling_players.append(player)
        self.pulling_player_dropdown = ft.Dropdown(
            label="Select pulling player",
            options=[
                ft.dropdown.Option(key=str(player.get("id")), text=player.get("name"))
                for player in pulling_players
            ],
            width=200,
            on_change=self.handle_pulling_player_change,
        )

        # Pull location radio buttons
        self.pull_location = ft.RadioGroup(
            content=ft.Row(
                [
                    ft.Radio(value="in_bounds", label="In Bounds"),
                    ft.Radio(value="out_of_bounds", label="Out of Bounds"),
                ]
            ),
            on_change=self.handle_pull_location_change,
        )

        # Catch/Lift options (initially hidden)
        self.catch_lift_row = ft.Row(
            [
                ft.Text("Pull was: "),
                ft.RadioGroup(
                    content=ft.Row(
                        [
                            ft.Radio(value="caught", label="Caught"),
                            ft.Radio(value="lifted", label="Lifted from ground"),
                        ]
                    ),
                    on_change=lambda e: self.update_pull_data(
                        field="catch_or_lift", value=e.control.value
                    ),
                ),
            ],
            visible=False,
        )

        # Brick options (initially hidden)
        self.brick_row = ft.Row(
            [
                ft.Text("Brick called? "),
                ft.RadioGroup(
                    content=ft.Row(
                        [
                            ft.Radio(value="yes", label="Yes"),
                            ft.Radio(value="no", label="No"),
                        ]
                    ),
                    on_change=lambda e: self.update_pull_data(
                        "brick_called", e.control.value
                    ),
                ),
            ],
            visible=False,
        )

        # Receiving player selection
        receiving_players: list[dict] = []
        for player_id in self.selected_players[
            "team1" if self.offensive_team == "team1" else "team2"
        ]:
            player = self.player_repo.find_by_id(player_id)
            if player is not None:
                receiving_players.append(player)

        self.receiving_player_dropdown = ft.Dropdown(
            label="Select receiving/lifting player",
            options=[
                ft.dropdown.Option(key=str(player.get("id")), text=player.get("name"))
                for player in receiving_players
            ],
            width=200,
            on_change=lambda e: self.update_pull_data("receiving_player", e.data),
        )

        # Continue button
        self.continue_button = ft.ElevatedButton(
            "Start Point", on_click=self.start_point, disabled=True
        )

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
                [
                    back_btn,
                    ft.Text("Pull Information", size=30, weight=ft.FontWeight.BOLD),
                ]
            ),
            ft.Divider(),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text(f"Pulling Team: {pulling_team.get('name')}", size=20),
                        self.pulling_player_dropdown,
                        ft.Text("Where did the pull land?", size=16),
                        self.pull_location,
                        self.catch_lift_row,
                        self.brick_row,
                        ft.Text(
                            f"Receiving Team: {receiving_team.get('name')}", size=20
                        ),
                        self.receiving_player_dropdown,
                        self.continue_button,
                    ]
                ),
                padding=20,
            ),
        )

    def handle_pulling_player_change(self, e):
        self.update_pull_data("pulling_player", e.data)

    def handle_pull_location_change(self, e):
        self.pull_data["pull_location"] = e.control.value
        self.catch_lift_row.visible = e.control.value == "in_bounds"
        self.brick_row.visible = e.control.value == "out_of_bounds"
        self.page.update()

    def update_pull_data(self, field: str, value: str):
        self.pull_data[field] = value
        self.update_continue_button()
        self.page.update()

    def update_continue_button(self):
        self.continue_button.disabled = not all(
            [
                self.pull_data["pulling_player"],
                self.pull_data["pull_location"],
                self.pull_data["receiving_player"],
                (
                    self.pull_data["catch_or_lift"]
                    if self.pull_data["pull_location"] == "in_bounds"
                    else True
                )
                or (
                    self.pull_data["brick_called"]
                    if self.pull_data["pull_location"] == "out_of_bounds"
                    else True
                ),
            ]
        )

    def start_point(self, e):
        # Navigate to point view with all collected data
        self.navigate_to(
            "point",
            game_id=self.game_id,
            team1_id=self.team1_id,
            team2_id=self.team2_id,
            selected_players=self.selected_players,
            offensive_team=self.offensive_team,
            pull_data=self.pull_data,
        )
