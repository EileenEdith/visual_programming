import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton

class MW(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('비밀번호 확인')
        self.initUI()
        self.show()

    def initUI(self):
        layout = QVBoxLayout()
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('사용자 이름을 입력하세요')  # 플레이스홀더 텍스트 설정
        layout.addWidget(self.username_input)

        # 비밀번호를 입력 받는 칸과 버튼 추가
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('비밀번호를 입력하세요')
        self.password_input.setMaxLength(10)
        self.password_input.setEchoMode(QLineEdit.Password) # 플레이스홀더 텍스트 설정
        self.submit_button = QPushButton('login')
        self.submit_button.clicked.connect(self.on_submit)  # 버튼 클릭 시 이벤트 연결

        layout.addWidget(self.password_input)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

        # 비밀번호 입력 필드의 텍스트가 변경될 때마다 check_password 함수 호출
        self.password_input.textChanged.connect(self.check_password)

    def check_password(self):
        # 비밀번호 입력 필드에서 텍스트 가져오기
        password = self.password_input.text()

        has_special_char = False  # 특수문자 여부를 저장할 변수를 False로 초기화합니다.

        # 비밀번호 문자열의 각 문자를 순회하며 특수문자가 있는지 확인합니다.
        for char in password:
            # 현재 문자가 특수문자인지 확인하고, 특수문자라면 has_special_char를 True로 설정하고 반복문을 종료합니다.
            if char in '!@#$%^&*()-_=+[]{}|;:,.<>?':
                has_special_char = True
                break

        # 특수문자가 있는 경우 버튼을 비활성화하고, 없는 경우 활성화하는 부분
        if has_special_char:
            self.submit_button.setEnabled(False)  # 특수문자가 있는 경우 버튼 비활성화
        else:
            self.submit_button.setEnabled(True)  # 특수문자가 없는 경우 버튼 활성화 


    def on_submit(self):
        # 입력된 비밀번호 출력
        password = self.password_input.text()
        username = self.username_input.text()
        if password == "wlgp1030":
            print("사용자 이름:", username)
            print("비밀번호:", password)
            print("welcome")
            QApplication.quit() #프로그램 종료
        else:
            print("틀렸습니다")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_wnd = MW()
    sys.exit(app.exec())
