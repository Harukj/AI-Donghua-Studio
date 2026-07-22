import customtkinter as ctk
from tkinter import messagebox
from core.project_manager import ProjectManager

class Dashboard(ctk.CTkFrame):
    def __init__(self, parent):
        # Khởi tạo Frame chính cho Dashboard với màu nền đồng bộ
        super().__init__(parent, fg_color="transparent")
        
        # Khởi tạo bộ quản lý dự án để tự động sinh thư mục khi bấm nút
        self.project_manager = ProjectManager()
        
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
        
        # --- THÊM NÚT "NEW PROJECT" THEO SPRINT 1 ---
        self.btn_new_project = ctk.CTkButton(
            self.menu_frame,
            text="+ New Project",
            fg_color="#2E7D32",          # Màu xanh lá cây chuẩn của hệ màu Hex
            hover_color="#1B5E20",        # Màu xanh đậm hơn khi di chuột vào
            font=ctk.CTkFont(size=13, weight="bold"),
            command=self.show_new_project_dialog
        )
        self.btn_new_project.pack(padx=15, pady=(0, 15), fill="x")
        
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
        
        # Nhãn hiển thị nội dung ban đầu
        self.status_label = ctk.CTkLabel(
            self.content_frame, 
            text="Chọn một danh mục hoặc nhấn 'New Project' để bắt đầu", 
            font=ctk.CTkFont(size=14, italic=True)
        )
        self.status_label.pack(expand=True)

    def show_new_project_dialog(self):
        """
        Hộp thoại yêu cầu nhập 'Project Name' và gọi ProjectManager tự sinh thư mục
        """
        # Hiển thị hộp thoại nhập text của CustomTkinter
        dialog = ctk.CTkInputDialog(text="Nhập tên dự án mới (Project Name):", title="New Project")
        project_name = dialog.get_input()
        
        # Kiểm tra nếu người dùng nhấn nút OK và nhập tên hợp lệ
        if project_name:
            project_name = project_name.strip()
            if project_name == "":
                messagebox.showwarning("Cảnh báo", "Tên dự án không được để trống!")
                return
                
            try:
                # Gọi ProjectManager sinh ra toàn bộ 8 thư mục con và file project.json
                project_path = self.project_manager.create_project(project_name)
                
                # Cập nhật thông tin trực quan lên bảng điều khiển bên phải
                self.status_label.configure(
                    text=f" Khởi tạo thành công dự án: {project_name}\n\nThư mục lưu trữ tài nguyên:\n{project_path}",
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=("#2E7D32", "#81C784")
                )
                messagebox.showinfo("Thành công", f"Đã sinh cấu trúc thư mục tự động cho:\n{project_name}")
                
            except FileExistsError as e:
                messagebox.showerror("Lỗi", str(e))
            except Exception as e:
                messagebox.showerror("Lỗi hệ thống", f"Không thể tạo dự án: {e}")

    def on_category_click(self, category_name):
        """
        Hàm xử lý sự kiện khi người dùng click vào từng mục trên Dashboard
        """
        print(f"Đang mở khu vực quản lý: {category_name}")
        
        # Cập nhật tiêu đề hiển thị bên khung nội dung bên phải, reset lại màu chữ về mặc định
        self.status_label.configure(
            text=f"Giao diện quản lý [{category_name}] đang được tải...",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=("#000000", "#FFFFFF")
        )
        
        # Highlight nút đang chọn và bỏ chọn các nút khác
        for name, btn in self.buttons.items():
            if name == category_name:
                btn.configure(fg_color=("#3B8ED0", "#1F6AA5")) # Màu xanh đậm khi chọn
            else:
                btn.configure(fg_color="transparent") # Trả về nền trong suốt nếu không chọn
