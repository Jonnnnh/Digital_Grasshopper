from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QItemDelegate, QStyleOptionViewItem


class MyDelegate(QItemDelegate):
    def __init__(self, parent=None, *args):
        super().__init__(parent, *args)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, idx: QModelIndex):
        painter.save()
        if hasattr(self.parent(), 'paint_game_cell'):
            self.parent().paint_game_cell(idx, painter, option)
        painter.restore()