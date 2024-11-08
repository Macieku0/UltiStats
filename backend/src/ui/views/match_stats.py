"""
This module contains the MatchStatsView class, which displays statistics for completed matches.
"""

import flet as ft
from src.ui.views.base_view import BaseView


class MatchStatsView(BaseView):
    """
    Match statistics view - displays statistics for completed matches
    """

    def initialize_view(self):
        # Back button
        back_btn = ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            on_click=lambda _: self.navigate_to("start"),
            tooltip="Back to main menu",
        )

        # Search and filter controls
        self.date_picker = ft.DatePicker(
            on_change=self.filter_matches,
        )

        self.team_dropdown = ft.Dropdown(
            label="Select Team",
            options=[
                ft.dropdown.Option("All Teams"),
                # TODO: Load actual teams from database
            ],
            width=200,
            on_change=self.filter_matches,
        )

        # Matches list
        self.matches_list = ft.ListView(
            expand=1,
            spacing=10,
            padding=20,
        )

        # Layout
        self.page.add(
            ft.Row(
                [
                    back_btn,
                    ft.Text("Match Statistics", size=30, weight=ft.FontWeight.BOLD),
                ]
            ),
            ft.Row(
                [
                    ft.Text("Filter matches:"),
                    ft.IconButton(
                        icon=ft.icons.CALENDAR_TODAY,
                        on_click=lambda _: self.date_picker.pick_date(),
                    ),
                    self.team_dropdown,
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            self.matches_list,
        )

        # Load initial data
        self.load_matches()

    def load_matches(self):
        """Load matches from database"""
        # TODO: Implement database integration
        # For now, show sample matches
        sample_matches = [
            {
                "date": "2024-03-15",
                "team1": "Team A",
                "team2": "Team B",
                "score1": 15,
                "score2": 12,
            },
            {
                "date": "2024-03-14",
                "team1": "Team C",
                "team2": "Team D",
                "score1": 15,
                "score2": 8,
            },
        ]

        for match in sample_matches:
            self.matches_list.controls.append(self.create_match_card(match))
        self.page.update()

    def create_match_card(self, match_data: dict) -> ft.Card:
        """Create a card display for a match"""
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            title=ft.Text(
                                f"{match_data['team1']} vs {match_data['team2']}",
                                weight=ft.FontWeight.BOLD,
                            ),
                            subtitle=ft.Text(f"Date: {match_data['date']}"),
                        ),
                        ft.Text(
                            f"Score: {match_data['score1']} - {match_data['score2']}",
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.Row(
                            [
                                ft.TextButton(
                                    "View Details",
                                    on_click=lambda e: self.show_match_details(
                                        match_data
                                    ),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ]
                ),
                padding=10,
            )
        )

    def filter_matches(self, e):
        """Filter matches based on selected criteria"""
        # TODO: Implement match filtering
        pass

    def show_match_details(self, match_data: dict):
        """Show detailed statistics for a match"""
        # TODO: Implement detailed match view
        pass
