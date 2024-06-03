import sys
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QFileDialog, QMessageBox
from main_window_ui import Ui_MainWindow

class TextEditor(QtWidgets.QMainWindow):
    def __init__(self):
        super(TextEditor, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # macOS에서 메뉴바를 강제로 애플리케이션 창에 표시
        if sys.platform == 'darwin':
            self.menuBar().setNativeMenuBar(False)

        # 메뉴 바의 Open 액션에 대한 트리거 연결
        self.ui.actionOpen.triggered.connect(self.open_file)
        # 텍스트가 변경될 때마다 상태 바를 업데이트
        self.ui.textEdit.textChanged.connect(self.update_status_bar)

        self.setWindowTitle("Text Editor")
        self.show()

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Text File", "", "Text Files (*.txt)", options=options)
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.ui.textEdit.setPlainText(content)
                    self.update_status_bar()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not open file: {e}")

    def update_status_bar(self):
        text_length = len(self.ui.textEdit.toPlainText())
        self.statusBar().showMessage(f"Character count: {text_length}")

def main():
    app = QtWidgets.QApplication(sys.argv)
    editor = TextEditor()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
