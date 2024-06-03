import sys, os

from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap, QKeyEvent
from PySide6.QtCore import Qt, Signal, QSize

class MW(QMainWindow):
    change_pixmap = Signal(int)

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.finished = False  # 상태를 관리하는 플래그

    def init_ui(self):
        self.fstr = os.path.dirname(os.path.abspath('/Users/bagseungbin/Desktop/coding/a'))
        self.setGeometry(100, 100, 200, 300)
        self.setWindowTitle("Custom Signals Ex")
        self.setup_main_wnd()
        self.show()

    def setup_main_wnd(self):
        self.idx = 0
        self.change_pixmap.connect(self.change_pixmap_handler)

        lm = QVBoxLayout()
        info_label = QLabel("<p>Press <i>+</i> key or <i>-</i> key to change image</p>")
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lm.addWidget(info_label)

        self.img_label = QLabel()
        pixmap = QPixmap(f"{self.fstr}/a/0.png")
        self.img_label.setPixmap(pixmap.scaled(QSize(180, 250), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lm.addWidget(self.img_label)

        container = QWidget()
        container.setLayout(lm)
        self.setCentralWidget(container)

    def keyPressEvent(self, event: QKeyEvent):
        if not self.finished:
            if event.key() == Qt.Key.Key_Plus:
                self.change_pixmap.emit(1)
            elif event.key() == Qt.Key.Key_Minus:
                self.change_pixmap.emit(-1)

            super().keyPressEvent(event)

    def change_pixmap_handler(self, offset):
        old_idx = self.idx
        self.idx = (self.idx + offset) % 10
        
        if self.idx == 0 and old_idx == 9:
            self.img_label.setText("끝났습니다")
            self.finished = True  # 키 입력을 더 이상 처리하지 않도록 설정
            return

        pixmap_path = f"{self.fstr}/a/{self.idx}.png"
        pixmap = QPixmap(pixmap_path)
        if pixmap.isNull():
            print(f"Failed to load image at path: {pixmap_path}")
        else:
            self.img_label.setPixmap(pixmap.scaled(QSize(180, 250), Qt.KeepAspectRatio, Qt.SmoothTransformation))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MW()
    sys.exit(app.exec())
