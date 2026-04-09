import sys
import sqlite3
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

DB_NAME = "students.db"

def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            score REAL,
            major TEXT NOT NULL,
            year INTEGER NOT NULL
        )
    ''')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_name ON students (name)')# gần giống tìm kiếm n-phân nhờ chia cluster ,O(logN)
    conn.commit()
    conn.close()

def generate_id(year, major):
    prefix = f"{year}{major}"
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id FROM students 
        WHERE id LIKE ? 
        ORDER BY CAST(SUBSTR(id, ?) AS INTEGER) DESC 
        LIMIT 1
    """, (f"{prefix}%", len(prefix) + 1))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        try:
            last_num = int(result[0][len(prefix):])
            next_num = last_num + 1
        except:
            next_num = 1
    else:
        next_num = 1
    return f"{prefix}{next_num:03d}"

def get_all_students():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students ORDER BY id")
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_student_logic(name, score, major, year):
    student_id = generate_id(year, major)
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students VALUES (?, ?, ?, ?, ?)",
                      (student_id, name, score, major, year))
        conn.commit()
        conn.close()
        return True, student_id
    except Exception as e:
        return False, str(e)

def update_student_logic(student_id, name, score, major, year):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE students SET name=?, score=?, major=?, year=? WHERE id=?",
                      (name, score, major, year, student_id))
        conn.commit()
        conn.close()
        return True, "Cập nhật thành công"
    except Exception as e:
        return False, str(e)

def delete_student_logic(student_id):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id=?", (student_id,))
        conn.commit()
        conn.close()
        return True, "Xóa thành công"
    except Exception as e:
        return False, str(e)

class StudentApp(QWidget):
    def __init__(self):
        super().__init__()
        setup_database() 
        self.init_ui()
        self.load_students()

    def init_ui(self):
        self.setWindowTitle("Quản Lý Sinh Viên")
        self.setGeometry(300, 300, 900, 600)
        layout = QVBoxLayout()
        
        form_layout = QHBoxLayout()
        self.name_input = QLineEdit(); self.name_input.setPlaceholderText("Họ tên")
        self.score_input = QLineEdit(); self.score_input.setPlaceholderText("Điểm")
        self.major_input = QLineEdit(); self.major_input.setPlaceholderText("Mã ngành")
        self.year_input = QLineEdit(); self.year_input.setPlaceholderText("Năm nhập học")
        
        form_layout.addWidget(self.name_input); form_layout.addWidget(self.score_input)
        form_layout.addWidget(self.major_input); form_layout.addWidget(self.year_input)
        
        button_layout = QHBoxLayout()
        self.add_btn = QPushButton("Thêm"); self.add_btn.clicked.connect(self.add_student)
        self.update_btn = QPushButton("Sửa"); self.update_btn.clicked.connect(self.update_student)
        self.delete_btn = QPushButton("Xóa"); self.delete_btn.clicked.connect(self.delete_student)
        
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.update_btn)
        button_layout.addWidget(self.delete_btn)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Họ tên", "Điểm", "Ngành", "Năm"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows) 
        self.table.itemClicked.connect(self.select_row) 
        
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.table)
        self.setLayout(layout)

    def load_students(self):
        self.table.setRowCount(0)#để"xóa"dữ liệu bảng
        rows = get_all_students() #khi này chỉ thêm ông thứ i,chứ ko thêm các ông 1,2,...,i-1 ,tránh trùng
        for row_data in rows:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for i, data in enumerate(row_data):
                val = "" if data is None else str(data)
                self.table.setItem(row, i, QTableWidgetItem(val))

    def select_row(self):
        curr_row = self.table.currentRow()
        if curr_row < 0: return
        self.name_input.setText(self.table.item(curr_row, 1).text())
        self.score_input.setText(self.table.item(curr_row, 2).text())
        self.major_input.setText(self.table.item(curr_row, 3).text())
        self.year_input.setText(self.table.item(curr_row, 4).text())

    def validate_input(self):
        name = self.name_input.text().strip()
        score_text = self.score_input.text().strip()
        major = self.major_input.text().strip().upper()
        year_text = self.year_input.text().strip()
        
        if not name or any(char.isdigit() for char in name):
            QMessageBox.warning(self, "Lỗi", "Tên không hợp lệ!")
            return None

        score = None
        if score_text:
            try:
                score = float(score_text)
                if not (0 <= score <= 10):
                    QMessageBox.warning(self, "Lỗi", "Điểm phải từ 0 đến 10!")
                    return None
            except ValueError:
                QMessageBox.warning(self, "Lỗi", "Điểm phải là số!")
                return None
        
        try:
            year = int(year_text)
        except:
            QMessageBox.warning(self, "Lỗi", "Năm không hợp lệ!")
            return None
            
        return name, score, major, year

    def add_student(self):
        valid = self.validate_input()
        if not valid: return
        success, result = add_student_logic(*valid)
        if success:
            self.load_students()
            QMessageBox.information(self, "Thành công", f"Đã thêm: {result}")
        else:
            QMessageBox.critical(self, "Lỗi", result)

    def update_student(self):
        curr_row = self.table.currentRow()
        if curr_row < 0:
            QMessageBox.warning(self, "Lỗi", "Hãy chọn 1 dòng để sửa!")
            return
        
        student_id = self.table.item(curr_row, 0).text()
        valid = self.validate_input()
        if not valid: return
        
        success, msg = update_student_logic(student_id, *valid)
        if success:
            self.load_students()
            QMessageBox.information(self, "Thành công", msg)
        else:
            QMessageBox.critical(self, "Lỗi", msg)

    def delete_student(self):
        curr_row = self.table.currentRow()
        if curr_row < 0:
            QMessageBox.warning(self, "Lỗi", "Hãy chọn 1 dòng để xóa!")
            return
            
        student_id = self.table.item(curr_row, 0).text()
        reply = QMessageBox.question(self, "Xác nhận", f"Xóa SV {student_id}?", 
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            success, msg = delete_student_logic(student_id)
            if success:
                self.load_students()
                QMessageBox.information(self, "Thành công", msg)
            else:
                QMessageBox.critical(self, "Lỗi", msg)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StudentApp()
    window.show()
    sys.exit(app.exec_())