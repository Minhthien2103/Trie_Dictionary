import tkinter as tk
from tkinter import ttk, messagebox
from RadixTrie import RadixTrie  # Import class bạn vừa làm

class DictionaryApp:
    def __init__(self, root):
        self.trie = RadixTrie()
        self.trie.load_from_json()
        self.root = root
        self.root.title("Từ Điển Anh-Việt (Radix-Trie)")
        self.root.geometry("600x500")

        # --- KHU VỰC NHẬP LIỆU ---
        input_frame = tk.Frame(self.root, pady=10)
        input_frame.pack(fill=tk.X)

        tk.Label(input_frame, text="Từ vựng:").grid(row=0, column=0, padx=5, pady=5)
        self.word_entry = tk.Entry(input_frame, width=20)
        self.word_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Định nghĩa:").grid(row=1, column=0, padx=5, pady=5)
        self.def_entry = tk.Entry(input_frame, width=20)
        self.def_entry.grid(row=1, column=1, padx=5, pady=5)

        # --- KHU VỰC NÚT BẤM ---
        btn_frame = tk.Frame(self.root, pady=5)
        btn_frame.pack(fill=tk.X)

        tk.Button(btn_frame, text="Thêm từ", width=10, command=self.handle_insert).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Tìm kiếm", width=10, command=self.handle_search).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Xóa từ", width=10, command=self.handle_delete).pack(side=tk.LEFT, padx=10)

        # --- KHU VỰC HIỂN THỊ CÂY RADIX-TRIE ---
        tk.Label(self.root, text="Cấu trúc dữ liệu Radix-Trie (Graphviz):", font=("Arial", 10, "bold")).pack(anchor="w", padx=10)
        
        # Khung chứa ảnh
        self.image_label = tk.Label(self.root, bg="white")
        self.image_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Biến cực kỳ quan trọng để giữ tham chiếu ảnh (nếu không Tkinter sẽ xóa mất ảnh)
        self.current_image = None

    # --- CÁC HÀM XỬ LÝ ---
    def handle_insert(self):
        word = self.word_entry.get().strip().lower()
        definition = self.def_entry.get().strip()
        
        if not word or not definition:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đủ từ và nghĩa!")
            return
            
        self.trie.insert(word, definition)
        self.word_entry.delete(0, tk.END)
        self.def_entry.delete(0, tk.END)
        self.refresh_tree_display()
        messagebox.showinfo("Thành công", f"Đã thêm từ: {word}")
        self.trie.save_to_json()

    def handle_search(self):
        word = self.word_entry.get().strip().lower()
        if not word:
            return
            
        result = self.trie.search(word)
        messagebox.showinfo("Kết quả tìm kiếm", f"Từ: {word}\nNghĩa: {result}")

    def handle_delete(self):
        word = self.word_entry.get().strip().lower()
        if not word:
            return
            
        self.trie.delete(word)
        self.refresh_tree_display()
        messagebox.showinfo("Thông báo", f"Đã thực hiện thao tác xóa từ: {word}")
        self.trie.save_to_json()

    # --- HÀM VẼ LẠI CÂY LÊN GIAO DIỆN ---
    def refresh_tree_display(self):
        # Bước 1: Yêu cầu class RadixTrie xuất cây hiện tại ra file PNG
        # Nhớ đảm bảo bạn đã copy hàm export_graphviz vào class RadixTrie rồi nhé!
        filename = "current_trie"
        self.trie.export_graphviz(filename)
        
        # Bước 2: Đọc file PNG vừa xuất và đưa lên giao diện Tkinter
        try:
            # Tkinter hỗ trợ đọc trực tiếp file PNG (Từ Python 3.4+)
            img_path = f"{filename}.png"
            self.current_image = tk.PhotoImage(file=img_path)
            
            # Cập nhật ảnh mới cho Label
            self.image_label.config(image=self.current_image)
        except Exception as e:
            print(f"Lỗi hiển thị ảnh Graphviz: {e}")
            # Nếu chưa cài Graphviz lõi trên máy, có thể nó sẽ nhảy vào lỗi này.

if __name__ == "__main__":
    root = tk.Tk()
    app = DictionaryApp(root)
    
    app.trie.insert("app", "Ứng dụng")
    app.trie.insert("apple", "Quả táo")
    app.trie.insert("apply", "Nộp đơn")

    app.trie.insert("banana", "Quả chuối")
    app.trie.insert("band", "Ban nhạc")
    app.trie.insert("bandit", "Kẻ cướp") # Chia tách "band"

    app.trie.insert("cat", "Con mèo")
    app.trie.insert("category", "Thể loại")
    app.trie.insert("do", "Làm / Hành động")
    app.trie.insert("dog", "Con chó")
    app.trie.insert("dodge", "Né tránh")
    app.refresh_tree_display()
    
    root.mainloop()