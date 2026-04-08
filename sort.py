import sqlite3
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from unicodedata import normalize, combining

DB_NAME = "students.db"

def remove_accents_lower(s):
   
    if not s:
        return ""
    nfkd_form = normalize('NFKD', s.lower())
    
    return "".join([c for c in nfkd_form if not combining(c)]).replace('đ', 'd')
#combining(c)=True if dấu hợp lệ,đ ko tách thành d đc nên cần replace
def get_sorted_students(criteria):
   
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    all_students = cursor.fetchall()
    conn.close()

    if not all_students:
        return []

    try:
        if "ID" in criteria:
           
            all_students.sort(key=lambda x: x[0])

        elif "Điểm" in criteria:
            def score_key(x):
                try:
                    score = float(x[2]) if x[2] is not None and str(x[2]).strip() != "" else 0.0
                except (ValueError, TypeError):
                    score = 0.0
               
                return (-score, x[0]) 
            
            all_students.sort(key=score_key)

        elif "Họ tên" in criteria:
            def name_sort_key(student):
                # student[1] là cột Họ tên
                full_name = student[1].strip().split()
                if not full_name:
                    return ("", "", student[0])
                
                ten = full_name[-1] 
                ho_dem = " ".join(full_name[:-1])
                
                return (remove_accents_lower(ten), ten.lower(), remove_accents_lower(ho_dem), student[0])
            
            all_students.sort(key=name_sort_key)

    except Exception as e:
        print(f"Lỗi thực thi sắp xếp: {e}")#ko cần Qmessagebox
        
    return all_students

class SortTestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sắp xếp sinh viên") 
        self.setGeometry(200, 200, 800, 500)
        
        layout = QVBoxLayout()
        
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Sắp xếp theo...", "ID", "Điểm", "Họ tên"]) 
        
        # currentIndexChanged là Signal có sẵn của QComboBox, phát ra khi  chọn mục khác
        self.sort_combo.currentIndexChanged.connect(self.run_sort)
        
        self.sort_combo.setStyleSheet("""
            background-color: #ff69b4; 
            color: white; 
            font-size: 18px; 
            padding: 5px;
            font-weight: bold;
        """)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Họ tên", "Điểm", "Ngành", "Năm"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(QLabel("Chọn kiểu sắp xếp để kiểm tra:"))
        layout.addWidget(self.sort_combo)
        layout.addWidget(self.table)
        self.setLayout(layout)
        
        self.run_sort()

    def run_sort(self):
        criteria = self.sort_combo.currentText()
        
        if "..." in criteria:
            return

        try:
            results = get_sorted_students(criteria)
            self.display_results(results)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi hiển thị: {str(e)}")

    def display_results(self, results):
      
        self.table.setRowCount(0)
        for data in results:
            row = self.table.rowCount()
            self.table.insertRow(row)
            for i, value in enumerate(data):
                # Nếu dữ liệu là None thì hiện ô trống
                val = "" if value is None else str(value)
                item = QTableWidgetItem(val)
               
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, i, item)

if __name__ == "__main__":
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS students 
                      (id TEXT PRIMARY KEY, name TEXT, score REAL, major TEXT, year INTEGER)''')
    conn.commit()
    conn.close()
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    test_win = SortTestWindow()
    test_win.show()
    sys.exit(app.exec_())