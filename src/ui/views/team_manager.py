import flet as ft
from src.ui.views.base_view import BaseView
from typing import Callable
from src.database.domain_repositories import TeamRepository, PlayerRepository
from enum import Enum


class PlayerRole(str, Enum):
    """Player roles in ultimate frisbee"""

    HANDLER = "Handler"
    CUTTER = "Cutter"
    HYBRID = "Hybrid"


class PlayerManager:
    """Nested view for managing players within a team"""

    def __init__(self, page: ft.Page, team_id: str, on_close: Callable):
        self.page = page
        self.team_id = team_id
        self.on_close = on_close
        self.team_repository = TeamRepository()
        self.player_repository = PlayerRepository()
        self.container = ft.Container()
        self.initialize_view()

    def initialize_view(self):
        # Player list
        self.players_list = ft.ListView(
            expand=1,
            spacing=10,
            padding=20,
        )

        # New player form
        self.player_name_field = ft.TextField(
            label="Player Name",
            width=300,
        )

        self.player_number_field = ft.TextField(
            label="Number",
            width=300,
            input_filter=ft.NumbersOnlyInputFilter(),
        )

        self.player_role_dropdown = ft.Dropdown(
            label="Role",
            width=300,
            options=[ft.dropdown.Option(role.value) for role in PlayerRole],
        )

        # Add player button
        add_player_btn = ft.ElevatedButton(
            text="Add Player",
            icon=ft.icons.ADD,
            on_click=self.add_player,
        )

        # Close button
        close_btn = ft.IconButton(
            icon=ft.icons.CLOSE,
            on_click=lambda _: self.on_close(),
            tooltip="Close player management",
        )

        team = self.team_repository.find_by_id(self.team_id)
        team_name = team["name"] if team else "Unknown Team"

        # Layout
        self.container.content = ft.Column(
            [
                ft.Row(
                    [
                        close_btn,
                        ft.Text(
                            f"Manage Players - {team_name}",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                        ),
                    ]
                ),
                ft.Divider(),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "Add New Player", size=20, weight=ft.FontWeight.BOLD
                            ),
                            self.player_name_field,
                            self.player_number_field,
                            self.player_role_dropdown,
                            add_player_btn,
                        ],
                        spacing=20,
                    ),
                    padding=20,
                ),
                ft.Divider(),
                ft.Text("Current Players", size=20, weight=ft.FontWeight.BOLD),
                self.players_list,
            ],
            scroll=ft.ScrollMode.AUTO,
        )

        self.load_players()

    def load_players(self):
        """Load players for the current team"""
        team = self.team_repository.find_by_id(self.team_id)
        self.players_list.controls.clear()

        if team and "players" in team:
            for player_id in team["players"]:
                player = self.player_repository.find_by_id(player_id)
                if player:
                    self.players_list.controls.append(self.create_player_card(player))

        self.page.update()

    def add_player(self, e):
        """Add a new player to the team"""
        if not self.player_name_field.value:
            self.show_error("Player name is required")
            return

        if not self.player_number_field.value:
            self.show_error("Player number is required")
            return

        if not self.player_role_dropdown.value:
            self.show_error("Player role is required")
            return

        try:
            number = int(self.player_number_field.value)
            # Create player using repository
            player = self.player_repository.create_player(
                name=self.player_name_field.value,
                number=number,
                role=self.player_role_dropdown.value,
            )

            # Add player to team
            self.team_repository.add_player_to_team(self.team_id, player["id"])

            # Add to list
            self.players_list.controls.append(self.create_player_card(player))

            # Clear form
            self.player_name_field.value = ""
            self.player_number_field.value = ""
            self.player_role_dropdown.value = None

            self.page.update()

        except ValueError:
            self.show_error("Invalid number format")

    def create_player_card(self, player: dict) -> ft.Card:
        """Create a card display for a player"""
        delete_btn = ft.IconButton(
            icon=ft.icons.DELETE,
            on_click=lambda e, player_id=player["id"]: self.delete_player(player_id),
        )

        return ft.Card(
            content=ft.Container(
                content=ft.ListTile(
                    leading=ft.CircleAvatar(
                        content=ft.Text(str(player["number"])),
                    ),
                    title=ft.Text(player["name"], weight=ft.FontWeight.BOLD),
                    subtitle=ft.Text(f"Role: {player['role']}"),
                    trailing=delete_btn,
                ),
                padding=10,
            )
        )

    def delete_player(self, player_id: str):
        """Delete a player from the team and repository"""
        team = self.team_repository.find_by_id(self.team_id)
        if team and "players" in team:
            # Remove player from team
            team["players"].remove(player_id)
            self.team_repository.update(self.team_id, team)

            # Delete player from repository
            self.player_repository.delete(player_id)

            # Refresh the player list
            self.load_players()

    def show_error(self, message: str):
        """Show error message"""
        self.page.show_snack_bar(
            ft.SnackBar(content=ft.Text(message), bgcolor=ft.colors.ERROR)
        )


class TeamManager(BaseView):
    """Team management view - allows creating, editing, and managing teams"""

    def __init__(self, page: ft.Page, navigation_callback: Callable):
        self.team_repository = TeamRepository()
        self.player_repository = PlayerRepository()
        self.current_view = "teams"  # Track current view: "teams" or "players"
        super().__init__(page, navigation_callback)

    def initialize_view(self):
        # Create main container for swapping views
        self.main_container = ft.Container(expand=True)

        # Initialize both views
        self.teams_view = self.create_teams_view()
        self.player_manager = None

        # Set initial view
        self.show_teams_view()

        # Add main container to page
        self.page.add(self.main_container)

    def create_teams_view(self) -> ft.Column:
        """Create the teams list view"""
        # Team list section
        self.teams_list = ft.ListView(
            expand=1,
            spacing=10,
            padding=20,
        )

        # New team form
        self.team_name_field = ft.TextField(
            label="Team Name",
            width=300,
        )

        self.team_city_field = ft.TextField(
            label="City",
            width=300,
        )

        # Add team button
        add_team_btn = ft.ElevatedButton(
            text="Add Team",
            icon=ft.icons.ADD,
            on_click=self.add_team,
        )

        # Back button
        back_btn = ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            on_click=lambda _: self.navigate_to("start"),
            tooltip="Back to main menu",
        )

        # Create teams view
        teams_view = ft.Column(
            [
                ft.Row(
                    [
                        back_btn,
                        ft.Text("Team Management", size=30, weight=ft.FontWeight.BOLD),
                    ]
                ),
                ft.Divider(),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Add New Team", size=20, weight=ft.FontWeight.BOLD),
                            self.team_name_field,
                            self.team_city_field,
                            add_team_btn,
                        ],
                        spacing=20,
                    ),
                    padding=20,
                ),
                ft.Divider(),
                ft.Text("Teams", size=20, weight=ft.FontWeight.BOLD),
                self.teams_list,
            ],
            scroll=ft.ScrollMode.AUTO,
        )

        # Load existing teams
        self.load_teams()

        return teams_view

    def show_teams_view(self):
        """Show the teams list view"""
        self.current_view = "teams"
        self.main_container.content = self.teams_view
        self.page.update()

    def show_player_manager(self, team_id: str):
        """Show the player manager view for a specific team"""
        self.current_view = "players"
        self.player_manager = PlayerManager(
            self.page, team_id, on_close=self.show_teams_view
        )
        self.main_container.content = self.player_manager.container
        self.page.update()

    def load_teams(self):
        """Load teams from repository"""
        teams_data = self.team_repository.find_all()
        self.teams_list.controls.clear()

        for team in teams_data:
            self.teams_list.controls.append(self.create_team_card(team))

        self.page.update()

    def add_team(self, e):
        """Add a new team"""
        if not self.team_name_field.value:
            self.show_error("Team name is required")
            return

        # Create team using repository
        new_team = self.team_repository.create_team(
            name=self.team_name_field.value, city=self.team_city_field.value
        )

        # Add to list
        self.teams_list.controls.append(self.create_team_card(new_team))

        # Clear form
        self.team_name_field.value = ""
        self.team_city_field.value = ""

        self.page.update()

    def create_team_card(self, team: dict) -> ft.Card:
        """Create a card display for a team"""
        delete_btn = ft.IconButton(
            icon=ft.icons.DELETE,
            on_click=lambda e, team_id=team["id"]: self.delete_team(team_id),
        )

        manage_players_btn = ft.ElevatedButton(
            text="Manage Players",
            icon=ft.icons.PEOPLE,
            on_click=lambda e, team_id=team["id"]: self.show_player_manager(team_id),
        )

        # Get player count
        player_count = len(team.get("players", []))

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.ListTile(
                            leading=ft.Icon(ft.icons.GROUP),
                            title=ft.Text(team["name"], weight=ft.FontWeight.BOLD),
                            subtitle=ft.Text(team["city"]) if team["city"] else None,
                            trailing=delete_btn,
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text(f"Players: {player_count}"),
                                    manage_players_btn,
                                ],
                                spacing=10,
                            ),
                            padding=ft.padding.only(left=10, right=10, bottom=10),
                        ),
                    ]
                ),
                padding=10,
            )
        )

    def delete_team(self, team_id: str):
        """Delete a team"""
        # Get team data before deletion to handle player cleanup
        team = self.team_repository.find_by_id(team_id)
        if team:
            # Delete all players first
            for player_id in team.get("players", []):
                self.player_repository.delete(player_id)

            # Delete the team
            if self.team_repository.delete(team_id):
                # Refresh the team list
                self.load_teams()
            else:
                self.show_error("Failed to delete team")
        else:
            self.show_error("Team not found")

    def show_error(self, message: str):
        """Show error message"""
        self.page.show_snack_bar(
            ft.SnackBar(content=ft.Text(message), bgcolor=ft.colors.ERROR)
        )
