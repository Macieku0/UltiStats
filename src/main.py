import flet as ft


def main(page: ft.Page):
    page.title = "Ultimate Stats"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Initial player number and other players
    initial_player_number = 5
    other_players = [2, 31, 49, 17]

    # Style constants
    CIRCLE_SIZE = 60
    CIRCLE_BORDER_RADIUS = CIRCLE_SIZE / 2

    def create_player_circle(number: int, is_draggable: bool = False):
        """
        Create a circular container for player number
        """
        return ft.Container(
            content=ft.Text(str(number), size=20, weight=ft.FontWeight.BOLD),
            width=CIRCLE_SIZE,
            height=CIRCLE_SIZE,
            bgcolor=ft.colors.BLUE_200,
            border_radius=CIRCLE_BORDER_RADIUS,
            alignment=ft.alignment.center,
            data=number,  # Store the number as data for reference
        )

    # Create draggable source
    draggable_player = ft.Draggable(
        content=create_player_circle(initial_player_number),
        content_feedback=create_player_circle(initial_player_number),
    )

    # Function to handle drag accept
    def drag_accept(e: ft.DragTargetAcceptEvent):
        # Get the source and target containers
        source_content = draggable_player.content
        target_content = e.control.content

        # Swap the numbers
        temp_number = source_content.data
        source_content.content.value = str(target_content.data)
        source_content.data = target_content.data
        target_content.content.value = str(temp_number)
        target_content.data = temp_number

        # Update the UI
        page.update()

    # Create drag targets
    drag_targets = []
    for player_num in other_players:
        drag_target = ft.DragTarget(
            content=create_player_circle(player_num),
            on_accept=drag_accept,
        )
        drag_targets.append(drag_target)

    # Create layout
    court_layout = ft.Column(
        [
            # First row with draggable player
            ft.Row(
                [draggable_player],
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
    page.add(court_layout)


if __name__ == "__main__":
    ft.app(target=main)
