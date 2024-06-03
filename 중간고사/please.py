import sys
from PySide6.QtWidgets import ( QApplication,
    QDialog,
    QMainWindow,
    QPushButton,
    QDialogButtonBox,
    QVBoxLayout,
    QLabel,
    QMessageBox,
)

class CustomDlg(QDialog):
        def __init__(self, parent = None):
            super().__init__(parent)
            
            self.setWindowTitle('Hello, QDialog')
            
            buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
            
            self.button_box = QDialogButtonBox(buttons)
            
            self.button_box.accepted.connect(self.accept)
            
            self.button_box.rejected.connect(self.reject)
            
            self.layout = QVBoxLayout()
            message = QLabel('Is something ok?')

            self.layout = QVBoxLayout()
            self.layout.addWidget(message)
            self.layout.addWidget(self.button_box) # QDialogButtonBox객체 추가.
            self.setLayout(self.layout)
class MW(QMainWindow): 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QDialog Ex.")
        lm = QVBoxLayout()
        
        button = QPushButton("Press it for a Dialog")
        button.clicked.connect(self.button_clicked)
        

        self.setCentralWidget(button)
        
    def button_clicked(self, s):
        print("click", s)
        #dlg = QDialog(self) #부모 지정
        #dlg = QDialog() #부모 지정 x, 화면 중앙에 만듦
        #dlg.setWindowTitle("QDialog Title") 
        #dlg.exec() #modal 
          # -------------
        # for custom dlg
        #dlg = CustomDlg(self)
        #if dlg.exec(): # Modal Dialog
        #    print('ok')
        #else:
        #    print("cancel")
        
        #------------------
        #QMessageBox.inforamtion
        # result = QMessageBox.information(
        #             self,
        #             'Message',
        #             'This is an information message'
        # )
        # print(f'QMessage.information:{result}')
        
        #------------------
        # QMessageBox.about(
        #         self,
        #         "About This SW",
        #         """<p> The example of QMessageBox <p>
        #         <p> version 0.1 """
        # )
        
        #QMessageBox.inforamtion
        # result = QMessageBox.warning(
        #             self,
        #             'Message',
        #             'This is an information message',
        #             QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel
        # )
        # print(f'QMessage.information:{result}')
        
        ans = QMessageBox.question(
          self,                 # parent
          "title of question",  # 질문 제목
          "cotent of question", # 질문 내용.
          QMessageBox.StandardButton.No | 
          QMessageBox.StandardButton.Yes, # responses
          QMessageBox.StandardButton.Yes # default response
        )
        print(f'{ans=}')
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MW()
    window.show()
    app.exec()