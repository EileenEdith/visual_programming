import sys
from PySide6.QtWidgets import (QMainWindow, QApplication, QLabel, QPushButton, QLineEdit, QVBoxLayout, QRadioButton, QButtonGroup, QWidget)

class MW(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initialize_ui()
        
    def initialize_ui(self):
        self.setWindowTitle("joat")
        self.setup_main_wnd()
        self.show()
        
    def setup_main_wnd(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
              
        self.rb01 = QRadioButton('1. sleep')
        self.rb02 = QRadioButton('2. visual programming')
        self.rb03 = QRadioButton('3. die')
        
        lm = QVBoxLayout()
        lm.addWidget(QLabel('What is most important'))
        lm.addWidget(self.rb01)
        lm.addWidget(self.rb02)
        lm.addWidget(self.rb03)
        
        self.central_widget.setLayout(lm)
        self.bg = QButtonGroup(self)
        self.bg.addButton(self.rb01)
        self.bg.addButton(self.rb02)
        self.bg.addButton(self.rb03)
        
        self.bg.buttonClicked.connect(self.ck_click)  # 버튼 그룹의 버튼 클릭 시그널에 연결
    
    def ck_click(self, button):
        tmp = button.text()
        print(tmp)
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MW()
    sys.exit(app.exec())
