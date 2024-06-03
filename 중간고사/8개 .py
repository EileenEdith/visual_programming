import sys
from PySide6.QtWidgets import (
    QApplication, QDialog, QMainWindow, QVBoxLayout, QWidget,
    QMessageBox, QDialogButtonBox, QLabel, QRadioButton, QGroupBox,QHBoxLayout
)

class CustomDlg(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Custom Dialog Example')
        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.button_box = QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        
        layout = QVBoxLayout()
        message = QLabel('Do you want to proceed with the custom action?')
        layout.addWidget(message)
        layout.addWidget(self.button_box)
        self.setLayout(layout)

class MW(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QMessageBox Examples")
        self.setup_ui()
        
    def setup_ui(self):
        # Create the central widget and main layout
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Create a group box for organizing radio buttons
        group_box = QGroupBox("Dialog Types1")
        layout = QVBoxLayout()
        group_boxs= QGroupBox("Dialog Types2")
        layouts = QVBoxLayout()

        # Create buttons and connect to the appropriate functions
        btn_info = QRadioButton('Information')
        btn_warning = QRadioButton('Warning')
        btn_critical = QRadioButton('Critical')
        btn_question = QRadioButton('Question')
        
        btn_about = QRadioButton('About')
        btn_about_qt = QRadioButton('About Qt')
        btn_custom = QRadioButton('Custom Dialog')
        btn_plain = QRadioButton('Plain Dialog')
        
        btn_info.clicked.connect(self.show_info)
        btn_warning.clicked.connect(self.show_warning)
        btn_critical.clicked.connect(self.show_critical)
        btn_question.clicked.connect(self.show_question)
        
        btn_about.clicked.connect(self.show_about)
        btn_about_qt.clicked.connect(self.show_about_qt)
        btn_custom.clicked.connect(self.show_custom)
        btn_plain.clicked.connect(self.show_plain)

        # Add buttons to layout within the group box
        layout.addWidget(btn_info)
        layout.addWidget(btn_warning)
        layout.addWidget(btn_critical)
        layout.addWidget(btn_question)
        
        layouts.addWidget(btn_about)
        layouts.addWidget(btn_about_qt)
        layouts.addWidget(btn_custom)
        layouts.addWidget(btn_plain)
        
        # Set the layout for the group box and add to the main layout
        group_box.setLayout(layout)
        group_boxs.setLayout(layouts)
        main_layout.addWidget(group_box)
        main_layout.addWidget(group_boxs)
    def show_info(self):
        QMessageBox.information(self, 'Information', 'This is an information message.')

    def show_warning(self):
        QMessageBox.warning(self, 'Warning', 'This is a warning message.')

    def show_critical(self):
        QMessageBox.critical(self, 'Critical', 'This is a critical message.')

    def show_question(self):
        result = QMessageBox.question(self, 'Question', 'Is this a question message?', QMessageBox.Yes | QMessageBox.No)
        print(f'Question result: {result}')

    def show_about(self):
        QMessageBox.about(self, 'About', 'This is about this software.')

    def show_about_qt(self):
        QMessageBox.aboutQt(self, 'About Qt')

    def show_custom(self):
        dlg = CustomDlg(self)
        if dlg.exec():
            print('Custom Dialog Accepted')
        else:
            print('Custom Dialog Rejected')

    def show_plain(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Plain Dialog")
        dlg.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MW()
    window.show()
    sys.exit(app.exec())
