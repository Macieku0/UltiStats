# Main application class for Ultimate Frisbee statistics gathering.
import flet as ft

from src.ui.components.theme import create_theme_switch
from src.ui.views.game_view import GameView
from src.ui.views.start_page import StartPage
from src.ui.views.team_manager import TeamManager
from src.ui.views.match_stats import MatchStatsView
from src.ui.views.player_stats import PlayerStatsView
from src.ui.views.point_view import PointView
from src.ui.views.setup_point import SetupPointView
from src.ui.views.pull_info import PullInfoView


class UltiStatsApp:
    """Main application class for Ultimate Frisbee statistics gathering."""

    def __init__(self, page: ft.Page):
        self.page = page
        self.setup_page()
        self.current_view = None
        self.initialize_app()

    def setup_page(self):
        """Initialize page settings and theme"""
        self.page.title = "Ultimate Stats"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.theme_mode = ft.ThemeMode.LIGHT

        # Create and set app bar
        theme_switch = create_theme_switch(self.page)
        self.page.appbar = ft.AppBar(
            title=ft.Text("Ultimate Stats", size=24, weight=ft.FontWeight.BOLD),
            center_title=True,
            actions=[theme_switch],
        )

    def initialize_app(self):
        """Show initial view"""
        self.navigate_to("start")

    def navigate_to(self, view_name: str, **kwargs):
        """Navigate to specified view"""
        self.page.clean()

        views = {
            "start": StartPage,
            "team_manager": TeamManager,
            "game": GameView,
            "match_stats": MatchStatsView,
            "point": PointView,
            "pull_info": PullInfoView,
            "setup_point": SetupPointView,
            "player_stats": PlayerStatsView,
        }
        current_view = views.get(view_name)
        if current_view is not None:
            self.current_view = current_view(self.page, self.navigate_to, **kwargs)
        else:
            raise ValueError(f"View not found: {view_name}")
