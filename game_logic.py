import random


class GameLogic:
    def __init__(self, size):
        self.size = size
        self.n = size + 1  # точки, если 4х4 квадрата, то точек 5х5
        self.lines = {}  # {(x1, y1, x2, y2): player_id}
        self.scores = {1: 0, 2: 0}

    def get_all_possible_lines(self, offset, step):
        #Генерирует все возможные свободные линии на поле
        possible = []
        for r in range(self.n):
            for c in range(self.n):
                x, y = offset + c * step, offset + r * step
                # Горизонтальные (нельзя уйти влево или вправо от края)
                if c < self.n - 1:
                    l = (x, y, x + step, y)
                    if l not in self.lines: possible.append(l) # если линии нет, то точка свободна
                # Вертикальные (нельзя уйти вверх или вниз от края)
                if r < self.n - 1:
                    l = (x, y, x, y + step)
                    if l not in self.lines: possible.append(l)
        return possible

    def check_squares_closure(self, line, player_id, offset, step):
        # Проверяет, закрыл ли ход один или два квадрата
        x1, y1, x2, y2 = line
        closed_squares = []
        made_score = False

        # Определяем координаты верхних левых углов двух потенциальных квадратов
        if y1 == y2:  # Горизонтальная линия
            check_corners = [(x1, y1 - step), (x1, y1)]
        else:  # Вертикальная линия
            check_corners = [(x1 - step, y1), (x1, y1)]

        for sx, sy in check_corners:
            # Границы квадрата
            s1 = (sx, sy, sx + step, sy)  # верх
            s2 = (sx, sy + step, sx + step, sy + step)  # низ
            s3 = (sx, sy, sx, sy + step)  # лево
            s4 = (sx + step, sy, sx + step, sy + step)  # право

            # Если все 4 стороны заняты
            if all(s in self.lines for s in [s1, s2, s3, s4]):
                closed_squares.append((sx, sy))
                self.scores[player_id] += 1
                made_score = True

        return made_score, closed_squares

    def get_bot_move(self, difficulty, offset, step):
        available = self.get_all_possible_lines(offset, step)
        if not available: return None

        # Поиск хода, который приносит очко (Medium и Hard)
        if difficulty in ["medium", "hard"]:
            for line in available:
                self.lines[line] = 2  # Временно ставим
                is_score, _ = self.check_squares_closure(line, 2, offset, step)
                if is_score:
                    # Если ход закрыл квадрат, нам нужно отменить начисление очка,
                    self.scores[2] -= len(_)
                    del self.lines[line]
                    return line
                del self.lines[line]

        # Логика для Hard (не подставлять квадраты игроку)
        if difficulty == "hard":
            # Ищем ходы, после которых у игрока не появится возможности закрыть квадрат
            safe_moves = [l for l in available if not self._creates_opportunity(l, offset, step)]
            if safe_moves:
                return random.choice(safe_moves)

        # Случайный ход (Easy или если нет безопасных ходов)
        return random.choice(available)

    def _creates_opportunity(self, line, offset, step):
        # Проверяет, создаст ли этот ход третью стенку в каком-либо квадрате
        self.lines[line] = 2
        # Ищем, может ли игрок после этого хода закрыть какой-либо квадрат
        potential_lines = self.get_all_possible_lines(offset, step)
        can_player_score = False

        for next_l in potential_lines:
            self.lines[next_l] = 1
            is_score, _ = self.check_squares_closure(next_l, 1, offset, step)
            if is_score:
                self.scores[1] -= len(_)
                can_player_score = True
                del self.lines[next_l]
                break
            del self.lines[next_l]

        del self.lines[line]
        return can_player_score