import tkinter as tk
from config import *


class SettingsMenu(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg_color)
        self.controller = controller
        self.refresh()

    def refresh(self):
        # Очистка старых виджетов
        for widget in self.winfo_children():
            widget.destroy()

        # Настройка текущего фона и текстов
        bg_main = self.controller.bg_color
        accent = THEME.get(bg_main.upper(), "#3B82F6")
        self.configure(bg=bg_main)
        texts = LANGUAGES[self.controller.current_lang]

        # Кнопка Назад
        tk.Button(self, text=texts["back"], font=("Helvetica", 12, "bold"),bg="white", relief="flat", padx=15, pady=5,highlightthickness=0,
                  command=lambda: self.controller.show_frame("MainMenu")).place(relx=0.15, rely=0.05)

        card = tk.Frame(self, bg="white", padx=30, pady=30, relief="flat")
        card.place(relx=0.5, rely=0.5, anchor="center", width=450)

        # Язык
        tk.Label(card, text=texts["lang_label"], font=("Helvetica", 11, "bold"),bg="white", fg="#4B5563").pack(anchor="w", pady=(5, 5))
        lang_frame = tk.Frame(card, bg="white")
        lang_frame.pack(fill="x", pady=(0, 15))

        for lang in ["Russian", "English"]:
            is_active = self.controller.current_lang == lang
            btn = tk.Button(lang_frame, text=lang, font=("Helvetica", 10),
                            bg=accent if is_active else "#F1F5F9",
                            fg="white" if is_active else "#1E293B",
                            relief="flat", width=12, pady=8,
                            command=lambda l=lang: self.controller.change_language(l))
            btn.pack(side="left", padx=(0, 10))

        # Цветовая тема
        tk.Label(card, text=texts["theme_label"], font=("Helvetica", 11, "bold"),
                 bg="white", fg="#4B5563").pack(anchor="w", pady=(5, 5))
        theme_frame = tk.Frame(card, bg="white")
        theme_frame.pack(fill="x", pady=(0, 20))
        themes = [
            ("#F0F7FF", "Голубой", "Blue"),
            ("#E2E8F0", "Светло-серый", "Light Gray"),
            ("#E0F2F1", "Бирюзовый", "Teal")
        ]

        for color_hex, name_ru, name_en in themes:
            is_active = self.controller.bg_color.upper() == color_hex.upper()
            # название вывести на кнопку
            display_name = name_ru if self.controller.current_lang == "Russian" else name_en
            # Кнопки выбора цвета с текстом
            btn = tk.Button(theme_frame, text=display_name, font=("Helvetica", 9),
                            bg=color_hex, fg="#1E293B",
                            relief="flat", width=14, pady=10,
                            highlightbackground=accent if is_active else "#E2E8F0",
                            highlightthickness=2,
                            command=lambda c=color_hex: self.controller.change_theme(c))
            btn.pack(side="left", padx=(0, 10))

        # Правила игры
        tk.Label(card, text=texts["about"], font=("Helvetica", 11, "bold"),bg="white", fg="#4B5563").pack(anchor="w", pady=(10, 5))
        # Текст описания
        desc_label = tk.Label(card, text=texts["desc"], font=("Helvetica", 12, "bold"),bg="#F8FAFC", fg="#475569", wraplength=380,
                              justify="left", padx=15, pady=15)
        desc_label.pack(fill="x")