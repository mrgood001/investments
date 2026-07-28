import sys
import tkinter as tk
from pathlib import Path
from tkinter import ttk


def resource_path(relative_path: str) -> Path:
    """Путь к ресурсу, рабочий и при запуске из исходников, и из PyInstaller-бандла."""
    base_path = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
    return base_path / relative_path


class BaseApp(tk.Tk):
    """Базовое окно приложения: тема + навигация между экранами.

    Наследники регистрируют свои экраны через register_screen()
    и решают, какой показать первым.
    """

    def __init__(self, title: str = "App", geometry: str = "600x500"):
        super().__init__()
        self.title(title)
        self.minsize(*map(int, geometry.replace("x", " ").split()))

        icon_path = resource_path("assets/icon.png")
        self.iconphoto(True, tk.PhotoImage(file=str(icon_path)))

        self.style = ttk.Style(self)
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.screens: dict[str, ttk.Frame] = {}
        self.current_screen: str | None = None

        self.apply_theme("system")

    def register_screen(self, name: str, screen: ttk.Frame) -> None:
        self.screens[name] = screen
        screen.grid(row=0, column=0, sticky="nsew", in_=self.container)

    def show_screen(self, name: str) -> None:
        if name not in self.screens:
            raise ValueError(f"Unknown screen: {name}")
        self.screens[name].tkraise()
        self.current_screen = name

    def apply_theme(self, theme: str) -> None:
        """theme: 'light', 'dark' или 'system'."""
        if theme == "system":
            theme = self._detect_system_theme()

        self.style.theme_use("clam")
        if theme == "dark":
            self.style.configure(".", background="#2b2b2b", foreground="#e0e0e0")
        else:
            self.style.configure(".", background="#f5f5f5", foreground="#000000")

    def _detect_system_theme(self) -> str:
        # TODO: платформозависимое определение (GTK/реестр Windows и т.д.)
        return "light"
