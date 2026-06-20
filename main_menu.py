import tkinter as tk
from config import *


class MainMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg_color)
        self.controller = controller
        texts = LANGUAGES[self.controller.current_lang]

        # Кнопка Настройки
        self.btn_settings = tk.Button(self, text=texts["settings"], font=("Helvetica", 18),bg="white", relief="flat", highlightthickness=0,
                                      command=lambda: controller.show_frame("SettingsMenu"))
        self.btn_settings.place(relx=0.95, rely=0.15, anchor="ne")

        # Заголовок
        self.title_label = tk.Label(self, text=texts["main_title"], font=("Helvetica", 48, "bold"),bg=self.controller.bg_color, fg="#1C2536")
        self.title_label.pack(pady=(250, 50))

        # Кнопка Новая игра
        self.btn_play = tk.Button(self, text=texts["play"], font=("Helvetica", 18, "bold"),width=30, height=2, bg="white", relief="flat",highlightthickness=0,
                                  command=lambda: controller.show_frame("ModeMenu"))
        self.btn_play.pack(pady=10)

        # Кнопка Выход
        self.btn_exit = tk.Button(self, text=texts["exit"], font=("Helvetica", 15, "bold"),  width=20, height=2, bg="white", relief="flat",highlightthickness=0,
                                  command=lambda: controller.show_frame("ExitConfirmation"))
        self.btn_exit.pack(pady=10)

    def refresh(self):
        bg = self.controller.bg_color
        lang = self.controller.current_lang
        texts = LANGUAGES[lang]
        accent = THEME.get(bg, "#3B82F6")
        # Обновляем фон экрана и заголовка
        self.config(bg=bg)
        self.btn_play.config(bg=accent, fg="white")
        # Остальные элементы
        if hasattr(self, 'title_label'):
            self.title_label.config(bg=bg, text=texts["main_title"])
        # Обновляем тексты и цвета кнопок
        self.btn_play.config(text=texts["play"], bg=accent, fg="white")
        self.btn_settings.config(text=texts["settings"])
        self.btn_exit.config(text=texts["exit"])


