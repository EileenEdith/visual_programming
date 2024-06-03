from PySide6.QtWidgets import QMainWindow,QApplication
from ds_uic import Ui_MainWindow 
import sys,os

class MW(QMainWindow, Ui_MainWindow): 
    def __init__(self):
        super().__init__()
        self.setupUi(self) 
        
        self.lineEdit.returnPressed.connect(self.my_slot)
        
        
        self.show()
        
    def my_slot(self):
        c_txt = self.lineEdit.text()
        self.label.setText(c_txt)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mwd = MW()
    sys.exit(app.exec())