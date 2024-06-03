from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox
from ui_design import Ui_MainWindow
import sys, os

class MW(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.show()

    def my_slot(self):
        start = self.textEdit.toPlainText()
        exec(start)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mwd = MW()
    sys.exit(app.exec())
