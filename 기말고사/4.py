import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidget, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QMenuBar, QStatusBar, QSplitter
from PySide6.QtGui import QPixmap, QPainter, QPen, QKeySequence, QAction
from PySide6.QtCore import Qt, QDir, QEvent

class ImageLabelingTool(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Labeling Tool")
        self.setGeometry(100, 100, 1000, 600)

        self.initUI()

    def initUI(self):
        self.createMenuBar()
        self.createStatusBar()

        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        self.splitter = QSplitter(Qt.Horizontal)
        self.layout.addWidget(self.splitter)

        self.imageList = QListWidget()
        self.imageList.currentItemChanged.connect(self.displayImage)
        self.splitter.addWidget(self.imageList)

        self.graphicsView = QGraphicsView()
        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)
        self.splitter.addWidget(self.graphicsView)

        self.pen = QPen(Qt.black, 2, Qt.SolidLine)

        self.graphicsView.setRenderHint(QPainter.Antialiasing)
        self.graphicsView.setMouseTracking(True)
        self.graphicsView.viewport().installEventFilter(self)

        self.imagePaths = []
        self.currentImageIndex = -1

    def createMenuBar(self):
        menuBar = self.menuBar()

        fileMenu = menuBar.addMenu("File")
        openDirAction = QAction("Open Directory", self)
        openDirAction.setShortcut(QKeySequence.Open)
        openDirAction.triggered.connect(self.openDirectory)
        fileMenu.addAction(openDirAction)

        saveLabelAction = QAction("Save Label", self)
        saveLabelAction.setShortcut(QKeySequence.Save)
        saveLabelAction.triggered.connect(self.saveLabel)
        fileMenu.addAction(saveLabelAction)

    def createStatusBar(self):
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

    def openDirectory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Open Directory", QDir.homePath())
        if dir_path:
            self.loadImagesFromDirectory(dir_path)

    def loadImagesFromDirectory(self, dir_path):
        self.imagePaths = [os.path.join(dir_path, f) for f in os.listdir(dir_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
        self.imageList.clear()
        self.imageList.addItems(self.imagePaths)
        if self.imagePaths:
            self.imageList.setCurrentRow(0)

    def displayImage(self, current, previous):
        if current:
            self.currentImageIndex = self.imageList.currentRow()
            imagePath = self.imagePaths[self.currentImageIndex]
            self.statusBar.showMessage(imagePath)
            pixmap = QPixmap(imagePath)
            self.scene.clear()
            self.pixmapItem = QGraphicsPixmapItem(pixmap)
            self.scene.addItem(self.pixmapItem)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Right and self.currentImageIndex < len(self.imagePaths) - 1:
            self.imageList.setCurrentRow(self.currentImageIndex + 1)
        elif event.key() == Qt.Key_Left and self.currentImageIndex > 0:
            self.imageList.setCurrentRow(self.currentImageIndex - 1)

    def saveLabel(self):
        if self.currentImageIndex >= 0:
            imagePath = self.imagePaths[self.currentImageIndex]
            with open('labels.csv', 'a') as f:
                f.write(f"{imagePath},label\n")
            self.statusBar.showMessage(f"Label saved for {imagePath}")

    def eventFilter(self, source, event):
        if event.type() == QEvent.Type.MouseButtonPress and source is self.graphicsView.viewport():
            self.lastPoint = event.pos()
            self.drawing = True
            return True
        elif event.type() == QEvent.Type.MouseMove and source is self.graphicsView.viewport() and self.drawing:
            painter = QPainter(self.pixmapItem.pixmap())
            painter.setPen(self.pen)
            painter.drawLine(self.lastPoint, event.pos())
            painter.end()
            self.lastPoint = event.pos()
            self.graphicsView.viewport().update()
            return True
        elif event.type() == QEvent.Type.MouseButtonRelease and source is self.graphicsView.viewport():
            self.drawing = False
            return True
        return super().eventFilter(source, event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageLabelingTool()
    window.show()
    sys.exit(app.exec())
