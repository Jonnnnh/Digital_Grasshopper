class GameCell:
    def __init__(self, block: bool = False, number: int = 0, step: bool = False, is_locked=False, is_active=False):
        self._block = block
        self._number = number
        self._step = step
        self._is_locked = is_locked
        self._is_active = is_active

    @property
    def block(self) -> bool:
        return self._block

    @property
    def number(self) -> int:
        return self._number

    @property
    def step(self) -> bool:
        return self._step

    @property
    def is_locked(self) -> bool:
        return self._is_locked

    @property
    def is_active(self) -> bool:
        return self._is_active
