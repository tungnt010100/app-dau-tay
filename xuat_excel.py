import os
import winsound
import sqlite3
from PyQt5.QtWidgets import QFileDialog, QMessageBox
DB_NAME = "students.db"
def export_to_excel(data_list, file_path):
    import pandas as pd 
    try:
        columns = ["ID", "Họ tên", "Điểm", "Ngành", "Năm"]
        df = pd.DataFrame(data_list, columns=columns)
        df.to_excel(file_path, index=False)
        return True, f"Xuất file thành công tại:\n{file_path}"
    except PermissionError:
        return False, "Lỗi: File đang mở ở chương trình khác. Vui lòng đóng lại!"
    except Exception as e:
        return False, str(e)

def run_export_flow(parent_window, data):
   
    if not data:
        winsound.MessageBeep(winsound.MB_ICONHAND)
        QMessageBox.warning(parent_window, "Lỗi", "Không có dữ liệu để xuất!")
        return

    file_path, _ = QFileDialog.getSaveFileName(
        parent_window, "Lưu file Excel", "DanhSachSV.xlsx", "Excel Files (*.xlsx)" 
        #mặc định tên file là DanhsachSV,và file phải ở dạng xlsx(excel)
    )
    
    if file_path:
        success, msg = export_to_excel(data, file_path)
        if success:
            winsound.MessageBeep(winsound.MB_OK)
            QMessageBox.information(parent_window, "Thành công", msg)
            try:
                os.startfile(file_path)
            except:
                pass
        else:
            winsound.MessageBeep(winsound.MB_ICONHAND)
            QMessageBox.critical(parent_window, "Lỗi", msg)

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)

    try:
        conn = sqlite3.connect("students.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        real_data = cursor.fetchall()
        conn.close()
        
        run_export_flow(None, real_data)
    except Exception as e:
        print(f"Chưa có dữ liệu để test: {e}")
    
    sys.exit(app.exec_())