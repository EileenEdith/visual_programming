import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QListWidget, 
    QVBoxLayout, QWidget, QFileDialog, QMenuBar, 
    QStatusBar, QLabel, QScrollArea, QSlider, QToolBar)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QAction

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Directory to QListWidget Example")  # 윈도우 제목 설정

        # 메인 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 레이아웃 설정
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # QListWidget 생성
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        # 이미지 표시를 위한 QLabel 및 QScrollArea 설정
        self.image_label = QLabel()
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.image_label)
        layout.addWidget(self.scroll_area)

        # StatusBar 생성
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # 메뉴바 설정
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        menubar.setNativeMenuBar(False)

        # 디렉토리 선택 액션 추가
        open_action = QAction("Open Directory", self)
        open_action.triggered.connect(self.open_directory)
        file_menu.addAction(open_action)

        # 툴바 설정 (확대/축소)
        toolbar = QToolBar("Image Toolbar")
        self.addToolBar(toolbar)

        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.triggered.connect(self.zoom_in)
        toolbar.addAction(zoom_in_action)

        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.triggered.connect(self.zoom_out)
        toolbar.addAction(zoom_out_action)

        # QListWidget 아이템 클릭 시 이벤트 연결
        self.list_widget.itemClicked.connect(self.show_image)

        self.dir_path = None  # 선택된 디렉토리 경로 저장 변수
        self.scale_factor = 1.0  # 이미지 스케일 팩터 초기화

        self.show()  # 윈도우 표시

    def open_directory(self):
        self.dir_path = QFileDialog.getExistingDirectory(self, 'Select Directory')
        if self.dir_path:
            self.list_widget.clear()

            jpeg_files = [os.path.basename(f)
                         for f in os.listdir(self.dir_path)
                         if f.endswith('.jpeg')]
            
            for jpeg_file in jpeg_files:
                self.list_widget.addItem(jpeg_file)

    def show_image(self, item):
        f_path = os.path.join(self.dir_path, item.text())
        self.status_bar.showMessage(f_path)
        pixmap = QPixmap(f_path)
        self.image_label.setPixmap(pixmap.scaled(self.scale_factor * pixmap.size(), Qt.KeepAspectRatio))

    def zoom_in(self):
        self.scale_factor *= 1.25
        self.update_image()

    def zoom_out(self):
        self.scale_factor /= 1.25
        self.update_image()

    def update_image(self):
        if not self.image_label.pixmap().isNull():
            self.image_label.setPixmap(self.image_label.pixmap().scaled(self.scale_factor * self.image_label.pixmap().size(), Qt.KeepAspectRatio))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mwd = MainWindow()
    sys.exit(app.exec())
