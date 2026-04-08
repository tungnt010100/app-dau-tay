🎓 App Quản Lý Sinh Viên - Dự án đầu tay
Đây là ứng dụng quản lý sinh viên được xây dựng bằng Python & PyQt5,cho phép QLSV 1 cách khoa học,dễ dàng
✨ Các tính năng nổi bật
**Hệ thống CRUD** : Cho phép Thêm, Sửa, Xóa sinh viên với quy trình kiểm tra dữ liệu đầu vào (Corner Test) chặt chẽ.
Phân quyền người dùng :
Admin: Toàn quyền quản trị dữ liệu.
Sinh viên: Chế độ chỉ xem, tìm kiếm và sắp xếp (cá nút thêm,sửa,xóa bị ẩn đi với SV).
Tìm kiếm thông minh **Fuzzy Search**: Sử dụng thuật toán tìm kiếm gần đúng, cho phép tìm thấy kết quả ngay cả khi gõ thiếu hoặc sai dấu.
Đặc biệt: Tên sinh viên khớp với từ khóa sẽ được highlight màu xanh lục .
Sắp xếp đa tầng **Advanced Sorting**: Hỗ trợ sắp xếp theo ID, Điểm và Tên.
Xử lý logic tên tiếng Việt chuẩn ,ngay cả với những trường hợp khó
Sắp xếp điểm số giảm dần, ưu tiên ID nếu trùng điểm.
**Xuất dữ liệu chuyên nghiệp**: Tích hợp thư viện **Pandas** để xuất báo cáo ra file Excel và tự động mở file ngay sau khi xuất thành công.
**Tích hợp âm thanh**: Sử dụng **winsound** để báo hiệu thành công hoặc cảnh báo lỗi, giúp người dùng tương tác tốt hơn.
🛠 Vài tính năng khác
**Data Normalization**: Sử dụng chuẩn hóa **NFKD Unicode** để xử lý triệt để các ngoại lệ về dấu tiếng Việt trong tính năng Search và Sort.
**Database Optimization**: Sử dụng B-Tree Index trong SQLite3 để đảm bảo tốc độ tìm kiếm cực nhanh kể cả khi dữ liệu lớn.


sửa lại như này chắc ok hơn
