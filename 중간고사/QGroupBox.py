import sys

from PySide6.QtWidgets import (QApplication, QWidget,
                             QLabel,
                             QVBoxLayout,
                             QComboBox)
from PySide6.QtCore import Qt

class MW (QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Ex: QCombobox")
        self.setup_main_wnd()
        self.show()

    def setup_main_wnd(self):
        lm = QVBoxLayout()

        lm.addWidget(QLabel('What is most important?'))

        self.items = ['faith', 'hope', 'love'] #메인 윈도우? 에서 잡근할 수 있도록 넣어줌. 

        cb = QComboBox()

        for idx, c in enumerate(self.items): #굳이 index를 안받아와도 됨,,? 
            cb.addItem(c)

        cb.activated.connect(self.on_selected) #항상 실행이 돼서 슬롯으로 바꿈
        cb.currentIndexChanged.connect(self.on_current_idx_changed)# 다른 항목으로 바꿨을 때 triiger 되는 걸, 바뀌어야지만 trigger됨. 
        lm.addWidget(cb)


        self.dp_label = QLabel("")
        lm.addWidget(self.dp_label)

        self.setLayout(lm)

    def on_selected(self, idx): #인덱스로 넘어옴
        tmp = "you selected :"
        tmp += self.items[idx] 

        print(tmp)
        self.dp_label.setText(tmp)

    def on_current_idx_changed(self, idx):
        print(f'"currentIndexChanged" occured {idx}')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_wnd = MW()
    sys.exit(app.exec())
