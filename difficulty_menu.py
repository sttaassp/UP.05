import tkinter as tk
from config import *


class DifficultyMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg_color)
        self.controller = controller

        # Хранилища для управления виджетами
        self.option_frames = {}
        self.option_labels = {}
        self.selected_diff = tk.StringVar(value="")
        texts = LANGUAGES[self.controller.current_lang]

        # Кнопка Назад
        self.btn_back = tk.Button(self, text=texts["back"], font=("Helvetica", 12, "bold"),
                                  bg="white", relief="flat", padx=15, pady=5,
                                  highlightthickness=0,
                                  command=lambda: controller.show_frame("ModeMenu"))
        self.btn_back.place(relx=0.15, rely=0.05)

        # Центральный контейнер
        self.content = tk.Frame(self, bg=self.controller.bg_color)
        self.content.place(relx=0.5, rely=0.5, anchor="center")

        # Заголовок
        self.title_label = tk.Label(self.content, text=texts["diff_title"],
                                    font=("Helvetica", 36, "bold"),
                                    bg=self.controller.bg_color, fg="#1E293B")
        self.title_label.pack(pady=(0, 40))

        # Варианты сложности
        self._create_difficulty_option(texts["easy"], "easy")
        self._create_difficulty_option(texts["medium"], "medium")
        self._create_difficulty_option(texts["hard"], "hard")

        # 5. Кнопка Далее
        self.btn_next = tk.Button(self.content, text=texts["next"], font=("Helvetica", 13, "bold"),
                                  bg="#E5E7EB", fg="white", relief="flat",
                                  width=20, pady=15, state="disabled",
                                  highlightthickness=0, command=self._on_next)
        self.btn_next.pack(pady=(40, 0))

    def _create_difficulty_option(self, text, value):
        frame = tk.Frame(self.content, bg="white", highlightthickness=2,
                         highlightbackground="#F1F5F9", width=340, height=80)
        frame.pack_propagate(False)
        frame.pack()

        lbl = tk.Label(frame, text=text, font=("Helvetica", 14, "bold"), bg="white", fg="#1E293B")
        lbl.pack(expand=True)

        # Сохранение ссылок для обновления
        self.option_frames[value] = frame
        self.option_labels[value] = lbl

        def select(e=None):
            for f in self.option_frames.values():
                f.config(highlightbackground="#F1F5F9")

            accent = THEME.get(self.controller.bg_color.upper(), "#3B82F6")
            frame.config(highlightbackground=accent)

            self.selected_diff.set(value)
            self.btn_next.config(bg=accent, fg="white", state="normal", cursor="hand2")

        for widget in (frame, lbl):
            widget.bind("<Button-1>", select)
            widget.config(cursor="hand2")

    def refresh(self):
        # Обновление текстов и цветов
        bg = self.controller.bg_color
        texts = LANGUAGES[self.controller.current_lang]
        accent = THEME.get(bg.upper(), "#3B82F6")

        # Обновление фонов и текстов управления
        self.config(bg=bg)
        self.content.config(bg=bg)
        self.title_label.config(bg=bg, text=texts["diff_title"])
        self.btn_back.config(text=texts["back"])
        self.btn_next.config(text=texts["next"])

        # Обновление текстов
        self.option_labels["easy"].config(text=texts["easy"])
        self.option_labels["medium"].config(text=texts["medium"])
        self.option_labels["hard"].config(text=texts["hard"])

        # Обновление активных элементов
        active_val = self.selected_diff.get()
        if active_val:
            self.btn_next.config(bg=accent)
            self.option_frames[active_val].config(highlightbackground=accent)

    def _on_next(self):
        self.controller.game_diff.set(self.selected_diff.get())
        self.controller.show_frame("SizeMenu")

