"""
This module contains the StartPage class, which is a view that represents the landing page of the application.
"""

import flet as ft
from src.ui.views.base_view import BaseView


class StartPage(BaseView):
    """
    Start page view - the landing page of the application.
    Provides navigation to different sections of the app.
    """

    def initialize_view(self):
        title = ft.Text(
            "UltiStats",
            size=40,
            weight=ft.FontWeight.BOLD,
            text_align=ft.TextAlign.CENTER,
        )

        subtitle = ft.Text(
            "Ultimate Frisbee Statistics Tracker",
            size=20,
            weight=ft.FontWeight.W_300,
            text_align=ft.TextAlign.CENTER,
        )

        # Main menu buttons
        new_game_btn = ft.ElevatedButton(
            text="New Game",
            icon=ft.icons.SPORTS,
            on_click=lambda _: self.navigate_to("game"),
        )

        manage_teams_btn = ft.ElevatedButton(
            text="Manage Teams",
            icon=ft.icons.GROUP,
            on_click=lambda _: self.navigate_to("team_manager"),
        )

        match_stats_btn = ft.ElevatedButton(
            text="Match Statistics",
            icon=ft.icons.BAR_CHART,
            on_click=lambda _: self.navigate_to("match_stats"),
        )

        player_stats_btn = ft.ElevatedButton(
            text="Player Statistics",
            icon=ft.icons.PERSON,
            on_click=lambda _: self.navigate_to("player_stats"),
        )

        # Layout
        self.page.add(
            ft.Container(
                content=ft.Column(
                    [
                        title,
                        subtitle,
                        ft.Divider(height=40),
                        ft.Container(
                            content=ft.Column(
                                [
                                    new_game_btn,
                                    manage_teams_btn,
                                    match_stats_btn,
                                    player_stats_btn,
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=20,
                            ),
                            padding=ft.padding.all(20),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10,
                ),
                padding=ft.padding.all(20),
            )
        )
