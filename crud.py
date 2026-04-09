import sqlite3

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
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_name ON students (name)') # tìm kiếm theo cluster với O(logN)
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

def add_student_logic(name, score_text, major, year_text):
    
    name = name.strip()
    if not name or any(char.isdigit() for char in name):
        return False, "Tên không hợp lệ (không được để trống hoặc chứa số)!"

    score = None
    if score_text and str(score_text).strip() != "":
        try:
            score = float(score_text)
            if not (0 <= score <= 10):
                return False, "Điểm phải từ 0 đến 10!"
        except ValueError:
            return False, "Điểm phải là số!"
    
    try:
        year = int(year_text)
        if not (1900 <= year <= 2100):
            return False, "Năm nhập học phải từ 1900 đến 2100!"
    except:
        return False, "Năm không hợp lệ!"

    major = major.strip().upper()
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

def update_student_logic(student_id, name, score_text, major, year_text):
    try:
       
        name = name.strip()
        if not name or any(char.isdigit() for char in name):
            return False, "Tên không hợp lệ!"

        score = None
        if score_text and str(score_text).strip() != "":
            score = float(score_text)
        
        year = int(year_text)
        if not (1900 <= year <= 2100):
            return False, "Năm nhập học phải từ 1900 đến 2100!"
            
        major = major.strip().upper()

        new_id = student_id
        if not student_id.startswith(f"{year}{major}"):
            new_id = generate_id(year, major) 

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
       #cập nhật ID
        cursor.execute("UPDATE students SET id=?, name=?, score=?, major=?, year=? WHERE id=?",
                      (new_id, name, score, major, year, student_id))
        conn.commit()
        conn.close()
        return True, f"Cập nhật thành công! (ID mới: {new_id})" if new_id != student_id else "Cập nhật thành công"
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