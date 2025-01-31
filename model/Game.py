from model.GameState import GameState
from model.GameCell import GameCell
from model.Utils import Utils


class Game:
    def __init__(self, start_level: int):
        self._state = None
        self._row_count = 0
        self._col_count = 0
        self._field = []
        self._current_level = start_level
        self.new_game()
        self._current_cell = None
        self._current_cell_row = None
        self._current_cell_col = None
        self._steps = []

    def new_game(self) -> None:
        self.init_game_field()
        self._state = GameState.PLAYING

    @property
    def row_count(self) -> int:
        return self._row_count

    @property
    def col_count(self) -> int:
        return self._col_count

    @property
    def field(self) -> list:
        return self._field

    @property
    def state(self) -> GameState:
        return self._state

    @property
    def current_level(self) -> int:
        return self._current_level

    @property
    def has_moves_left(self) -> bool:
        for row in self._field:
            for cell in row:
                if cell.block and not cell.is_locked:
                    return True
        return False

    @property
    def is_completed(self) -> bool:
        for row in self._field:
            for cell in row:
                if not cell.is_locked:
                    return False
        return True

    def init_game_field(self):
        level = Utils.read_int_multy_array_form_file(self._current_level)
        self._col_count, self._row_count = len(level[0]), len(level)
        self._field = [[GameCell() for _ in range(self.col_count)] for _ in range(self.row_count)]

        for row in range(self.row_count):
            for col in range(self.col_count):
                cell_value = level[row][col]
                if cell_value in [1, 2, 3, 4]:
                    self._field[row][col] = GameCell(block=True, number=cell_value)

    def find_steps(self, row, column):
        step = self._current_cell.number
        directions = [(step, 0), (-step, 0), (0, step), (0, -step),
                      (step, step), (-step, -step), (step, -step), (-step, step)]
        for dr, dc in directions:
            self.check_neighbor(row + dr, column + dc)

    def check_neighbor(self, row, column):
        if 0 <= row < self._row_count and 0 <= column < self._col_count:
            cell = self._field[row][column]
            if not cell.block and not cell.step:
                cell._step = True
                self._steps.append([row, column])

    def swap_cells(self, row, col):
        for cell in self._steps:
            if cell[0] == row and cell[1] == col:
                self._steps.remove(cell)
        self._field[row][col] = self._current_cell
        self._field[row][col]._is_locked = True
        self._field[row][col]._is_active = False
        self._field[self._current_cell_row][self._current_cell_col] = GameCell()

    def clear_steps(self):
        for cell in self._steps:
            self._field[cell[0]][cell[1]] = GameCell()
        self._steps.clear()

    def on_button_click(self, row: int, col: int):
        if self.state != GameState.PLAYING:
            return

        if self._field[row][col].block and not self._field[row][col].is_locked:
            if self._current_cell is not None:
                self._current_cell._is_active = False
            self._current_cell = self._field[row][col]
            self._current_cell._is_active = True
            self.clear_steps()
            self._current_cell_row = row
            self._current_cell_col = col
            self.find_steps(row, col)

        if self._field[row][col].step:
            self.swap_cells(row, col)
            self.clear_steps()