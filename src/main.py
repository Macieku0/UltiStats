import flet as ft


class UI:
    """
    Application for Ultimate Frisbee statistics gathering.

    Well designed user interface is crucial part of application due to high dynamics of the game.
    It is very important to have easy to use and intuitive interface to gather data as fast as possible.
    """

    def __init__(self, page: ft.Page):
        self.page: ft.Page = page
        self.page.title = "Ultimate Stats"
        self.page.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        # Add theme support
        self.page.theme_mode = ft.ThemeMode.LIGHT

        # Create theme switch
        self.theme_switch = self.create_theme_switch()

        # Create app bar with theme switch
        self.app_bar = ft.AppBar(
            title=ft.Text(value="Ultimate Stats", size=24, weight=ft.FontWeight.BOLD),
            center_title=True,
            actions=[self.theme_switch],
        )
        self.page.appbar = self.app_bar

        # Style constants
        self.CIRCLE_SIZE = 60
        self.CIRCLE_BORDER_RADIUS: float = self.CIRCLE_SIZE / 2

        # State variables
        self.player_numbers: list[int] = []
        self.initial_player_number: int | None = None
        self.draggable_player: None | ft.Draggable = None

        # Initialize the first view
        self.show_number_input()

    def create_theme_switch(self):
        """
        Create a theme switch button
        """

        def toggle_theme(e):
            self.page.theme_mode = (
                ft.ThemeMode.LIGHT
                if self.page.theme_mode == ft.ThemeMode.DARK
                else ft.ThemeMode.DARK
            )
            # Update icon and tooltip
            theme_icon_button.icon = (
                ft.icons.DARK_MODE
                if self.page.theme_mode == ft.ThemeMode.LIGHT
                else ft.icons.LIGHT_MODE
            )
            theme_icon_button.tooltip = (
                "Switch to dark theme"
                if self.page.theme_mode == ft.ThemeMode.LIGHT
                else "Switch to light theme"
            )
            self.page.update()

        theme_icon_button = ft.IconButton(
            icon=ft.icons.DARK_MODE,
            tooltip="Switch to dark theme",
            on_click=toggle_theme,
        )
        return theme_icon_button

    def create_player_circle(self, number: int, is_draggable: bool = False):
        """Create a circular container for player number"""
        return ft.Container(
            content=ft.Text(str(number), size=20, weight=ft.FontWeight.BOLD),
            width=self.CIRCLE_SIZE,
            height=self.CIRCLE_SIZE,
            bgcolor=ft.colors.BLUE_200,
            border_radius=self.CIRCLE_BORDER_RADIUS,
            alignment=ft.alignment.center,
            data=number,  # Store the number as data for reference
        )

    def validate_player_numbers(self, e):
        """
        Validate player numbers and move to initial player selection
        """
        try:
            # Get numbers from text fields
            numbers: list[int] = [int(field.value) for field in self.number_fields]
            # Check if numbers are unique
            if len(set(numbers)) != 5:
                raise ValueError("Numbers must be unique!")
            # Store player numbers
            self.player_numbers = numbers
            # Clear main view and show initial player selection
            self.page.clean()
            self.pull_section()
        except ValueError as ve:
            self.error_text.value = f"{ve} Please enter valid unique numbers"
            self.page.update()

    def pull_section(self):
        """
        Show the view for selecting player that caches/lifts the pull
        User needs to fill additional information about the pull:
        - If pull fall in bounds or not
        - If pull fall in bounds, if it was caught or lifted from the ground
        - If pull fall out of bounds, if brick was called or not
        - Initial player - player that started the point by lifting/catching the pull
        """

        def on_pull_location_change(e):
            # Show/hide relevant options based on pull location
            if e.control.value == "in_bounds":
                catch_lift_row.visible = True
                brick_row.visible = False
            else:  # out_of_bounds
                catch_lift_row.visible = False
                brick_row.visible = True
            self.page.update()

        def on_player_selected(e):
            # Store selected player and pull information
            selected_player = e.control.data
            pull_data = {
                "pulling_player": selected_player,
                "pull_location": pull_location.value,
                "catch_or_lift": catch_lift.value
                if pull_location.value == "in_bounds"
                else None,
                "brick_called": brick_called.value
                if pull_location.value == "out_of_bounds"
                else None,
            }
            # Store pull data for later use
            self.pull_info = pull_data
            # Move to the next view (game view)
            self.page.clean()
            self.show_game_view(
                selected_player,
                [num for num in self.player_numbers if num != selected_player],
            )

        # Pull Location Radio Buttons
        pull_location = ft.RadioGroup(
            content=ft.Row(
                [
                    ft.Radio(value="in_bounds", label="In Bounds"),
                    ft.Radio(value="out_of_bounds", label="Out of Bounds"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            on_change=on_pull_location_change,
        )

        # Catch/Lift Options (initially hidden)
        catch_lift = ft.RadioGroup(
            content=ft.Row(
                [
                    ft.Radio(value="caught", label="Caught"),
                    ft.Radio(value="lifted", label="Lifted from ground"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        catch_lift_row = ft.Row(
            [ft.Text("Pull was: "), catch_lift],
            visible=False,
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # Brick Options (initially hidden)
        brick_called = ft.RadioGroup(
            content=ft.Row(
                [
                    ft.Radio(value="yes", label="Yes"),
                    ft.Radio(value="no", label="No"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        brick_row = ft.Row([ft.Text("Brick called? "), brick_called], visible=False)

        # Player Selection
        player_buttons: list[ft.ElevatedButton] = [
            ft.ElevatedButton(
                text=f"Player {num}",
                data=num,
                on_click=on_player_selected,
            )
            for num in self.player_numbers
        ]

        self.page.add(
            ft.Text("Start the point!", size=24, weight=ft.FontWeight.BOLD),
            ft.Container(height=20),  # Spacing
            ft.Text("Where did the pull land?", size=16),
            pull_location,
            ft.Container(height=10),  # Spacing
            catch_lift_row,
            brick_row,
            ft.Container(height=20),  # Spacing
            ft.Text("Select player who received the pull:", size=16),
            ft.Row(
                player_buttons,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10,
            ),
        )

    def select_initial_player(self, e):
        """
        Handle initial player selection and go to the standard view
        """
        self.initial_player_number = e.control.data
        other_players: list[int] = [
            num for num in self.player_numbers if num != self.initial_player_number
        ]
        self.page.clean()
        if self.initial_player_number is not None:
            self.show_game_view(
                initial_number=self.initial_player_number, other_numbers=other_players
            )
        else:
            self.pull_section()

    def drag_accept(self, e: ft.DragTargetAcceptEvent):
        """Handle drag and drop acceptance"""
        # Get the source and target containers
        if self.draggable_player is None:
            return
        source_content = self.draggable_player.content
        target_content = e.control.content

        # Swap the numbers
        temp_number = source_content.data
        source_content.content.value = str(target_content.data)
        source_content.data = target_content.data
        target_content.content.value = str(temp_number)
        target_content.data = temp_number

        # Update the draggable's content_feedback to match the new number
        self.draggable_player.content_feedback = self.create_player_circle(
            source_content.data
        )

        # Update the UI
        self.page.update()

    def show_game_view(self, initial_number: int, other_numbers: list):
        """
        Show the main game view with draggable and targets
        """
        # Create draggable source
        self.draggable_player = ft.Draggable(
            content=self.create_player_circle(number=initial_number),
            content_feedback=self.create_player_circle(number=initial_number),
        )

        # Create drag targets
        drag_targets: list[int] = []
        for player_num in other_numbers:
            drag_target = ft.DragTarget(
                content=self.create_player_circle(number=player_num),
                on_accept=self.drag_accept,
            )
            drag_targets.append(drag_target)

        # Create layout
        court_layout = ft.Column(
            [
                # First row with draggable player
                ft.Row(
                    [self.draggable_player],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                # Empty row for spacing
                ft.Container(height=40),
                # Row with drag targets
                ft.Row(
                    drag_targets,
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                    spacing=20,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )

        # Add layout to page
        self.page.add(court_layout)

    def show_number_input(self):
        """
        Show the initial number input view
        """
        self.error_text = ft.Text("", color=ft.colors.RED_400)
        self.number_fields = [
            ft.TextField(
                label=f"Player {i+1} number",
                width=200,
                keyboard_type=ft.KeyboardType.NUMBER,
            )
            for i in range(5)
        ]

        # Create initial view
        self.page.add(
            ft.Text("Enter Player Numbers", size=20, weight=ft.FontWeight.BOLD),
            ft.Column(
                self.number_fields, alignment=ft.MainAxisAlignment.CENTER, spacing=10
            ),
            self.error_text,
            ft.ElevatedButton("Continue", on_click=self.validate_player_numbers),
        )


def main(page: ft.Page):
    app: UI = UI(page=page)


if __name__ == "__main__":
    ft.app(target=main)
