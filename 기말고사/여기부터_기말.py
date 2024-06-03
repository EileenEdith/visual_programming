import sys

from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QProgressBar, 
    QPushButton,
    QWidget, QVBoxLayout,
)
from PySide6.QtCore import QTimer 

class MW(QMainWindow):

    def __init__(self): #인스턴스 메서드
        super(MW, self).__init__() #MW클래스가 고유하게 가진 기능들을 추가, super().__init__()과 같음
        self.setWindowTitle("ex: QProgressBar")
        self.setGeometry(200, 200, 300, 150) #x,y,w,h

        self.progressBar = QProgressBar(self, minimum=9, maximum=20)
        self.progressValue = self.progressBar.minimum()
        self.progressBar.setGeometry(50, 50, 200, 30)

        self.startButton = QPushButton("start", self)
        #self.startButton.setGeometry(100, 100, 100, 30) 
        self.startButton.clicked.connect(self.startProgress)

        self.timer = QTimer(self) #인스턴스 어트리뷰트로 유지(timer라고만 만들면 local scoop에서 만들어지기 때문에 해당 메서드가 끝나면 사라짐)
        self.timer.timeout.connect(self.updateProgress)
        #self.progressValue = 0

        lm = QVBoxLayout()
        lm.addWidget(self.progressBar)
        lm.addWidget(self.startButton)

        tmp = QWidget()
        tmp.setLayout(lm)

        self.setCentralWidget(tmp)
        self.show()

    def startProgress(self): #인스턴스 메서드
        self.progressBar.reset()
        self.progressValue = self.progressBar.value()
        self.startButton.setEnabled(False)
        # self.progressBar.setValue(self.progressValue)
        self.timer.start(100)  # 100 milliseconds마다 타이머 발생, stop을 하기 전까진 계속 동작

    def updateProgress(self):
        self.progressValue +=1
        self.progressBar.setValue(self.progressValue)
        if self.progressValue >= self.progressBar.maximum():
            self.timer.stop()
            #self.progressBar.reset()
            self.startButton.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MW()
    sys.exit(app.exec())