from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QItemDelegate, QStyleOptionViewItem


class MyDelegate(QItemDelegate):
    def __init__(self, parent=None, *args):
        QItemDelegate.__init__(self, parent, *args)

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, idx: QModelIndex):
        painter.save()
        self.parent().on_item_paint(idx, painter, option)
        painter.restore()