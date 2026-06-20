import tkinter as tk
from config import *


class GameResult(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg_color)
        self.controller = controller

    def refresh(self, s1=None, s2=None):
        lang = self.controller.current_lang
        texts = LANGUAGES[lang]
        bg = self.controller.bg_color
        accent = THEME.get(bg.upper(), "#3B82F6")
        mode = self.controller.game_mode.get()
        if s1 is None or s2 is None:
            try:
                game_screen = self.controller.frames["GameScreen"]
                s1 = game_screen.logic.scores[1]
                s2 = game_screen.logic.scores[2]
            except (AttributeError, KeyError):
                return  # Ничего не рисуется, если игры не было
        # Очистка
        for widget in self.winfo_children():
            widget.destroy()

        # Определение победителя
        p1_name = texts["player1"]
        p2_name = texts["bot"] if mode == "bot" else texts["player2"]

        if s1 > s2:
            winner_text = f"{p1_name} {texts['wins']}"
            winner_color = accent
        elif s2 > s1:
            winner_text = f"{p2_name} {texts['wins']}"
            winner_color = accent
        else:
            winner_text = texts["draw"]
            winner_color = accent

        self.config(bg=bg)

        # Центральная карточка
        card = tk.Frame(self, bg="white", padx=50, pady=50, relief="flat", highlightthickness=1,highlightbackground="#E2E8F0")
        card.place(relx=0.5, rely=0.5, anchor="center", width=550)

        # Текст результата
        tk.Label(card, text=texts.get("result_title", ""), font=("Helvetica", 20, "bold"),bg="white", fg="#94A3B8").pack(pady=(0, 5))
        tk.Label(card, text=winner_text, font=("Helvetica", 28, "bold"),bg="white", fg=winner_color).pack(pady=(0, 10))

        # Блок счета
        score_frame = tk.Frame(card, bg="white")
        score_frame.pack(pady=(0, 40))
        self._create_score_box(score_frame, s1, p1_name, "#3B82F6")
        self._create_score_box(score_frame, s2, p2_name, "#EF4444")

        # Кнопки
        btn_new = tk.Button(card, text=texts["new_game"], font=("Helvetica", 12, "bold"),bg=accent, fg="white", relief="flat", width=20, pady=12, cursor="hand2",
                            command=lambda: self.controller.show_frame("GameScreen"))
        btn_new.pack(side="left", padx=15)

        btn_menu = tk.Button(card, text=texts["main_menu"], font=("Helvetica", 12, "bold"),bg="#F1F5F9", fg="#475569", relief="flat", width=20, pady=12, cursor="hand2",
                            command=lambda: self.controller.show_frame("MainMenu"))
        btn_menu.pack(side="left", padx=17)

    def _create_score_box(self, parent, score, label, color):
        box = tk.Frame(parent, bg="#F8FAFC", padx=30, pady=15)
        box.pack(side="left", padx=15)
        tk.Label(box, text=str(score), font=("Helvetica", 32, "bold"), bg="#F8FAFC", fg="#1E293B").pack()
        tk.Label(box, text=label, font=("Helvetica", 10, "bold"), bg="#F8FAFC", fg=color).pack()

