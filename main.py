import flet as ft
from src.ui.app import UltiStatsApp


def main(page: ft.Page):
    app = UltiStatsApp(page)


if __name__ == "__main__":
    ft.app(target=main)
