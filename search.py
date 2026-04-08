import sqlite3
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont
from unicodedata import normalize, combining
from rapidfuzz import fuzz

DB_NAME = "students.db"
FUZZY_THRESHOLD = 72

def remove_accents_lower(s):
    if not s: return ""
    nfkd_form = normalize('NFKD', s.lower())
    return "".join([c for c in nfkd_form if not combining(c)]).replace('đ', 'd')#ko phải dấu thì cho cook
   #thêm NFKD để xử lí trường hợp search đặc biệt
def search_engine(query):
    query = query.strip().lower()
    if not query: return []
    
    clean_query = remove_accents_lower(query)

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Tìm chính xác ID
    cursor.execute("SELECT * FROM students WHERE id = ?", (query.upper(),))
    exact_id = cursor.fetchone()
    if exact_id:
        conn.close()
        return [("EXACT_ID", exact_id)]

    #Tìm gần đúng Tên
    cursor.execute("SELECT * FROM students")
    all_students = cursor.fetchall()
    conn.close()

    fuzzy_results = []
    for student in all_students:
        clean_name = remove_accents_lower(student[1])
        
        score = fuzz.partial_ratio(clean_query, clean_name)
        
        if score >= FUZZY_THRESHOLD:
            fuzzy_results.append((score, student))

    fuzzy_results.sort(key=lambda x: (-x[0], x[1]))
    return [("FUZZY_NAME", item[1]) for item in fuzzy_results]

def display_results_to_table(table_widget, results):
  
    table_widget.setRowCount(0)
    for tag, data in results:
        row = table_widget.rowCount()
        table_widget.insertRow(row)
        for i, val in enumerate(data):
            display_val = "" if val is None else str(val)
            item = QTableWidgetItem(display_val)
            item.setTextAlignment(Qt.AlignCenter)  
            if tag == "FUZZY_NAME" and i == 1:
                item.setForeground(QColor(20, 250, 20))
                font = QFont(); font.setBold(True); item.setFont(font)
            table_widget.setItem(row, i, item)