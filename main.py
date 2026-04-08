import sys
import winsound
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

import crud, giaodien, search, sort, role_admin_va_SV, xuat_excel

class MainController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyle("Fusion")
        
        self.login_win = role_admin_va_SV.LoginScreen()
        self.main_win = giaodien.StudentAppUI()
        
        self.login_win.login_success.connect(self.on_login_success)
        self.connect_main_signals()

    def on_login_success(self, role):
        self.role = role
        is_admin = (role == "admin")
        self.main_win.add_btn.setVisible(is_admin)
        self.main_win.update_btn.setVisible(is_admin)
        self.main_win.delete_btn.setVisible(is_admin)
        
        self.login_win.close()
        self.main_win.show()
        winsound.MessageBeep(winsound.MB_OK)
        self.refresh_table_data()

    def connect_main_signals(self):
        self.main_win.search_input.textChanged.connect(self.handle_search)
        self.main_win.sort_combo.currentIndexChanged.connect(self.handle_sort)
        self.main_win.add_btn.clicked.connect(self.handle_add)
        self.main_win.update_btn.clicked.connect(self.handle_update)
        self.main_win.delete_btn.clicked.connect(self.handle_delete)
        self.main_win.excel_btn.clicked.connect(self.handle_export)
        self.main_win.table.itemClicked.connect(self.fill_form_from_table)

    def refresh_table_data(self):
        data = crud.get_all_students()
        # Gọi hàm hiển thị từ file search
        search.display_results_to_table(self.main_win.table, [("NORMAL", r) for r in data])

    def handle_search(self):
        query = self.main_win.search_input.text()
        if not query: self.refresh_table_data(); return
        results = search.search_engine(query)
        search.display_results_to_table(self.main_win.table, results)

    def handle_sort(self):
        criteria = self.main_win.sort_combo.currentText()
        if criteria == "Sắp xếp": return
        data = sort.get_sorted_students(criteria)
        search.display_results_to_table(self.main_win.table, [("NORMAL", r) for r in data])

    def handle_add(self):
        success, result = crud.add_student_logic(
            self.main_win.name_input.text(), self.main_win.score_input.text(),
            self.main_win.major_input.text(), self.main_win.year_input.text()
        )
        self.finalize_crud(success, f"Đã thêm SV: {result}" if success else result)

    def handle_update(self):
        row = self.main_win.table.currentRow()
        if row < 0: return
        sid = self.main_win.table.item(row, 0).text()
        success, msg = crud.update_student_logic(
            sid, self.main_win.name_input.text(), self.main_win.score_input.text(),
            self.main_win.major_input.text(), self.main_win.year_input.text()
        )
        self.finalize_crud(success, msg)

    def handle_delete(self):
        row = self.main_win.table.currentRow()
        if row < 0: return
        sid = self.main_win.table.item(row, 0).text()
        if QMessageBox.question(self.main_win, "Xác nhận", f"Xóa SV {sid}?") == QMessageBox.Yes:
            success, msg = crud.delete_student_logic(sid)
            self.finalize_crud(success, msg)

    def handle_export(self):
        current_data = []
        for r in range(self.main_win.table.rowCount()):
            current_data.append([self.main_win.table.item(r, c).text() for c in range(5)])
            #c tương đương 5 thuộc tính của SV,r là duyệt các SV(hàng)
        xuat_excel.run_export_flow(self.main_win, current_data)

    def finalize_crud(self, success, message):
        winsound.MessageBeep(winsound.MB_OK if success else winsound.MB_ICONHAND)
        QMessageBox.information(self.main_win, "Thông báo", message) if success else QMessageBox.critical(self.main_win, "Lỗi", message)
        if success: self.refresh_table_data()

    def fill_form_from_table(self, item):
        row = item.row()
        self.main_win.name_input.setText(self.main_win.table.item(row, 1).text())
        self.main_win.score_input.setText(self.main_win.table.item(row, 2).text())
        self.main_win.major_input.setText(self.main_win.table.item(row, 3).text())
        self.main_win.year_input.setText(self.main_win.table.item(row, 4).text())

    def run(self):
        self.login_win.show()
        sys.exit(self.app.exec_())

if __name__ == "__main__":
    crud.setup_database()
    MainController().run()