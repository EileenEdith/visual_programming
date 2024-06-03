import sys
from PySide6.QtWidgets import (QApplication, 
                                         QMainWindow, QLabel,QWidget)
from PySide6.QtCore import Qt #enumerate type을 사용하기 위해

class MW(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle("Event Handling Ex")
        self.set_main_wnd()
        self.show()
        
    def set_main_wnd(self):
        label = QLabel(
            """<p>Press the <b>ESC</b> key
            to quit this program.</p>"""
        )
        self.setCentralWidget(label)
        
    def keyPressEvent(self, event): #호출하는 시점을 모름. escape 키가 눌러졌을때 호출(사용자가 선택)
        """Reimplement the key press event to close the
        window.""" #상속받아서 오버라이딩 하자
        if event.key() == Qt.Key.Key_Escape:
            #self.close()
            self.hide()
        elif event.key() == Qt.Key.Key_A:

            self.second_window = NW()
            self.second_window.show()
            
class NW(QWidget):
    def __init__(self):
        super().__init__()
        self.init_UI()
        
    def init_UI(self):
        self.setGeometry(100,100,300,200)
        self.setWindowTitle("second window")
        self.set_main_wnnd()
        self.show()
        
    def set_main_wnnd(self):
        label = QLabel(self)
        label.setText("Hello, World!")
        
    def keyPressEvent(self, event): #호출하는 시점을 모름. escape 키가 눌러졌을때 호출(사용자가 선택)
        """Reimplement the key press event to close the
        window.""" #상속받아서 오버라이딩 하자
        if event.key() == Qt.Key.Key_Space:
            self.close()
            
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MW()
    sys.exit(app.exec())
