from PyQt5 import QtWidgets, uic
import os

from PyQt5 import QtSvg
from PyQt5.QtGui import QMouseEvent, QPainter, QStandardItemModel
from PyQt5.QtWidgets import QStyleOptionViewItem, QHeaderView
from PyQt5.QtCore import QModelIndex, QRectF, Qt

from model.Game import Game
from gui.MyDelegate import MyDelegate


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        ui_path = 'C:/Users/Daria/PycharmProjects/DigitalGrasshopper/MainWindowUI.ui'
        if not os.path.exists(ui_path):
            raise FileNotFoundError(f"UI file '{ui_path}' does not exist")
        try:
            uic.loadUi(ui_path, self)
        except Exception as e:
            raise RuntimeError(f"Error loading UI file: {e}")
        uic.loadUi(ui_path, self)

        self.setFixedSize(720, 800)

        self.center_window()
        if not hasattr(self, 'tableView'):
            raise AttributeError(
                "UI file does not contain 'tableView'. Check if the UI file is correct and the path is valid.")

        images_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources/images')
        self._images = {
            os.path.splitext(f)[0]: QtSvg.QSvgRenderer(os.path.join(images_dir, f))
            for f in os.listdir(images_dir)
        }

        self.game = Game(1)
        self.game_resize(self.game)
        self.tableView.setItemDelegate(MyDelegate(self))
        self.pushButton.clicked.connect(self.new_game)

        def new_mouse_press_event(e: QMouseEvent) -> None:
            idx = self.tableView.indexAt(e.pos())
            self.on_item_clicked(idx, e)

        self.tableView.mousePressEvent = new_mouse_press_event

    def center_window(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        center_x = (screen.width() - self.width()) // 2
        center_y = (screen.height() - self.height()) // 2
        self.move(center_x, center_y)

    def game_resize(self, game: Game) -> None:
        if not isinstance(game, Game):
            raise TypeError("Argument 'game' must be an instance of Game")
        model = QStandardItemModel(game.row_count, game.col_count)
        self.tableView.setModel(model)
        row_height = 114
        column_width = 119
        for row in range(game.row_count):
            self.tableView.setRowHeight(row, row_height)
        for col in range(game.col_count):
            self.tableView.setColumnWidth(col, column_width)
        self.update_view()

    def new_game(self):
        try:
            self.game = Game(self.spinBox.value())
        except Exception as e:
            print(f"Error creating new game: {e}")
        else:
            self.update_view()

    def update_view(self):
        self.tableView.viewport().update()

    def on_item_paint(self, e: QModelIndex, painter: QPainter, option: QStyleOptionViewItem) -> None:
        cell = self.game.field[e.row()][e.column()]
        img = self._images['default']
        if cell.block:
            name = ""
            if cell.is_active:
                name = name + "active "
            if cell.is_locked:
                name = name + "locked "
            if cell.number == 1:
                name = name + "1"
            if cell.number == 2:
                name = name + "2"
            if cell.number == 3:
                name = name + "3"
            if cell.number == 4:
                name = name + "4"
            img = self._images[name]
        if cell.step:
            img = self._images['step']
        img.render(painter, QRectF(option.rect))

    def on_item_clicked(self, e: QModelIndex, me: QMouseEvent = None) -> None:
        if me.button() == Qt.LeftButton or me.button() == Qt.RightButton:
            self.game.on_button_click(e.row(), e.column())
            self.is_game_over()
        self.update_view()

    @staticmethod
    def is_game_over():
        pass
