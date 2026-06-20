import tkinter as tk
from config import *


class SizeMenu(tk.Frame):
    def __init__(self, parent, controller):
        # Используем динамический фон из контроллера
        super().__init__(parent, bg=controller.bg_color)
        self.controller = controller
        self.option_frames = {}
        self.option_labels = {}
        self.selected_size = tk.StringVar(value="")
        texts = LANGUAGES[self.controller.current_lang]

        # Кнопка Назад
        self.btn_back = tk.Button(self, text=texts["back"], font=("Helvetica", 12, "bold"), bg="white", relief="flat", padx=15, pady=5,
                             highlightthickness=0, command=lambda: controller.show_frame("DifficultyMenu"))
        self.btn_back.place(relx=0.15, rely=0.05)

        # Центральный контейнер для идеального выравнивания
        self.content = tk.Frame(self, bg=self.controller.bg_color)
        self.content.place(relx=0.5, rely=0.5, anchor="center")

        # 3. Заголовок (сохраняем в self для метода refresh)
        self.title_label = tk.Label(self.content, text=texts["size_title"], font=("Helvetica", 36, "bold"),bg=self.controller.bg_color, fg="#1E293B")
        self.title_label.pack(pady=(0, 40))

        # 4. Варианты размера поля
        self._create_size_option(texts["4x4"], "4x4")
        self._create_size_option(texts["6x6"], "6x6")
        self._create_size_option(texts["8x8"], "8x8")

        # 5. Кнопка Начать игру
        self.btn_start = tk.Button(self.content, text=texts["start_game"], font=("Helvetica", 13, "bold"), bg="#E5E7EB", fg="#9CA3AF", relief="flat", width=35, pady=15, state="disabled",
                                  highlightthickness=0, command=self._on_next)
        self.btn_start.pack(pady=(40, 0))

    def _create_size_option(self, text, value):
        frame = tk.Frame(self.content, bg="white", highlightthickness=2, highlightbackground="#F1F5F9", width=240, height=80)
        frame.pack_propagate(False)
        frame.pack()

        lbl = tk.Label(frame, text=text, font=("Helvetica", 14, "bold"), bg="white", fg="#1E293B")
        lbl.pack(expand=True)

        self.option_frames[value] = frame
        self.option_labels[value] = lbl

        def select(e=None):
            # Сбрасываем обводку у всех карточек
            for f in self.option_frames.values():
                f.config(highlightbackground="#F1F5F9")

            accent = THEME.get(self.controller.bg_color.upper(), "#3B82F6")
            frame.config(highlightbackground=accent)

            self.selected_size.set(value)
            self.btn_start.config(bg=accent, fg="white", state="normal")

        # Привязка клика ко всей карточке
        for widget in (frame, lbl):
            widget.bind("<Button-1>", select)
            widget.config(cursor="hand2")

    def refresh(self):
        # Упрощенное обновление текстов и цветов
        bg = self.controller.bg_color
        texts = LANGUAGES[self.controller.current_lang]
        accent = THEME.get(bg.upper(), "#3B82F6")

        self.config(bg=bg)
        self.content.config(bg=bg)
        self.title_label.config(bg=bg, text=texts["size_title"])
        self.btn_back.config(text=texts["back"])
        self.btn_start.config(text=texts["start_game"])

        # Обновление активных элементов
        active_val = self.selected_size.get()
        if active_val:
            self.btn_start.config(bg=accent)
            self.option_frames[active_val].config(highlightbackground=accent)

    def _on_back(self):
        """Логика возврата зависит от режима игры"""
        if self.controller.game_mode.get() == "bot":
            self.controller.show_frame("DifficultyMenu")
        else:
            self.controller.show_frame("ModeMenu")

    def _on_next(self):
        """Сохраняем размер и переходим к игре"""
        self.controller.game_size.set(self.selected_size.get())
        self.controller.show_frame("GameScreen")