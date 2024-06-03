import sys
from PySide6.QtWidgets import (QApplication, QWidget, 
                             QRadioButton, QCheckBox, QButtonGroup,
                             QHBoxLayout,QVBoxLayout,
                             QGroupBox)
from PySide6.QtCore import Qt

class MW (QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setMinimumSize(400,200)
        self.setWindowTitle("QGroupBox Ex")
        self.setup_main_wnd()
        self.show()

    def setup_main_wnd(self):

        lm = QHBoxLayout()

        self.checks = QGroupBox("QCheckBox Grp")
        self.set_check_boxes()
        lm.addWidget(self.checks)

        self.radios = QGroupBox("QRadioButton Grp")
        self.set_radio_buttons()
        lm.addWidget(self.radios)

        self.setLayout(lm)

    def set_check_boxes(self):
        lm = QVBoxLayout()
        self.button_grp_checks = QButtonGroup()
        for idx in range(3):
            cb = QCheckBox(f"check {idx}")
            self.button_grp_checks.addButton(cb)
            lm.addWidget(cb)
        self.checks.setLayout(lm)
        self.button_grp_checks.setExclusive(False)
        self.button_grp_checks.buttonClicked.connect(self.toggle_check_box)

    def set_radio_buttons(self):
        lm = QVBoxLayout()
        self.button_grp_radios = QButtonGroup()
        for idx in range(3):
            rb = QRadioButton(f"radio {idx}")
            self.button_grp_radios.addButton(rb)
            lm.addWidget(rb)
        self.radios.setLayout(lm)
        self.button_grp_radios.setExclusive(False)
        self.button_grp_radios.buttonClicked.connect(self.toggle_radio_button)

    def toggle_check_box(self, state):
        for c in self.button_grp_checks.buttons():
            if c.isChecked():
                print(c.text())
        print("======================\n\n")

    def toggle_radio_button(self, state):
        for idx, c in enumerate(self.button_grp_radios.buttons()):
            if c.isChecked():
                print(idx, c.text())
        print("======================\n\n")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    wnd = MW()
    sys.exit(app.exec())
