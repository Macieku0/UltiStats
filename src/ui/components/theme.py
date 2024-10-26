"""
This file contains the implementation of the theme switch button
"""

import flet as ft


def create_theme_switch(page: ft.Page) -> ft.IconButton:
    """
    Create a theme switch button that toggles between light and dark mode

    Args:
        page (ft.Page): The current page instance

    Returns:
        ft.IconButton: The theme switch button
    """

    def toggle_theme(e):
        page.theme_mode = (
            ft.ThemeMode.LIGHT
            if page.theme_mode == ft.ThemeMode.DARK
            else ft.ThemeMode.DARK
        )
        # Update icon and tooltip
        theme_icon_button.icon = (
            ft.icons.DARK_MODE
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.icons.LIGHT_MODE
        )
        theme_icon_button.tooltip = (
            "Switch to dark theme"
            if page.theme_mode == ft.ThemeMode.LIGHT
            else "Switch to light theme"
        )
        page.update()

    theme_icon_button = ft.IconButton(
        icon=ft.icons.DARK_MODE,
        tooltip="Switch to dark theme",
        on_click=toggle_theme,
    )
    return theme_icon_button
