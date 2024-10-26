"""
This module contains the PlayerStatsView class, which is responsible for displaying player statistics.
"""

import flet as ft
from src.ui.views.base_view import BaseView


class PlayerStatsView(BaseView):
    """
    Player statistics view - displays individual player statistics
    """

    def initialize_view(self):
        # Back button
        back_btn = ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            on_click=lambda _: self.navigate_to("start"),
            tooltip="Back to main menu",
        )

        # Search and filter controls
        self.search_field = ft.TextField(
            label="Search players",
            width=300,
            prefix_icon=ft.icons.SEARCH,
            on_change=self.filter_players,
        )

        self.team_dropdown = ft.Dropdown(
            label="Filter by Team",
            options=[
                ft.dropdown.Option("All Teams"),
                # TODO: Load actual teams from database
            ],
            width=200,
            on_change=self.filter_players,
        )

        # Players list
        self.players_list = ft.ListView(
            expand=1,
            spacing=10,
            padding=20,
        )

        # Layout
        self.page.add(
            ft.Row(
                [
                    back_btn,
                    ft.Text("Player Statistics", size=30, weight=ft.FontWeight.BOLD),
                ]
            ),
            ft.Row(
                [
                    self.search_field,
                    self.team_dropdown,
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            self.players_list,
        )

        # Load initial data
        self.load_players()

    def load_players(self):
        """Load players from database"""
        # TODO: Implement database integration
        # For now, show sample players
        sample_players = [
            {
                "name": "John Doe",
                "number": 7,
                "team": "Team A",
                "stats": {
                    "games": 10,
                    "points": 25,
                    "assists": 15,
                    "catches": 45,
                },
            },
            {
                "name": "Jane Smith",
                "number": 14,
                "team": "Team B",
                "stats": {
                    "games": 8,
                    "points": 18,
                    "assists": 22,
                    "catches": 38,
                },
            },
        ]

        for player in sample_players:
            self.players_list.controls.append(self.create_player_card(player))
        self.page.update()

    def create_player_card(self, player_data: dict) -> ft.Card:
        """Create a card display for a player"""
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.CircleAvatar(
                                content=ft.Text(str(player_data["number"])),
                            ),
                            title=ft.Text(
                                player_data["name"],
                                weight=ft.FontWeight.BOLD,
                            ),
                            subtitle=ft.Text(f"Team: {player_data['team']}"),
                        ),
                        ft.Divider(),
                        ft.Row(
                            [
                                ft.Text(f"Games: {player_data['stats']['games']}"),
                                ft.Text(f"Points: {player_data['stats']['points']}"),
                                ft.Text(f"Assists: {player_data['stats']['assists']}"),
                                ft.Text(f"Catches: {player_data['stats']['catches']}"),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ]
                ),
                padding=10,
            ),
        )
