import sys
import os
from PySide6.QtWidgets import (QMainWindow, QApplication, QLabel, QWidget)

class MW(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setGeometry(200, 100, 400, 200)
        self.setup_main_wnd()
        self.show()
        
    def setup_main_wnd(self):
        hello_label = QLabel(self)
        hello_label.setText("Hello World")
        hello_label.move(150, 90)

        dir_label = QLabel(self)
        script_directory = os.path.dirname(os.path.abspath(__file__))
        dir_label.setText(script_directory)
        dir_label.move(150, 110)  

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MW()
    sys.exit(app.exec())
