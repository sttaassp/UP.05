import tkinter as tk
from config import *
from game_logic import GameLogic

class GameScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg_color)
        self.controller = controller
        texts = LANGUAGES[self.controller.current_lang]

        # Настройки поля
        self.step = 60
        self.offset = 30
        self.turn = 1

        # Интерфейс
        self.header = tk.Frame(self, bg=controller.bg_color)
        self.header.pack(pady=30)

        # Блок Игрок 1
        self.p1_frame = tk.Frame(self.header, bg="white", padx=20, pady=10, highlightthickness=2,highlightbackground="#3B82F6", bd=0)
        self.p1_frame.pack(side="left", padx=20)

        self.p1_name_label = tk.Label(self.p1_frame, text="", font=("Helvetica", 12, "bold"), bg="white", fg="#3B82F6")
        self.p1_name_label.pack(side="left")

        self.p1_score_label = tk.Label(self.p1_frame, text="0", font=("Helvetica", 16, "bold"), bg="white",fg="#1E293B")
        self.p1_score_label.pack(side="left", padx=(15, 0))

        # Чей ход
        self.status_label = tk.Label(self.header, text="Ход игрока 1", font=("Helvetica", 12), bg=controller.bg_color,fg="#64748B")
        self.status_label.pack(side="left", padx=40)

        # Блок Игрок 2
        self.p2_frame = tk.Frame(self.header, bg="white", padx=20, pady=10, highlightthickness=1,highlightbackground="#E2E8F0", bd=0)
        self.p2_frame.pack(side="left", padx=20)

        self.p2_name_label = tk.Label(self.p2_frame, text="", font=("Helvetica", 12, "bold"), bg="white", fg="#EF4444")
        self.p2_name_label.pack(side="left")

        self.p2_score_label = tk.Label(self.p2_frame, text="0", font=("Helvetica", 16, "bold"), bg="white",fg="#1E293B")
        self.p2_score_label.pack(side="left", padx=(15, 0))

        # Холст
        self.canvas_container = tk.Frame(self, bg="white", padx=25, pady=25, highlightthickness=1,highlightbackground="#E2E8F0")
        self.canvas_container.pack(expand=True)
        self.canvas = tk.Canvas(self.canvas_container, bg="white", highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._on_canvas_click)

        # Кнопки
        self.footer = tk.Frame(self, bg=controller.bg_color)
        self.footer.pack(pady=40)
        self.btn_new_game = tk.Button(self.footer, text=texts["new_game"], font=("Helvetica", 13, "bold"), bg="white", width=20, pady=15, relief="flat",
                                      highlightthickness=0, command=self.start_game, cursor="hand2")
        self.btn_new_game.pack(side="left", padx=10)

        self.btn_menu = tk.Button(self.footer, text=texts["main_menu"], font=("Helvetica", 13, "bold"), bg="white", width=20, pady=15, relief="flat",
                                  highlightthickness=0, command=lambda: controller.show_frame("MainMenu"),cursor="hand2")
        self.btn_menu.pack(side="left", padx=10)

    def refresh(self):
        bg = self.controller.bg_color
        lang = self.controller.current_lang
        texts = LANGUAGES[lang]
        accent = THEME.get(bg.upper(), "#3B82F6")

        # Обновляем фоны
        self.config(bg=bg)
        self.header.config(bg=bg)
        self.footer.config(bg=bg)
        self.status_label.config(bg=bg)

        # Обновляем тексты кнопок
        self.btn_new_game.config(text=texts["new_game"])
        self.btn_menu.config(text=texts["main_menu"])

        # Обновляем имена игроков в зависимости от языка
        p1_name = "Игрок 1" if lang == "Russian" else "Player 1"
        self.p1_name_label.config(text=f"● {p1_name}")
        mode = self.controller.game_mode.get()
        if mode == "bot":
            p2_name = "Бот" if lang == "Russian" else "Bot"
        else:
            p2_name = "Игрок 2" if lang == "Russian" else "Player 2"
        self.p2_name_label.config(text=f"● {p2_name}")
        self._update_ui()

    def start_game(self):
        #Запуск или перезапуск игры
        size_str = self.controller.game_size.get()
        squares_count = int(size_str.split('x')[0])

        self.logic = GameLogic(squares_count)
        self.turn = 1

        n = squares_count + 1
        canvas_size = (n - 1) * self.step + self.offset * 2
        self.canvas.config(width=canvas_size, height=canvas_size)

        self._draw_grid(n)
        self.refresh()

    def _draw_grid(self, n):
        self.canvas.delete("all")
        for r in range(n):
            for c in range(n):
                x = self.offset + c * self.step
                y = self.offset + r * self.step
                self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3,fill="#64748B", outline="")

    def _on_canvas_click(self, event):
        # Блокируем клик, если сейчас ход бота
        if self.turn == 2 and self.controller.game_mode.get() == "bot":
            return

        line = self._find_closest_line(event.x, event.y)
        if line and line not in self.logic.lines:
            self._make_move(line)
            print(f"Поставили линию: {line}")

    def _find_closest_line(self, x, y):
        # Поиск ближайшей линии
        threshold = 15
        best_line = None
        min_dist = threshold

        # Берем все возможные линии поля (горизонтальные и вертикальные)
        for r in range(self.logic.n):
            for c in range(self.logic.n):
                lx, ly = self.offset + c * self.step, self.offset + r * self.step

                # Горизонтальная от (lx, ly) вправо
                if c < self.logic.n - 1:
                    l = (lx, ly, lx + self.step, ly)
                    dist = abs(y - ly) if lx <= x <= lx + self.step else 100
                    if dist < min_dist:
                        min_dist = dist
                        best_line = l

                # Вертикальная от (lx, ly) вниз
                if r < self.logic.n - 1:
                    l = (lx, ly, lx, ly + self.step)
                    dist = abs(x - lx) if ly <= y <= ly + self.step else 100
                    if dist < min_dist:
                        min_dist = dist
                        best_line = l
        return best_line

    def _make_move(self, line):
        # Логика
        self.logic.lines[line] = self.turn

        # Отрисовка линии
        color = "#3B82F6" if self.turn == 1 else "#EF4444"
        self.canvas.create_line(line, fill=color, width=4, capstyle="round")

        # Проверка квадратов
        made_score, closed_sqs = self.logic.check_squares_closure(line, self.turn, self.offset, self.step)

        #Закраска квадратов
        for sx, sy in closed_sqs:
            fill_color = "#DBEAFE" if self.turn == 1 else "#FEE2E2"
            self.canvas.create_rectangle(sx + 4, sy + 4, sx + self.step - 4, sy + self.step - 4, fill=fill_color, outline="")

        # Смена хода
        if not made_score:
            self.turn = 2 if self.turn == 1 else 1
        self._update_ui()
        total_possible = 2 * self.logic.size * (self.logic.size + 1)
        if len(self.logic.lines) == total_possible:
            res_frame = self.controller.frames["GameResult"]
            res_frame.refresh(self.logic.scores[1], self.logic.scores[2])
            self.controller.show_frame("GameResult")
            self.after(500, self._show_final_results)
            return
        # Бот
        if self.turn == 2 and self.controller.game_mode.get() == "bot":
            self.after(600, self._bot_turn_logic)

    def _bot_turn_logic(self):
        diff = self.controller.game_diff.get()
        move = self.logic.get_bot_move(diff, self.offset, self.step)
        if move:
            self._make_move(move)

    def _update_ui(self):
        if not hasattr(self, 'logic'):
            return
        lang = self.controller.current_lang
        texts = LANGUAGES[lang]

        self.p1_score_label.config(text=str(self.logic.scores[1]))
        self.p2_score_label.config(text=str(self.logic.scores[2]))

        if self.turn == 1:
            self.p1_frame.config(highlightbackground="#3B82F6", highlightthickness=2)
            self.p2_frame.config(highlightbackground="#E2E8F0", highlightthickness=1)
            self.status_label.config(text=texts["turn_p1"])
        else:
            self.p2_frame.config(highlightbackground="#EF4444", highlightthickness=2)
            self.p1_frame.config(highlightbackground="#E2E8F0", highlightthickness=1)

            if self.controller.game_mode.get() == "bot":
                self.status_label.config(text=texts["turn_bot"])
            else:
                self.status_label.config(text=texts["turn_p2"])

    def _show_final_results(self):
        res_frame = self.controller.frames["GameResult"]
        # Передаем актуальный счет в экран результатов
        res_frame.refresh(self.logic.scores[1], self.logic.scores[2])
        self.controller.show_frame("GameResult")