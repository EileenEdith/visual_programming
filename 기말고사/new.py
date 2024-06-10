import sys
import os
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QListWidget,
    QListWidgetItem, 
    QHBoxLayout, QVBoxLayout, QWidget, QFileDialog, QMenuBar, 
    QStatusBar, QLabel, QLineEdit, QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.image as mpimg
import matplotlib.pyplot as plt  # Import added

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

        self.start_point = None
        self.end_point = None
        self.rect = None

        self.mpl_connect('button_press_event', self.on_click)
        self.mpl_connect('motion_notify_event', self.on_motion)
        self.mpl_connect('button_release_event', self.on_release)

    def display_image(self, image_path):
        self.ax.clear()
        img = mpimg.imread(image_path)
        self.ax.imshow(img)
        self.ax.axis('off')  # Hide the axis
        self.fig.subplots_adjust(
            left=0, right=1,
            top=1, bottom=0
        )
        self.draw()

    def save_image(self, save_path):
        self.fig.savefig(save_path, bbox_inches='tight', pad_inches=0)
        self.draw()

    def on_click(self, event):
        if event.button == 1 and event.inaxes:  # Left mouse button
            self.start_point = (event.xdata, event.ydata)
            if self.rect:
                self.rect.remove()
                self.rect = None

    def on_motion(self, event):
        if self.start_point and event.inaxes:
            if self.rect:
                self.rect.remove()
            x0, y0 = self.start_point
            x1, y1 = event.xdata, event.ydata
            self.rect = self.ax.add_patch(
                plt.Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False, edgecolor='red', linewidth=2)
            )
            self.draw()

    def on_release(self, event):
        if event.button == 1 and self.start_point and event.inaxes:  # Left mouse button
            self.end_point = (event.xdata, event.ydata)
            self.start_point = None
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
        
        # NavigationToolbar 생성 및 설정.
        self.nav_toolbar = NavigationToolbar(self.canvas, self)
        
        right_layout.addWidget(self.nav_toolbar)
        right_layout.addWidget(self.canvas)
        
        # Label, LineEdit, and Button for labeling
        self.label_label = QLabel("Label:")
        self.label_edit = QLineEdit()
        self.save_button = QPushButton("Save Labeled Image")
        self.save_button.clicked.connect(self.save_labeled_image)

        right_layout.addWidget(self.label_label)
        right_layout.addWidget(self.label_edit)
        right_layout.addWidget(self.save_button)

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
        file_path = item.data(Qt.UserRole)
        self.canvas.display_image(file_path)
        self.status_bar.showMessage(file_path)
        self.current_image_path = file_path

    def save_labeled_image(self):
        label = self.label_edit.text()
        if self.current_image_path and label:
            # 이미지에 라벨 추가
            self.canvas.ax.text(10, 10, label, color='white', fontsize=12, bbox=dict(facecolor='black', alpha=0.5))
            save_path = self.current_image_path.replace('.png', f'_{label}.png')
            self.canvas.save_image(save_path)
            self.status_bar.showMessage(f"Labeled image saved to {save_path}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())
