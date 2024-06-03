#Enter키가 입력되는 경우, my_signal 이라는 커스텀시그널이 발생하고 이를 연결한 slot을 통해 int값을 입력받는 modal dialog가 뜨는 code.
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QDialog, QVBoxLayout, QLineEdit, QPushButton
from PySide6.QtCore import Qt, Signal

class IntInputDialog(QDialog):
    def __init__(self, parent=None): #parent = None으로 설정하면, 다이얼로그는 어떤 특정 위젯에 종속되지 않고 애플리케이션의 모든 창 위에 모달로 표시될 수 있습니다. 이는 다이얼로그가 애플리케이션 내 어디서나 중립적으로 사용될 수 있음을 의미합니다.
        #독립적인 창이나 유틸리티 다이얼로그를 생성할 때 유용
        super().__init__(parent) #parent = None을 매개변수로 설정하고, super().__init__(parent)를 호출하는 방식은 다이얼로그 또는 다른 위젯을 생성할 때 선택적으로 부모를 지정할 수 있도록 하기 위함임.
        self.layout = QVBoxLayout(self)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setPlaceholderText("Enter an integer")
        self.layout.addWidget(self.lineEdit)

        self.button = QPushButton("Submit", self)
        #QDialog 클래스에 미리 구현되어 있는 메서드
        self.button.clicked.connect(self.accept)
        #레이아웃에 이미 self.lineEdit이 추가되어 있으므로, self.button은 self.lineEdit 아래에 위치하게 됨. 
        self.layout.addWidget(self.button)

        #IntInputDialog의 레이아웃 구성을 완성하며, 포함된 모든 위젯들이 수직 레이아웃에 따라 적절히 배치됨. 
        self.setLayout(self.layout) 

    def get_integer(self):
        return int(self.lineEdit.text())

class MW(QMainWindow):
    my_signal = Signal() #이 시그널은 특정 조건이 충족될 때 다른 부분의 코드를 실행할 수 있는 연결 메커니즘을 제공합니다.

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(100, 100, 300, 200)
        label = QLabel(
            """<p>Press the <b>Enter</b> key
            to open an input dialog.</p>""")
        self.setCentralWidget(label)
        self.show()

        self.my_signal.connect(self.show_dialog) #my_signal에 연결된 slot,따라서 Enter 키가 눌리면 self.my_signal.emit()이 호출되어 self.show_dialog 메서드가 실행

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Return:
            print("Enter key pressed!")
            self.my_signal.emit() #연결된 모든 슬롯을 순차적으로 호출, self.my_signal.emit()를 호출하면, self.my_signal에 연결된 모든 슬롯이 실행

    def show_dialog(self):
        dialog = IntInputDialog(self)
        if dialog.exec():
            value = dialog.get_integer()
            print("Integer entered:", value)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MW()
    sys.exit(app.exec())
