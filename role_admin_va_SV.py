import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QFont

DB_NAME = "students.db"
def verify_admin_password(password):
    return password == "AloVuphaikhongem?"

class EyeButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setFixedSize(24, 24)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                border: none;
                background: transparent;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.1);
            }
        """)
        self.is_visible = False
        self.update_icon()
        
    def update_icon(self):
        self.setText("👁" if self.is_visible else "🔒") 
    
    def toggle_visibility(self):
        self.is_visible = not self.is_visible 
        self.update_icon()
        return self.is_visible # Báo cáo mắt "nhắm" hay "mở"

class AdminLoginDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Xác thực Admin")
        self.setFixedSize(400, 250)
        self.setStyleSheet("background-color: #ffffff; font-size: 16px;")
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(40, 30, 40, 30)
        
        label = QLabel("Nhập mật khẩu:")
        label.setAlignment(Qt.AlignCenter)
        
        password_layout = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("padding: 10px; border: 1px solid #ccc; border-radius: 5px;") # Border radius để "cắt" phần nhọn
        
        self.eye_button = EyeButton()
        self.eye_button.clicked.connect(self.toggle_password_visibility)
        
        password_layout.addWidget(self.password_input)
        password_layout.addWidget(self.eye_button)
        
        self.btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.btn_box.accepted.connect(self.accept)
        self.btn_box.rejected.connect(self.reject)
        
        self.btn_box.setStyleSheet("""
            QPushButton { 
                padding-top: 8px;      /* Cách trên 8px */
                padding-bottom: 8px;   /* Cách dưới 8px */
                padding-left: 15px;    /* Cách trái 15px */
                padding-right: 15px;   /* Cách phải 15px */
                
                border-radius: 4px;    /* Bo góc */
                border: 2px solid ;    /* Tạo độ dày đường viền cho 2 nút OK và Cancel */
                background-color: #f9f9f9;
            }
            QPushButton:hover {   /* Sẽ auto kích hoạt khi rê chuột qua */
                background-color: #fff9c4;
            }
        """)
        
        layout.addWidget(label)
        layout.addLayout(password_layout)  
        layout.addWidget(self.btn_box)
        self.setLayout(layout)

    def toggle_password_visibility(self):
        is_visible = self.eye_button.toggle_visibility() 
        self.password_input.setEchoMode(QLineEdit.Normal if is_visible else QLineEdit.Password)

    def get_password(self):
        return self.password_input.text()

class LoginScreen(QWidget):
    login_success = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Login")
        self.setFixedSize(600, 500) 
        self.setStyleSheet("background-color: #f0f2f5; font-size: 18px;")

        layout = QVBoxLayout()
        layout.setSpacing(40) 
        layout.setContentsMargins(80, 60, 80, 60)

        title = QLabel("Chọn vai trò")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #34495e; margin-bottom: 20px;")

        self.admin_btn = QPushButton("ADMIN")
        self.admin_btn.setCursor(Qt.PointingHandCursor)
        self.admin_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c; color: white; 
                font-weight: bold; padding: 25px; border-radius: 12px; 
            }
            QPushButton:hover { background-color: #c0392b; } /* Khi user lướt qua nút, hover kích hoạt */
        """)
        self.admin_btn.clicked.connect(self.handle_admin_click)

        self.sv_btn = QPushButton("SINH VIÊN")
        self.sv_btn.setCursor(Qt.PointingHandCursor)
        self.sv_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db; color: white; 
                font-weight: bold; padding: 25px; border-radius: 12px; 
            }
            QPushButton:hover { background-color: #2980b9; }
        """)
        self.sv_btn.clicked.connect(self.handle_sv_click)

        layout.addWidget(title)
        layout.addWidget(self.admin_btn)
        layout.addWidget(self.sv_btn)
        
        self.setLayout(layout)

    def handle_admin_click(self):
        dialog = AdminLoginDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            password = dialog.get_password()
            if verify_admin_password(password):
                self.login_success.emit("admin")
            else:
                QMessageBox.warning(self, "Lỗi", "Sai mật khẩu Quản trị viên!")

    def handle_sv_click(self):
        self.login_success.emit("sv")