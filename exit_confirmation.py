import tkinter as tk
from config import *

class ExitConfirmation(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1E293B")
        self.controller = controller
        texts = LANGUAGES[self.controller.current_lang]

        card = tk.Frame(self, bg="white", padx=40, pady=40, relief="flat")
        card.place(relx=0.5, rely=0.5, anchor="center", width=420)

        self.label_question = tk.Label(card, text=texts["confirm_exit"], font=("Helvetica", 11, "bold"), bg="white", fg="#64748B")
        self.label_question.pack(pady=(0, 30))

        self.btn_frame = tk.Frame(card, bg="white")
        self.btn_frame.pack(fill="x")

        # Кнопка Отмена
        self.btn_cancel = tk.Button(self.btn_frame, text=texts["cancel"], font=("Helvetica", 10, "bold"),
                                    bg="#F1F5F9", fg="#475569", relief="flat",
                                    width=14, pady=12, cursor="hand2",
                                    command=lambda: controller.show_frame("MainMenu"))
        self.btn_cancel.pack(side="left", padx=10, expand=True)
        # Кнопка Подтвердить
        self.btn_confirm = tk.Button(self.btn_frame, text=texts["confirm"],font=("Helvetica", 10, "bold"),
                                     bg="#3B82F6", fg="white", relief="flat",
                                     width=14, pady=12, cursor="hand2",
                                     command=controller.quit)
        self.btn_confirm.pack(side="right", padx=10, expand=True)

    def refresh(self):
        texts = LANGUAGES[self.controller.current_lang]
        # Получаем цвет текущей темы
        current_bg = self.controller.bg_color.upper()
        accent = THEME.get(current_bg, "#3B82F6")

        # 1. Обновляем тексты из config.py
        self.label_question.config(text=texts["confirm_exit"])
        self.btn_cancel.config(text=texts["cancel"])
        self.btn_confirm.config(text=texts["confirm"])

        # 2. Красим кнопку подтверждения в цвет текущей темы
        self.btn_confirm.config(bg=accent)

        # 3. Визуальный отклик для кнопки отмены (чуть темнее фона карты)
        self.btn_cancel.config(bg="#F1F5F9")

    def _on_cancel(self):
        self.controller.show_frame("MainMenu")
