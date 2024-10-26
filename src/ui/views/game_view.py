"""
This module contains the GameView class, which is responsible for rendering the game view.
"""

import flet as ft
from src.ui.views.base_view import BaseView
from src.database.domain_repositories import TeamRepository, GameRepository


class GameView(BaseView):
    """
    Game view - allows selecting teams and starting points
    """

    def __init__(self, page: ft.Page, navigation_callback):
        self.team_repo = TeamRepository()
        self.game_repo = GameRepository()
        self.selected_teams: dict[str, None | str] = {"team1": None, "team2": None}
        self.current_game: dict | None = None
        super().__init__(page, navigation_callback)

    def initialize_view(self):
        # Title
        title = ft.Text("New Game", size=30, weight=ft.FontWeight.BOLD)

        # Team selection dropdowns
        self.team1_dropdown = ft.Dropdown(
            label="Team 1",
            width=300,
            on_change=lambda e: self.update_team_selection("team1", e.data),
        )

        self.team2_dropdown = ft.Dropdown(
            label="Team 2",
            width=300,
            on_change=lambda e: self.update_team_selection("team2", e.data),
        )

        # Start point button
        self.start_point_btn = ft.ElevatedButton(
            text="Start Point",
            icon=ft.icons.PLAY_ARROW,
            on_click=self.start_point,
            disabled=True,
        )

        # Game score display
        self.score_display = ft.Row(
            [
                ft.Text("0", size=40, weight=ft.FontWeight.BOLD),
                ft.Text("-", size=40),
                ft.Text("0", size=40, weight=ft.FontWeight.BOLD),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            visible=False,
        )

        # Layout
        self.page.add(
            ft.Row(
                [
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        on_click=lambda _: self.navigate_to("start"),
                    ),
                    title,
                ]
            ),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Text("Select Teams", size=20, weight=ft.FontWeight.BOLD),
                        self.team1_dropdown,
                        ft.Text("VS", size=20, text_align=ft.TextAlign.CENTER),
                        self.team2_dropdown,
                        ft.Divider(),
                        self.score_display,
                        self.start_point_btn,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                ),
                padding=20,
            ),
        )

        # Load teams
        self.load_teams()

    def load_teams(self):
        """Load teams into dropdowns"""
        teams = self.team_repo.find_all()
        options = [ft.dropdown.Option(team["id"], team["name"]) for team in teams]
        self.team1_dropdown.options = options
        self.team2_dropdown.options = options
        self.page.update()

    def update_team_selection(self, team_key: str, team_id: str):
        """Handle team selection"""
        self.selected_teams[team_key] = team_id

        # Enable/disable start button based on selections
        teams_selected = all(self.selected_teams.values())
        different_teams = (
            self.selected_teams["team1"] != self.selected_teams["team2"]
            if teams_selected
            else False
        )

        self.start_point_btn.disabled = not (teams_selected and different_teams)

        # Create or update game if both teams are selected
        if teams_selected and different_teams:
            if not self.current_game:
                if self.selected_teams["team1"] and self.selected_teams["team2"]:
                    self.current_game = self.game_repo.create_game(
                        team1_id=self.selected_teams["team1"],
                        team2_id=self.selected_teams["team2"],
                    )
                else:
                    raise ValueError("Both teams must be selected to create a game")
            self.score_display.visible = True
        else:
            self.score_display.visible = False

        self.page.update()

    def start_point(self, e):
        """Start a new point"""
        if self.current_game:
            # Navigate to point view with current game ID
            self.navigate_to(
                "setup_point",
                game_id=self.current_game["id"],
                team1_id=self.selected_teams["team1"],
                team2_id=self.selected_teams["team2"],
            )
