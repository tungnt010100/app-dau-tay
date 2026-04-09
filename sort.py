import sqlite3
from unicodedata import normalize, combining

DB_NAME = "students.db"

def remove_accents_lower(s):
  
    if not s:
        return ""
    nfkd_form = normalize('NFKD', s.lower())
    return "".join([c for c in nfkd_form if not combining(c)]).replace('đ', 'd')

def get_name_sort_tuple(full_name_str, student_id):
  
    parts = full_name_str.strip().split()
    if not parts:
        return ("", "", student_id)
    
    ten_chinh = parts[-1]
    ho_dem = " ".join(parts[:-1]) if len(parts) > 1 else ""
    
    return (
        remove_accents_lower(ten_chinh), 
        remove_accents_lower(ho_dem), 
        student_id
    )

def get_sorted_students(criteria):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    all_students = cursor.fetchall()
    conn.close()

    if not all_students:
        return []

    try:
        if criteria == "ID":
            
            all_students.sort(key=lambda x: x[0])

        elif criteria == "Điểm":
            def score_sort_logic(x):
               
                try:
                    score_val = float(x[2]) if x[2] is not None and str(x[2]).strip() != "" else 0.0
                except:
                    score_val = 0.0
                

                name_criteria = get_name_sort_tuple(x[1], x[0])
             
                return (-score_val, name_criteria)
            
            all_students.sort(key=score_sort_logic)

        elif criteria == "Họ Tên":
           
            all_students.sort(key=lambda x: get_name_sort_tuple(x[1], x[0]))

    except Exception as e:
        print(f"Lỗi thực thi sắp xếp: {e}")
        
    return all_students
