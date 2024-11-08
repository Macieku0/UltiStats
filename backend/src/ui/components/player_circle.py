"""
This module contains functions and classes to create player circles for visualizing player numbers.
"""

import flet as ft
from typing import Optional, Callable


def create_player_circle(
    number: int,
    size: int = 60,
    bgcolor: str = ft.colors.BLUE_200,
    on_click: Optional[Callable] = None,
    is_selected: bool = False,
    is_draggable: bool = False,
) -> ft.Container:
    """
    Create a circular container for player number visualization.

    Args:
        number (int): Player's number
        size (int): Size of the circle in pixels
        bgcolor (str): Background color of the circle
        on_click (Optional[Callable]): Click handler function
        is_selected (bool): Whether the player is currently selected
        is_draggable (bool): Whether the circle should be draggable

    Returns:
        ft.Container: A container with the player number in a circle
    """
    border_radius = size / 2

    # Create the basic circle container
    circle = ft.Container(
        content=ft.Text(
            str(number),
            size=size * 0.33,  # Text size proportional to circle size
            weight=ft.FontWeight.BOLD,
            color=ft.colors.BLACK if not is_selected else ft.colors.WHITE,
        ),
        width=size,
        height=size,
        bgcolor=bgcolor if not is_selected else ft.colors.BLUE_700,
        border_radius=border_radius,
        alignment=ft.alignment.center,
        on_click=on_click,
        data=number,  # Store the number as data for reference
        animate=ft.animation.Animation(
            300, "easeOut"
        ),  # Smooth animation for state changes
    )

    # Add hover effect
    if on_click:
        circle.ink = True
        circle.tooltip = f"Player {number}"

    # Add border for selected state
    if is_selected:
        circle.border = ft.border.all(2, ft.colors.BLUE_900)

    # Add shadow for depth
    circle.shadow = ft.BoxShadow(
        spread_radius=1, blur_radius=4, color=ft.colors.BLACK26, offset=ft.Offset(0, 2)
    )

    return circle


def create_draggable_player_circle(
    number: int,
    size: int = 60,
    bgcolor: str = ft.colors.BLUE_200,
    on_drag_start: Optional[Callable] = None,
    on_drag_end: Optional[Callable] = None,
) -> ft.Draggable:
    """
    Create a draggable player circle.

    Args:
        number (int): Player's number
        size (int): Size of the circle in pixels
        bgcolor (str): Background color of the circle
        on_drag_start (Optional[Callable]): Function to call when drag starts
        on_drag_end (Optional[Callable]): Function to call when drag ends

    Returns:
        ft.Draggable: A draggable container with the player number in a circle
    """
    # Create the basic circle
    circle = create_player_circle(number=number, size=size, bgcolor=bgcolor)

    # Wrap in a draggable container
    draggable = ft.Draggable(
        content=circle,
        content_feedback=create_player_circle(
            number=number,
            size=size,
            bgcolor=ft.colors.BLUE_400,  # Slightly different color for feedback
            is_selected=True,
        ),
        data=number,  # Store the number as data for reference
    )

    # Add drag callbacks if provided
    if on_drag_start:
        draggable.on_drag_start = on_drag_start
    if on_drag_end:
        draggable.on_drag_end = on_drag_end

    return draggable


class PlayerCircleGroup(ft.UserControl):
    """
    A group of player circles that can be arranged in different formations.
    """

    def __init__(
        self,
        numbers: list[int],
        size: int = 60,
        spacing: int = 10,
        formation: str = "horizontal",
        on_player_click: Optional[Callable] = None,
    ):
        super().__init__()
        self.numbers = numbers
        self.size = size
        self.spacing = spacing
        self.formation = formation
        self.on_player_click = on_player_click
        self.selected_number: int | None = None

    def build(self):
        """Build the group of player circles"""
        if self.formation == "horizontal":
            return ft.Row(
                [
                    create_player_circle(
                        number=number,
                        size=self.size,
                        on_click=lambda e: self._handle_click(e=e, number=number),
                        is_selected=number == self.selected_number,
                    )
                    for number in self.numbers
                ],
                spacing=self.spacing,
                alignment=ft.MainAxisAlignment.CENTER,
            )
        elif self.formation == "vertical":
            return ft.Column(
                [
                    create_player_circle(
                        number=number,
                        size=self.size,
                        on_click=lambda e: self._handle_click(e=e, number=number),
                        is_selected=number == self.selected_number,
                    )
                    for number in self.numbers
                ],
                spacing=self.spacing,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        elif self.formation == "stack":
            # Create a stacked formation (e.g., for offensive/defensive layouts)
            return ft.Stack(
                [
                    ft.Container(
                        create_player_circle(
                            number,
                            self.size,
                            on_click=lambda e: self._handle_click(e, number),
                            is_selected=number == self.selected_number,
                        ),
                        left=(index * (self.size + self.spacing)),
                        top=(index * (self.size + self.spacing) // 2),
                    )
                    for index, number in enumerate(self.numbers)
                ],
                width=(len(self.numbers) * (self.size + self.spacing)),
                height=((len(self.numbers) * (self.size + self.spacing)) // 2),
            )

    def _handle_click(self, e, number: int):
        """Handle click on a player circle"""
        self.selected_number = number if self.selected_number != number else None
        if self.on_player_click:
            self.on_player_click(number)
        self.update()
