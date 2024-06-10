import sys

from PySide6.QtWidgets import (
        QApplication, QMainWindow,
        QWidget, QPushButton, QLabel, QVBoxLayout,
        QLineEdit, QInputDialog)

class MW (QMainWindow):

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.show()

    def init_ui(self):
        layout = QVBoxLayout()
        tmp = QWidget()
        tmp.setLayout(layout)
        
        self.l_buttons = ['getText', 'getMultilineText', 'getInt']
        for idx, c_str in enumerate(self.l_buttons):
            button0 = QPushButton(c_str)
            button0.clicked.connect(self.slot00)
            layout.addWidget(button0)


        self.ret_label = QLabel() #사용자에게 받은 텍스트를 보여주기 위해
        layout.addWidget(self.ret_label)

        self.setCentralWidget(tmp)

    def slot00(self):
        print(self.sender())

        sender = self.sender() #<PySide6.QtWidgets.QPushButton(0x12a8f85b0) at 0x12aa36080>, self
        tmp_str = sender.text()
        is_ok = False

        if sender.text() == self.l_buttons[0]:
            ret_text, is_ok = QInputDialog.getText(
                    self,
                    "Input Text",
                    "Enter Your Text!",
                    QLineEdit.PasswordEchoOnEdit,
                    "default text!",
                    )
        elif tmp_str ==self.l_buttons[1]:
            ret_text, is_ok = QInputDialog.getMultiLineText(
                self,
                "Input Multi-Line Text"
                "Enter Your Multi-Line Text!"
            )
                
        elif tmp_str == self.l_buttons[2]:
            ret_val, is_ok = QInputDialog.getInt(
                self,
                "Input Integer"
                "Enter Your Integer Value"
            )
        if is_ok:
            #print()
            self.ret_label.setText(f'{ret_text}')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MW()
    sys.exit(app.exec())
