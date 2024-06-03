import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtGui import QAction
from ui_design import Ui_MainWindow  

class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.initUI()

    def initUI(self):
        loadUIAction = QAction('Load UI', self)
        loadUIAction.setShortcut('Ctrl+L')
        loadUIAction.setStatusTip('Load UI from ui_design.py')
        loadUIAction.triggered.connect(self.loadUI)

        self.statusBar()

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&File')
        filemenu.addAction(loadUIAction)

        self.setWindowTitle('Menubar')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def loadUI(self):
        self.ui.setupUi(self)
        self.ui.textEdit.textChanged.connect(self.countCharacters)

    def countCharacters(self):
        text = self.ui.textEdit.toPlainText()
        char_count = len(text)
        self.statusBar().showMessage(f'Character count: {char_count}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec())
