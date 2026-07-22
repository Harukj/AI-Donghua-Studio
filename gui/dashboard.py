import customtkinter as ctk
from PIL import Image
import os

class Dashboard(ctk.CTkFrame):
    def __init__(self, parent):
        # Khởi tạo Frame chính cho Dashboard với màu nền đồng bộ
        super().__init__(parent, fg_color="transparent")
        
        # Cấu hình lưới (Grid layout): 2 cột (Cột 0 chứa danh mục, Cột 1 chứa nội dung chi tiết)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)
        
        # 1. TẠO KHU VỰC DANH MỤC QUẢN LÝ (Left Panel)
        self.menu_frame = ctk.CTkFrame(self, corner_radius=10)
        self.menu_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Tiêu đề của phân khu chức năng
        self.title_label = ctk.CTkLabel(
            self.menu_frame, 
            text="QUẢN LÝ TÀI NGUYÊN", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.title_label.pack(padx=10, pady=15)
        
        # Danh sách các danh mục cần quản lý trong Sprint 1
        self.categories = [
            "Project",
            "Episodes",
            "Characters",
            "Environments",
            "Scenes",
            "Videos",
            "Audio",
            "Storage"
        ]
        
        # Tự động sinh ra các nút bấm tương ứng với từng danh mục
        self.buttons = {}
        for cat in self.categories:
            btn = ctk.CTkButton(
                self.menu_frame,
                text=cat,
                anchor="w",                     # Căn chữ lề trái cho đẹp
                height=40,
                corner_radius=6,
                font=ctk.CTkFont(size=13),
                command=lambda c=cat: self.on_category_click(c)
            )
            btn.pack(padx=15, pady=5, fill="x")
            self.buttons[cat] = btn

        # 2. TẠO KHU VỰC HIỂN THỊ NỘI DUNG CHI TIẾT (Right Panel)
        self.content_frame = ctk.CTkFrame(self, corner_radius=10)
        self.content_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Nhãn hiển thị nội dung tạm thời khi mới mở phần mềm
        self.status_label = ctk.CTkLabel(
            self.content_frame, 
            text="Chọn một danh mục để xem chi tiết", 
            font=ctk.CTkFont(size=14, italic=True)
        )
        self.status_label.pack(expand=True)

    def on_category_click(self, category_name):
        """
        Hàm xử lý sự kiện khi người dùng click vào từng mục trên Dashboard
        """
        print(f"Đang mở khu vực quản lý: {category_name}")
        
        # Cập nhật tiêu đề hiển thị bên khung nội dung bên phải
        self.status_label.configure(
            text=f"Giao diện quản lý [{category_name}] đang được tải...",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        
        # Highlight nút đang chọn và bỏ chọn các nút khác
        for name, btn in self.buttons.items():
            if name == category_name:
                btn.configure(fg_color=("#3B8ED0", "#1F6AA5")) # Màu xanh đậm khi chọn
            else:
                btn.configure(fg_color="transparent") # Trả về nền trong suốt nếu không chọn
