from PyQt5.QtWidgets import QItemDelegate, QStyleOptionViewItem
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QModelIndex

class MyDelegate(QItemDelegate):
    def __init__(self, parent=None, *args):
        super(MyDelegate, self).__init__(parent, *args)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, idx: QModelIndex):
        painter.save()
        mainWindow = self.parent()
        if hasattr(mainWindow, 'paint_game_cell'):
            mainWindow.paint_game_cell(idx, painter, option)
        painter.restore()