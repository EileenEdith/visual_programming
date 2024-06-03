import sys
import psutil
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PySide6.QtWidgets import QApplication, QMainWindow, QDialog, QVBoxLayout, QLineEdit, QPushButton

class IntervalInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setPlaceholderText("Enter refresh interval in seconds")
        self.layout.addWidget(self.lineEdit)

        self.button = QPushButton("Submit", self)
        self.button.clicked.connect(self.accept)
        self.layout.addWidget(self.button)

        self.setLayout(self.layout)

    def get_interval(self):
        try:
            return int(self.lineEdit.text())
        except ValueError:
            return 1  

class LiveMonitor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("CPU and RAM Usage Monitor")
        self.show()

        # Get update interval from user
        dialog = IntervalInputDialog(self)
        if dialog.exec():
            self.interval = dialog.get_interval()
        else:
            self.interval = 1  # Default interval

        # Set up the matplotlib figures
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1)
        self.ax1.set_title('CPU Usage (%)')
        self.ax2.set_title('RAM Usage (%)')

        self.cpu_usage, self.ram_usage = [], []
        #FuncAnimation은 matplotlib 라이브러리에서 제공하는 애니메이션 기능으로, 주어진 그래프를 주기적으로 자동으로 업데이트할 수 있게 해줍니다. 이를 통해 데이터의 변화를 시간에 따라 실시간으로 시각화할 수 있습니다.
        self.anim = FuncAnimation(self.fig, self.update_graph, init_func=self.init_graph, interval=self.interval * 1000)

        plt.show()

    def init_graph(self):
        self.ax1.set_xlim(0, 60)
        self.ax1.set_ylim(0, 100)
        self.ax2.set_xlim(0, 60)
        self.ax2.set_ylim(0, 100)
        return []

    def update_graph(self, frame):
        self.cpu_usage.append(psutil.cpu_percent()) # 현재 시스템의 CPU 사용률을 백분율로 반환
        self.ram_usage.append(psutil.virtual_memory().percent) #시스템의 가상 메모리 사용 상태에 대한 여러 통계를 반환하는 객체를 제공, 사용 중인 RAM의 비율을 백분율로 나타냅니다

        self.cpu_usage = self.cpu_usage[-60:] #각각 최근 60개의 데이터 포인트만 유지하여, 그래프가 과거의 일정 시간 범위 내 데이터만 표시하도록 함.
        self.ram_usage = self.ram_usage[-60:]
        x = range(len(self.cpu_usage))

        self.ax1.clear()
        self.ax1.plot(x, self.cpu_usage, label='CPU Usage')
        self.ax1.legend()

        self.ax2.clear()
        self.ax2.plot(x, self.ram_usage, label='RAM Usage')
        self.ax2.legend()

        self.ax1.set_title('CPU Usage (%)')
        self.ax2.set_title('RAM Usage (%)')

        return self.ax1, self.ax2

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LiveMonitor()
    sys.exit(app.exec())
