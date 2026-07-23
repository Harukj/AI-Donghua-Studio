import customtkinter as ctk
from tkinter import messagebox

class CharacterWindow(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        # Grid layout: Cột 0 là Danh sách nhân vật, Cột 1 là Form chi tiết hồ sơ
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)
        
        # Dữ liệu mẫu nhân vật ban đầu
        self.mock_characters = ["Tô Mộc", "Lâm Thanh", "Diệp Trường Sinh", "Triệu Thiên"]
        self.selected_character = None
        
        # 1. KHU VỰC BÊN TRÁI: DANH SÁCH NHÂN VẬT
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.title_label = ctk.CTkLabel(
            self.left_frame, text="Characters", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(padx=15, pady=15, anchor="w")
        
        self.btn_add_character = ctk.CTkButton(
            self.left_frame, text="+ Add Character", fg_color="#1F6AA5",
            font=ctk.CTkFont(size=13, weight="bold"), command=self.open_add_character_dialog
        )
        self.btn_add_character.pack(padx=15, pady=5, fill="x")
        
        self.separator = ctk.CTkLabel(self.left_frame, text="----------------------------------------", text_color="gray")
        self.separator.pack(padx=15, pady=5)
        
        self.list_frame = ctk.CTkScrollableFrame(self.left_frame, fg_color="transparent")
        self.list_frame.pack(padx=10, pady=5, fill="both", expand=True)
        
        # 2. KHU VỰC BÊN PHẢI: FORM CHI TIẾT HỒ SƠ
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.form_title = ctk.CTkLabel(
            self.right_frame, text="Hồ sơ chi tiết", font=ctk.CTkFont(size=18, weight="bold")
        )
        self.form_title.pack(padx=20, pady=15, anchor="w")
        
        # Khung cuộn chứa các ô nhập liệu của Form để không bị tràn màn hình
        self.form_scroll = ctk.CTkScrollableFrame(self.right_frame, fg_color="transparent")
        self.form_scroll.pack(padx=15, pady=5, fill="both", expand=True)
        
        # Tự động sinh các trường nhập liệu theo danh sách của ChatGPT
        self.fields = ["Tên", "Giới tính", "Tuổi", "Tóc", "Mắt", "Trang phục", "Tính cách", "Prompt Style", "Negative Prompt", "Ghi chú"]
        self.inputs = {}
        
        for field in self.fields:
            # Container cho mỗi hàng thông tin
            row_frame = ctk.CTkFrame(self.form_scroll, fg_color="transparent")
            row_frame.pack(fill="x", pady=4)
            
            lbl = ctk.CTkLabel(row_frame, text=field, width=120, anchor="w", font=ctk.CTkFont(size=13))
            lbl.pack(side="left", padx=5)
            
            # Sử dụng Textbox cho các trường mô tả dài, Entry cho trường ngắn
            if field in ["Trang phục", "Tính cách", "Negative Prompt", "Ghi chú"]:
                entry = ctk.CTkTextbox(row_frame, height=60, corner_radius=6)
            else:
                entry = ctk.CTkEntry(row_frame, placeholder_text=f"Nhập {field.lower()}...")
                
            entry.pack(side="left", fill="x", expand=True, padx=5)
            self.inputs[field] = entry
            
        # Nút bấm [ Save ] lưu thông tin xuống dưới cùng của form
        self.btn_save = ctk.CTkButton(
            self.right_frame, text="[ Save ]", fg_color="#2E7D32", hover_color="#1B5E20",
            font=ctk.CTkFont(size=14, weight="bold"), command=self.save_character_profile
        )
        self.btn_save.pack(padx=20, pady=15, fill="x")
        
        # Vẽ danh sách nhân vật ban đầu lên màn hình trái
        self.render_character_list()

    def render_character_list(self):
        """Vẽ danh sách nút bấm nhân vật bên lề trái"""
        for widget in self.list_frame.winfo_children():
            widget.destroy()
            
        for char_name in self.mock_characters:
            btn = ctk.CTkButton(
                self.list_frame, text=char_name, anchor="w", height=38,
                fg_color="transparent", text_color=("#000000", "#FFFFFF"),
                command=lambda name=char_name: self.load_character_profile(name)
            )
            btn.pack(fill="x", pady=2, padx=5)

    def load_character_profile(self, name):
        """Hàm xử lý khi click vào tên một nhân vật: Hiển thị tên lên tiêu đề và xóa trắng form chuẩn bị nhập liệu"""
        self.selected_character = name
        self.form_title.configure(text=f"Hồ sơ nhân vật: {name}")
        print(f"Đang xem hồ sơ: {name}")
        
        # Xóa sạch dữ liệu cũ trên các ô nhập liệu
        for field, widget in self.inputs.items():
            if isinstance(widget, ctk.CTkTextbox):
                widget.delete("1.0", "end")
            else:
                widget.delete(0, "end")
                
        # Tự động điền trường tên nhân vật vào ô nhập liệu 'Tên'
        self.inputs["Tên"].insert(0, name)

    def open_add_character_dialog(self):
        """Thêm nhanh một nhân vật mới vào danh sách bên trái"""
        dialog = ctk.CTkInputDialog(text="Nhập tên nhân vật mới:", title="Add Character")
        input_name = dialog.get_input()
        if input_name and input_name.strip() != "":
            self.mock_characters.append(input_name.strip())
            self.render_character_list()

    def save_character_profile(self):
        """Xử lý sự kiện khi nhấn nút [ Save ]"""
        if not self.selected_character:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một nhân vật từ danh sách trước khi lưu!")
            return
            
        # Thu thập toàn bộ văn bản người dùng vừa điền trên Form để chuẩn bị đẩy vào Database
        form_data = {}
        for field, widget in self.inputs.items():
            if isinstance(widget, ctk.CTkTextbox):
                form_data[field] = widget.get("1.0", "end-1c").strip()
            else:
                form_data[field] = widget.get().strip()
                
        print("Dữ liệu thu thập để lưu:", form_data)
        messagebox.showinfo("Thành công", f"Đã lưu thông tin chi tiết hồ sơ nhân vật: {form_data['Tên']}")
