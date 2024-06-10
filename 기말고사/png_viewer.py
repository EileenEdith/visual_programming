import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.image import imread

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, 
    QHBoxLayout, QListWidget, QListWidgetItem, QWidget, QFileDialog, QMenuBar, 
    QStatusBar, QPushButton, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

class ImageCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        self.setStyleSheet("background-color: #2f2f2f;")
        self.ax.axis('off')  # Hide the axis
        self.fig.subplots_adjust(
            left=0, right=1,
            top=1, bottom=0
        )

    def display_image(self, image_path):
        self.ax.clear()
        img = imread(image_path)
        self.ax.imshow(img)
        self.ax.axis('off')  # Hide the axis
        self.fig.subplots_adjust(
            left=0, right=1,
            top=1, bottom=0
        )
        self.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PNG Viewer")

        # 메인 레이아웃 설정
        main_layout = QHBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        right_layout = QVBoxLayout()
        right_widget = QWidget()
        right_widget.setLayout(right_layout)

        # QListWidget 생성 및 설정
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        main_layout.addWidget(self.list_widget)
        
        # Matplotlib FigureCanvas 생성 및 설정
        self.canvas = ImageCanvas(self)
        
        # NavigationToolbar 생성 및 설정
        self.nav_toolbar = NavigationToolbar(self.canvas, self)
        right_layout.addWidget(self.nav_toolbar)
        right_layout.addWidget(self.canvas)
        
        main_layout.addWidget(right_widget)

        # StatusBar 생성
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # 메뉴바 설정
        menubar = self.menuBar()
        file_menu = menubar.addMenu("Select Img Dir")
        menubar.setNativeMenuBar(False)

        # 디렉토리 선택 액션 추가
        open_action = QAction("Open Directory", self)
        open_action.triggered.connect(self.open_directory)
        file_menu.addAction(open_action)

        self.image_path = None

        # 마우스 드래그 상태 및 사각형 선택을 위한 변수 초기화
        self.dragging = False
        self.rect = None
        self.start_point = (0, 0)

        # 마우스 클릭 및 드래그 이벤트 연결
        self.canvas.mpl_connect('button_press_event', self.on_click)
        self.canvas.mpl_connect('motion_notify_event', self.on_drag)
        self.canvas.mpl_connect('button_release_event', self.on_release)

        self.show()

    def open_directory(self):
        # 디렉토리 선택 다이얼로그 열기
        directory = QFileDialog.getExistingDirectory(self, "Select Directory")
        if directory:
            self.list_widget.clear()
            # 디렉토리의 png 파일 목록 가져오기
            png_files = [f for f in os.listdir(directory) if f.endswith('.png')]
            for png_file in png_files:
                item = QListWidgetItem(png_file)
                item.setData(Qt.UserRole, os.path.join(directory, png_file))
                self.list_widget.addItem(item)

    def on_item_clicked(self, item):
        # 선택된 아이템의 파일 경로를 가져와서 이미지 표시
        self.image_path = item.data(Qt.UserRole)
        self.canvas.display_image(self.image_path)
        self.status_bar.showMessage(self.image_path)

    def on_click(self, event):
        if self.image_path is None:
            return
        # 마우스 클릭 이벤트 핸들러: 드래그 시작 지점 설정
        if event.inaxes != self.canvas.ax:
            return
        self.dragging = True
        self.start_point = (event.xdata, event.ydata)
        self.rect = self.canvas.ax.add_patch(
            plt.Rectangle(self.start_point, 
                          0, 0, 
                          fill=False, color='red')
        )
        self.canvas.draw()

    def on_drag(self, event):
        if self.image_path is None or not self.dragging:
            return
        # 마우스 드래그 이벤트 핸들러: 사각형의 위치와 크기를 실시간으로 조정
        if event.inaxes != self.canvas.ax:
            return
        x0, y0 = self.start_point
        x1, y1 = event.xdata, event.ydata
        self.rect.set_width(x1 - x0)
        self.rect.set_height(y1 - y0)
        self.rect.set_xy((min(x0, x1), min(y0, y1)))
        self.canvas.draw()

    def on_release(self, event):
        if self.image_path is None:
            return
        # 마우스 버튼 해제 이벤트 핸들러: 사용자가 사각형을 그린 후 마우스 버튼을 놓으면 호출됨
        if event.inaxes != self.canvas.ax or not self.dragging:
            return
        self.dragging = False
        response = QMessageBox.question(self, 
                                        "Confirm", 
                                        "Keep the rectangle?", 
                                        QMessageBox.Yes | QMessageBox.No)
        if response == QMessageBox.No:
            self.rect.remove()  # 사용자가 'No'를 선택했을 때 사각형 삭제
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
