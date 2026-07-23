import customtkinter as ctk
from gui.character.character_window import CharacterWindow

class Dashboard(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        # Cấu hình lưới (Grid layout): 2 cột (Cột 0 chứa thanh Menu điều hướng, Cột 1 chứa vùng nội dung)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=4)
        self.grid_rowconfigure(0, weight=1)
        
        # 1. KHU VỰC THANH MENU ĐIỀU HƯỚNG (Left Panel)
        self.menu_frame = ctk.CTkFrame(self, corner_radius=10)
        self.menu_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Tiêu đề ứng dụng phía trên Menu theo ảnh mẫu
        self.title_label = ctk.CTkLabel(
            self.menu_frame, 
            text="AI Donghua Studio", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.title_label.pack(padx=10, pady=20)
        
        # Danh sách các danh mục Menu được cập nhật chính xác theo đặc tả mới của ChatGPT
        self.categories = [
            "Project",
            "Characters",
            "Environment",
            "Camera",
            "Storyboard",
            "LTX Prompt",
            "Settings"
        ]
        
        # Tự động khởi tạo các nút bấm Menu điều hướng
        self.buttons = {}
        for cat in self.categories:
            btn = ctk.CTkButton(
                self.menu_frame,
                text=cat,
                anchor="w",                     # Căn chữ về lề trái
                height=40,
                corner_radius=6,
                font=ctk.CTkFont(size=13),
                command=lambda c=cat: self.on_category_click(c)
            )
            btn.pack(padx=15, pady=4, fill="x")
            self.buttons[cat] = btn

        # 2. KHU VỰC VÙNG HIỂN THỊ NỘI DUNG CHI TIẾT (Right Panel)
        self.content_frame = ctk.CTkFrame(self, corner_radius=10)
        self.content_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        # Nhãn thông báo trạng thái ban đầu khi mới bật ứng dụng lên
        self.status_label = ctk.CTkLabel(
            self.content_frame, 
            text="Chào mừng bạn đến với AI Donghua Studio.\nVui lòng chọn một danh mục ở thanh bên để bắt đầu làm việc.", 
            font=ctk.CTkFont(size=14, italic=True)
        )
        self.status_label.pack(expand=True)
        
        # Khởi tạo sẵn instance giao diện quản lý nhân vật để nhúng khi cần thiết
        self.character_view = None

    def on_category_click(self, category_name):
        """
        Hành động xử lý chuyển đổi phân hệ giao diện khi click vào từng nút bấm trên Menu
        """
        print(f"Hệ thống: Chuyển đổi trạng thái vùng nhìn sang [{category_name}]")
        
        # Highlight nút đang được lựa chọn và reset màu các nút còn lại
        for name, btn in self.buttons.items():
            if name == category_name:
                btn.configure(fg_color=("#3B8ED0", "#1F6AA5"))
            else:
                btn.configure(fg_color="transparent")
                
        # Xóa bỏ các Widget cũ đang hiển thị ở khung nội dung bên phải để chuẩn bị nạp giao diện mới
        for widget in self.content_frame.winfo_children():
            widget.pack_forget()  # Tạm ẩn hoặc xóa trạng thái xếp lớp cũ

        # LOGIC XỬ LÝ KHI NGƯỜI DÙNG BẤM VÀO "Characters" THEO ĐẶC TẢ TRONG ẢNH
        if category_name == "Characters":
            if self.character_view is None:
                # Khởi tạo giao diện CharacterWindow thực tế đã code ở các bước trước
                self.character_view = CharacterWindow(self.content_frame)
            
            # Nhúng toàn quyền khung quản lý Character Bible lấp đầy vùng content_frame bên phải
            self.character_view.pack(fill="both", expand=True, padx=10, pady=10)

        		# Mở file gui/dashboard.py, tìm tới hàm on_category_click và chèn đoạn code này vào ngay phía dưới khối "Environment":
		elif category_name == "Storyboard":
			from gui.storyboard.storyboard_window.py import StoryboardWindow
			# Khởi tạo và hiển thị khung nhìn kịch bản phân cảnh phim hoạt hình
			self.storyboard_view = StoryboardWindow(self.content_frame)
			self.storyboard_view.pack(fill="both", expand=True, padx=10, pady=10)

        elif category_name == "Environment":
            from gui.environment.environment_window import EnvironmentWindow
            self.environment_view = EnvironmentWindow(self.content_frame)
            self.environment_view.pack(fill="both", expand=True, padx=10, pady=10)

        else:
            # Đối với các danh mục khác chưa xây dựng giao diện chi tiết, hiển thị text thông báo tạm thời
            self.status_label.configure(
                text=f"Phân hệ chức năng [{category_name}] đang được thiết lập ở các Sprint tiếp theo.",
                font=ctk.CTkFont(size=15, weight="bold")
            )
            self.status_label.pack(expand=True)
        		# Mở file gui/dashboard.py, tìm tới hàm on_category_click và thêm đoạn này vào bên dưới phần xử lý "Characters":
     
