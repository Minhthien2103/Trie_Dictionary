# 📖 Từ Điển Tiếng Anh - Cấu Trúc Dữ Liệu Radix-Trie
**Đồ án môn học CS523 - Đại học Công nghệ Thông tin (UIT)**

Dự án phát triển ứng dụng từ điển Tiếng Anh giao diện trực quan, sử dụng cấu trúc dữ liệu **Radix-Trie (Patricia Tree)** để tối ưu hóa không gian lưu trữ và tăng tốc độ tra cứu với độ phức tạp thời gian là $O(k)$ ($k$ là chiều dài của từ).

---

## ✨ Chức năng chính
- **Tra cứu từ vựng:** Tìm kiếm siêu tốc dựa trên tiền tố.
- **Thêm từ mới (Insert):** Tự động xử lý chia tách nhánh (Splitting) khi có chung tiền tố.
- **Xóa từ (Delete):** Tích hợp thuật toán tự động gộp nhánh (Merge Compaction) để tối ưu bộ nhớ sau khi xóa.
- **Trực quan hóa cấu trúc dữ liệu:** Vẽ sơ đồ cây Radix-Trie theo thời gian thực để minh họa sự thay đổi dữ liệu sau mỗi thao tác.
- **Lưu trữ dữ liệu:** Tự động lưu và tải dữ liệu từ điển qua file `.json`.

---

## 🛠 Công nghệ sử dụng
- **Ngôn ngữ:** Python 3
- **Giao diện (GUI):** Tkinter
- **Trực quan hóa (Graph):** Graphviz Engine
- **Đóng gói:** PyInstaller

---

## 🚀 Hướng dẫn Cài đặt & Sử dụng

### Tùy chọn 1: Chạy trực tiếp
Bạn có thể chạy ứng dụng mà không cần cài đặt môi trường lập trình Python bằng cách tải file `.exe` tại mục **Releases**.

> ⚠️ **YÊU CẦU BẮT BUỘC (QUAN TRỌNG):**
> Ứng dụng sử dụng engine Graphviz để render cây Radix-Trie theo thời gian thực. Để chức năng vẽ cây hoạt động, vui lòng thực hiện:
> 1. Tải và cài đặt phần mềm lõi Graphviz cho Windows tại: [https://graphviz.org/download/](https://graphviz.org/download/)
> 2. Trong lúc cài đặt, **bắt buộc** tick chọn mục: `"Add Graphviz to the system PATH for all users"`.
> 3. Khởi động lại máy tính (hoặc restart lại Explorer) rồi mới mở file `.exe`.
> 
> *(Nếu không cài Graphviz, ứng dụng vẫn có thể Thêm/Xóa từ nhưng khu vực hiển thị sơ đồ cây sẽ bị lỗi).*

### Tùy chọn 2: Chạy từ Source Code
Nếu bạn muốn xem và chạy mã nguồn trực tiếp:

1. Clone kho lưu trữ này về máy:
   ```bash
   git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)
   cd your-repo-name