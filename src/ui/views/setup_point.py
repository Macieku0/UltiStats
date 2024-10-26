import flet as ft
from src.ui.views.base_view import BaseView
from src.database.domain_repositories import TeamRepository, PlayerRepository


class SetupPointView(BaseView):
    """
    Setup point view - allows selection of players for the point and starting positions
    """

    def __init__(
        self,
        page: ft.Page,
        navigation_callback,
        game_id: str,
        team1_id: str,
        team2_id: str,
    ):
        self.game_id = game_id
        self.team1_id = team1_id
        self.team2_id = team2_id
        self.team_repo = TeamRepository()
        self.player_repo = PlayerRepository()

        # Initialize all dictionaries in __init__
        self.selected_players: dict[str, list] = {"team1": [], "team2": []}
        self.selected_lists: dict[str, None | ft.Column] = {
            "team1": None,
            "team2": None,
        }
        self.available_lists: dict[str, None | ft.Column] = {
            "team1": None,
            "team2": None,
        }
        self.all_players: dict[str, list] = {"team1": [], "team2": []}

        self.starting_offensive_team: str | None = None
        super().__init__(page, navigation_callback)

    def initialize_view(self):
        # Load teams
        self.team1 = self.team_repo.find_by_id(self.team1_id)
        self.team2 = self.team_repo.find_by_id(self.team2_id)
        if not self.team1 or not self.team2:
            self.show_error("Teams not found")
            return

        # Load players for each team
        self.all_players["team1"] = self.player_repo.find_by_team_id(
            team_id=self.team1_id
        )
        self.all_players["team2"] = self.player_repo.find_by_team_id(
            team_id=self.team2_id
        )

        # Create player selection sections for each team
        team1_selection = self.create_team_selection_section(
            self.team1, "team1", "Select Team 1 Players"
        )
        team2_selection = self.create_team_selection_section(
            self.team2, "team2", "Select Team 2 Players"
        )

        # Create offense/defense selection
        self.offense_selection = ft.RadioGroup(
            content=ft.Row(
                [
                    ft.Radio(
                        value="team1",
                        label=f"{self.team1.get('name')} starts on Offense",
                    ),
                    ft.Radio(
                        value="team2",
                        label=f"{self.team2.get('name')} starts on Offense",
                    ),
                ]
            ),
            on_change=self.handle_offense_selection,
        )

        # Continue button
        self.continue_button = ft.ElevatedButton(
            "Continue to Pull",
            on_click=lambda _: self.navigate_to(
                "pull_info",
                game_id=self.game_id,
                team1_id=self.team1_id,
                team2_id=self.team2_id,
                selected_players=self.selected_players,
                offensive_team=self.starting_offensive_team,
            ),
            disabled=True,
        )

        # Back button
        back_btn = ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            on_click=lambda _: self.navigate_to(
                "setup_point",
                game_id=self.game_id,
                team1_id=self.team1_id,
                team2_id=self.team2_id,
            ),
            tooltip="Back to main menu",
        )

        # Main content
        content = ft.Column(
            [
                ft.Row(
                    [
                        back_btn,
                        ft.Text("Setup Point", size=30, weight=ft.FontWeight.BOLD),
                    ]
                ),
                ft.Divider(),
                ft.Row(
                    [team1_selection, team2_selection],
                    spacing=20,
                ),
                ft.Divider(),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "Starting Positions", size=20, weight=ft.FontWeight.BOLD
                            ),
                            self.offense_selection,
                        ]
                    ),
                    padding=20,
                ),
                self.continue_button,
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        # Add content to page
        self.page.add(content)

    def create_team_selection_section(
        self, team, team_key: str, title: str
    ) -> ft.Container:
        # Create search field
        search_field = ft.TextField(
            label="Search players by name or number",
            on_change=lambda e: self.filter_players(e.control.value, team_key),
        )

        # Create list view for selected players
        self.selected_lists[team_key] = ft.Column([], spacing=5)

        # Create list view for available players
        self.available_lists[team_key] = ft.Column([], spacing=5)

        # Initial population of available players
        self.update_player_lists(team_key)

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(title, size=20, weight=ft.FontWeight.BOLD),
                    search_field,
                    ft.Text("Selected Players (max 5):", size=16),
                    self.selected_lists[team_key],
                    ft.Divider(),
                    ft.Text("Available Players:", size=16),
                    ft.Container(
                        content=self.available_lists[team_key],
                        height=200,
                    ),
                ]
            ),
            padding=20,
        )

    def filter_players(self, search_term: str, team_key: str):
        if not search_term:
            filtered_players = self.all_players[team_key]
        else:
            search_term = search_term.lower()
            filtered_players = [
                player
                for player in self.all_players[team_key]
                if search_term in player.get("name", "").lower()
                or search_term in str(player.get("number", "")).lower()
            ]

        self.update_player_lists(team_key, filtered_players)
        self.page.update()

    def update_player_lists(self, team_key: str, available_players=None):
        if available_players is None:
            available_players = self.all_players[team_key]

        # Update selected players list
        selected_controls = []
        for player_id in self.selected_players[team_key]:
            player = next(
                p for p in self.all_players[team_key] if p.get("id") == player_id
            )
            selected_controls.append(
                ft.Row(
                    [
                        ft.Text(
                            f"{player.get('name')} - #{player.get('number', 'N/A')}"
                        ),
                        ft.IconButton(
                            icon=ft.icons.REMOVE_CIRCLE,
                            data={"team": team_key, "player_id": player.get("id")},
                            on_click=self.remove_player,
                        ),
                    ]
                )
            )
        selected_column = self.selected_lists[team_key]
        if isinstance(selected_column, ft.Column):
            selected_column.controls = selected_controls
            self.selected_lists[team_key] = selected_column

        # Update available players list
        available_controls = []
        for player in available_players:
            if player.get("id") not in self.selected_players[team_key]:
                available_controls.append(
                    ft.TextButton(
                        text=f"{player.get('name')} - #{player.get('number', 'N/A')}",
                        data={"team": team_key, "player_id": player.get("id")},
                        on_click=self.add_player,
                    )
                )

        available_column = self.available_lists[team_key]
        if isinstance(available_column, ft.Column):
            available_column.controls = available_controls
            self.available_lists[team_key] = available_column

    def add_player(self, e):
        team = e.control.data["team"]
        player_id = e.control.data["player_id"]

        if len(self.selected_players[team]) < 5:
            self.selected_players[team].append(player_id)
            self.update_player_lists(team)
            self.update_continue_button()
            self.page.update()
        else:
            self.show_error("Maximum 5 players can be selected per team")

    def remove_player(self, e):
        team = e.control.data["team"]
        player_id = e.control.data["player_id"]

        self.selected_players[team].remove(player_id)
        self.update_player_lists(team)
        self.update_continue_button()
        self.page.update()

    def handle_offense_selection(self, e):
        self.starting_offensive_team = e.control.value
        self.update_continue_button()
        self.page.update()

    def update_continue_button(self):
        self.continue_button.disabled = not (
            len(self.selected_players["team1"]) == 5
            and len(self.selected_players["team2"]) == 5
            and self.starting_offensive_team is not None
        )
