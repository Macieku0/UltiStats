# This file contains the base class for all views in the application
import flet as ft
from typing import Callable


class BaseView:
    """Base class for all views in the application"""

    def __init__(self, page: ft.Page, navigation_callback: Callable):
        self.page = page
        self.navigate_to = navigation_callback
        self.initialize_view()

    def initialize_view(self):
        """Initialize the view - to be implemented by subclasses"""
        raise NotImplementedError

    def clean_up(self):
        """Clean up resources before view is destroyed"""
        pass

    def show_error(self, message: str):
        """Display error message to user"""
        self.page.add(ft.Text(message, color=ft.colors.RED_400))
        self.page.update()

    def show_loading(self, show: bool = True):
        """Show/hide loading indicator"""
        if show:
            self.page.add(ft.ProgressRing())
        self.page.update()
