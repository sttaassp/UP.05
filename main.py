import tkinter as tk

from config import LANGUAGES, BG_COLOR
from main_menu import MainMenu
from settings_menu import SettingsMenu
from exit_confirmation import ExitConfirmation
from mode_menu import ModeMenu
from difficulty_menu import DifficultyMenu
from size_menu import SizeMenu
from game_screen import GameScreen
from game_result import GameResult

class SticksGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Палочки")
        self.attributes("-fullscreen", True)
        self.bind("<Escape>", lambda e: self.attributes("-fullscreen", False))
        self.current_lang = "Russian"
        self.bg_color = BG_COLOR
        self.game_mode = tk.StringVar(value="friend")
        self.game_size = tk.StringVar(value="4x4")
        self.game_diff = tk.StringVar(value="medium")

        # главный контейнера
        self.container = tk.Frame(self, bg=self.bg_color)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Регистрация и создание всех экранов
        self.frames = {}
        for F in (MainMenu, SettingsMenu, ModeMenu, DifficultyMenu, ExitConfirmation, SizeMenu, GameScreen, GameResult):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("MainMenu")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if hasattr(frame, "refresh"):
            frame.refresh()
        # Запуск игры
        if page_name == "GameScreen":
            frame.start_game()
        frame.tkraise()

    def change_language(self, lang_code):
        self.current_lang = lang_code
        self.refresh_all_frames()

    def change_theme(self, color_hex):
        self.bg_color = color_hex.upper()
        self.container.config(bg=self.bg_color)
        self.refresh_all_frames()

    # Обновляет визуальное состояние всех окон
    def refresh_all_frames(self):
        for frame in self.frames.values():
            if hasattr(frame, "refresh"):
                frame.refresh()

if __name__ == "__main__":
    app = SticksGame()
    app.mainloop()