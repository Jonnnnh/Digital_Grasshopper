from PyQt5 import QtWidgets, uic
import os
from PyQt5 import QtSvg
from PyQt5.QtGui import QMouseEvent, QPainter, QStandardItemModel
from PyQt5.QtWidgets import QMessageBox
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

        self.setFixedSize(720, 800)

        self.center_window()
        self.check_ui_components()
        self._images = {}
        images_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources/images')
        self.load_image_resources(images_dir)

        self.game = Game(1)
        self.initialize_game_view()

        self.pushButton.clicked.connect(lambda: self.start_new_game(self.spinBox.value()))
        self.pushButton_2.clicked.connect(self.close)

        self.tableView.mousePressEvent = self.handle_mouse_press_event

    def center_window(self):
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        self.move((screen.width() - self.width()) // 2, (screen.height() - self.height()) // 2)

    def check_ui_components(self):
        if not hasattr(self, 'tableView'):
            raise AttributeError("UI file does not contain 'tableView'.")

    def load_image_resources(self, images_dir):
        self._images = {os.path.splitext(f)[0]: QtSvg.QSvgRenderer(os.path.join(images_dir, f))
                        for f in os.listdir(images_dir)}

    def initialize_game_view(self):
        self.resize_game_table(self.game)
        self.tableView.setItemDelegate(MyDelegate(self))

    def resize_game_table(self, game: Game):
        model = QStandardItemModel(game.row_count, game.col_count)
        self.tableView.setModel(model)
        for row in range(game.row_count):
            self.tableView.setRowHeight(row, 114)
        for col in range(game.col_count):
            self.tableView.setColumnWidth(col, 119)
        self.refresh_game_view()

    def start_new_game(self, level):
        self.game = Game(level)
        self.initialize_game_view()

    def refresh_game_view(self):
        self.tableView.viewport().update()

    def paint_game_cell(self, e: QModelIndex, painter: QPainter, option):
        cell = self.game.field[e.row()][e.column()]
        img_name = 'default'
        if cell.block:
            img_name = f"{'active ' if cell.is_active else ''}{'locked ' if cell.is_locked else ''}{cell.number if cell.number > 0 else ''}".strip()
        elif cell.step:
            img_name = 'step'
        img = self._images.get(img_name, self._images['default'])
        img.render(painter, QRectF(option.rect))

    def handle_mouse_press_event(self, e: QMouseEvent):
        if e.button() in [Qt.LeftButton, Qt.RightButton]:
            idx = self.tableView.indexAt(e.pos())
            self.process_cell_click(idx)

    def process_cell_click(self, e: QModelIndex):
        self.game.on_button_click(e.row(), e.column())
        self.check_game_over()
        self.refresh_game_view()

    def check_game_over(self):
        if self.game.is_completed or not self.game.has_moves_left:
            message = "Game Over! Congratulations, you've completed the game!" if self.game.is_completed else "Game Over! No more moves left"
            QMessageBox.information(self, "Game Over", message)
