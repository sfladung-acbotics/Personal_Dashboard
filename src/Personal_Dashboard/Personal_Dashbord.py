import sys
import numpy as np


from PySide6.QtCore import Qt, QTimer, SIGNAL
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QFileDialog,
    QLabel,
    QMainWindow,
    QMessageBox,
    QScrollArea,
    QSizePolicy,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QSlider,
    QFrame,
    QStackedWidget,
    QTextEdit,
    QPushButton,
    QLineEdit,
)
from PySide6.QtGui import (
    QColorSpace,
    QGuiApplication,
    QImageReader,
    QImageWriter,
    QKeySequence,
    QPalette,
    QPainter,
    QPixmap,
    QImage,
    QFont,
)


class MainPane(QFrame):

    def build(self):
        pass


class Personal_Dashboard(QMainWindow):
    def __init__(self, app, model, parent=None):
        self.app = app
        super().__init__(parent)
        self.running = True
        self.model = model

    def build(self):
        self.setWindowTitle("Personal Dashboard")

        self.stack = QStackedWidget()
        self.main_panel = MainPane(self.model)
        self.main_panel.build()

        self.video_panel = QWidget()
        self.stack.addWidget(self.main_panel)
        self.setCentralWidget(self.stack)
        self.show()

    def keyPressEvent(self, event):
        if self.model is not None:
            key = event.key()
            if key in [ord("a"), ord("A")]:
                self.cycle_panels()

    def cycle_panels(self):
        ind = self.stack.currentIndex()
        ind = (ind + 1) % self.stack.count()
        self.stack.setCurrentIndex(ind)

    @classmethod
    def create(cls, model):
        # QApplication.shutdown()
        if not QApplication.instance():
            app = QApplication(sys.argv)
        else:
            app = QApplication.instance()
        app.setFont(QFont("Helvetica [Cronyx]", 18))
        gui = cls(app, model)
        gui.build()
        return gui

    def exec(self):
        self.app.exec()


if __name__ == "__main__":
    model = None
    gui = Personal_Dashboard.create(model=model)
    gui.exec()
    model.stop()
    sys.exit()
