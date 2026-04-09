import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QFont
DB_NAME = "students.db"
class StudentAppUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Quản Lý Sinh Viên")
        self.setGeometry(150, 150, 1000, 800)
        self.setStyleSheet("font-size: 16px;")

        main_layout = QVBoxLayout()

        top_bar = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Tìm kiếm...")
        self.search_input.setFixedWidth(360)
    
        self.sort_combo = QComboBox()
        # Giữ nguyên tên "Họ Tên" như cũ
        self.sort_combo.addItems(["Sắp xếp", "ID", "Họ Tên", "Điểm"])
        self.sort_combo.setStyleSheet("background-color: #ff69b4; color: white; font-size: 18px; padding: 6px;")
        
        self.excel_btn = QPushButton("Xuất Excel")
        self.excel_btn.setStyleSheet("background-color: #2ecc71; color: white; font-weight: bold;")

        top_bar.addWidget(self.search_input)
        top_bar.addStretch()
        top_bar.addWidget(self.sort_combo)
        top_bar.addWidget(self.excel_btn)

       
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Họ tên", "Điểm", "Ngành", "Năm"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        form_layout = QGridLayout()
        self.name_input = QLineEdit()
        self.score_input = QLineEdit()
        self.major_input = QLineEdit()
        self.year_input = QLineEdit()

        form_layout.addWidget(QLabel("Họ tên:"), 0, 0)
        form_layout.addWidget(self.name_input, 0, 1)
        form_layout.addWidget(QLabel("Điểm:"), 0, 2)
        form_layout.addWidget(self.score_input, 0, 3)
        form_layout.addWidget(QLabel("Mã ngành:"), 1, 0)
        form_layout.addWidget(self.major_input, 1, 1)
        form_layout.addWidget(QLabel("Năm:"), 1, 2)
        form_layout.addWidget(self.year_input, 1, 3)

        button_layout = QHBoxLayout()
        self.add_btn = QPushButton("Thêm")
        self.update_btn = QPushButton("Cập nhật")
        self.delete_btn = QPushButton("Xóa")
        
        self.add_btn.setStyleSheet("background-color: #3498db; color: white; padding: 9px; font-size: 24px;")
        self.update_btn.setStyleSheet("background-color: #f1c40f; color: black; padding: 9px; font-size: 24px;")
        self.delete_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 9px; font-size: 24px;")

        button_layout.addStretch()
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.update_btn)
        button_layout.addWidget(self.delete_btn)

       
        main_layout.addLayout(top_bar)
        main_layout.addWidget(self.table)
        main_layout.addSpacing(15)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = StudentAppUI()
    window.show()
    sys.exit(app.exec_())
