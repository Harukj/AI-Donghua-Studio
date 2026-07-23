import customtkinter as ctk
from tkinter import messagebox
from database.session import SessionLocal
from services.character_service import CharacterService

class CharacterWindow(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        # Khởi tạo phiên kết nối Database và Service xử lý dữ liệu nhân vật
        self.db = SessionLocal()
        self.char_service = CharacterService(self.db)
        
        self.selected_character = None
        
        # Cấu hình Grid layout (Cột 0: Danh sách, Cột 1: Form chi tiết)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)
        
        # 1. KHU VỰC BÊN TRÁI: DANH SÁCH NHÂN VẬT
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.title_label = ctk.CTkLabel(
            self.left_frame, text="Character Bible", font=ctk.CTkFont(size=20, weight="bold")
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
        
        self.form_scroll = ctk.CTkScrollableFrame(self.right_frame, fg_color="transparent")
        self.form_scroll.pack(padx=15, pady=5, fill="both", expand=True)
        
        # Các trường dữ liệu tương ứng cấu hình bảng cơ sở dữ liệu
        self.fields = ["Tên", "Giới tính", "Tuổi", "Tóc", "Mắt", "Trang phục", "Tính cách", "Prompt Style", "Negative Prompt", "Ghi chú"]
        self.inputs = {}
        
        for field in self.fields:
            row_frame = ctk.CTkFrame(self.form_scroll, fg_color="transparent")
            row_frame.pack(fill="x", pady=4)
            
            lbl = ctk.CTkLabel(row_frame, text=field, width=120, anchor="w", font=ctk.CTkFont(size=13))
            lbl.pack(side="left", padx=5)
            
            if field in ["Trang phục", "Tính cách", "Negative Prompt", "Ghi chú"]:
                entry = ctk.CTkTextbox(row_frame, height=60, corner_radius=6)
            else:
                entry = ctk.CTkEntry(row_frame, placeholder_text=f"Nhập {field.lower()}...")
                
            entry.pack(side="left", fill="x", expand=True, padx=5)
            self.inputs[field] = entry
            
        # Nút bấm [ Save ] kích hoạt ghi dữ liệu thật xuống SQLite
        self.btn_save = ctk.CTkButton(
            self.right_frame, text="[ Save Profile ]", fg_color="#2E7D32", hover_color="#1B5E20",
            font=ctk.CTkFont(size=14, weight="bold"), command=self.save_character_profile
        )
        self.btn_save.pack(padx=20, pady=15, fill="x")
        
        # Nút bấm phụ để chạy thử Prompt Builder hiển thị kết quả chuỗi đã ghép
        self.btn_test_prompt = ctk.CTkButton(
            self.right_frame, text="⚡ Build Test Prompt AI", fg_color="#E65100", hover_color="#B64000",
            font=ctk.CTkFont(size=13, weight="bold"), command=self.test_prompt_generation
        )
        self.btn_test_prompt.pack(padx=20, pady=(0, 15), fill="x")
        
        # Nạp danh sách nhân vật thực tế từ database lên màn hình lúc khởi động
        self.refresh_character_list()

    def refresh_character_list(self):
        """Đọc dữ liệu thật từ bảng 'characters' trong SQLite để vẽ lên giao diện"""
        for widget in self.list_frame.winfo_children():
            widget.destroy()
            
        # Gọi trực tiếp qua SQLAlchemy session để quét toàn bộ bảng
        from database.models.character import CharacterModel
        db_characters = self.db.query(CharacterModel).all()
        
        if not db_characters:
            empty_lbl = ctk.CTkLabel(self.list_frame, text="Chưa có dữ liệu nhân vật.", text_color="gray")
            empty_lbl.pack(pady=10)
            return
            
        for char in db_characters:
            btn = ctk.CTkButton(
                self.list_frame, text=char.name, anchor="w", height=38,
                fg_color="transparent", text_color=("#000000", "#FFFFFF"),
                command=lambda name=char.name: self.load_character_profile(name)
            )
            btn.pack(fill="x", pady=2, padx=5)

    def load_character_profile(self, name):
        """Tìm hồ sơ nhân vật trong DB và điền ngược lại lên các ô nhập liệu của Form"""
        self.selected_character = name
        self.form_title.configure(text=f"Hồ sơ nhân vật: {name}")
        
        character = self.char_service.get_character_by_name(name)
        if not character:
            return
            
        # Xóa dữ liệu cũ
        for field, widget in self.inputs.items():
            if isinstance(widget, ctk.CTkTextbox):
                widget.delete("1.0", "end")
            else:
                widget.delete(0, "end")
                
        # Khôi phục dữ liệu từ Database lên form giao diện
        self.inputs["Tên"].insert(0, character.name or "")
        self.inputs["Giới tính"].insert(0, character.gender or "")
        self.inputs["Tuổi"].insert(0, character.age or "")
        self.inputs["Tóc"].insert(0, character.hair or "")
        self.inputs["Mắt"].insert(0, character.eyes or "")
        
        # Đối với trường Textbox cần ghi dữ liệu theo dạng chuỗi dòng
        self.inputs["Trang phục"].insert("1.0", character.clothes or "")
        self.inputs["Tính cách"].insert("1.0", character.personality or "")
        self.inputs["Prompt Style"].insert(0, character.style or "")
        self.inputs["Negative Prompt"].insert("1.0", character.negative_prompt or "")
        self.inputs["Ghi chú"].insert("1.0", character.notes or "")

    def open_add_character_dialog(self):
        """Hộp thoại thêm nhanh bản ghi nhân vật mới vào database"""
        dialog = ctk.CTkInputDialog(text="Nhập tên nhân vật mới cần khởi tạo:", title="Add Character")
        input_name = dialog.get_input()
        if input_name and input_name.strip() != "":
            name = input_name.strip()
            # Khởi tạo bản ghi thô vào cơ sở dữ liệu trước với trường ID dự án mặc định
            self.char_service.add_character({"Tên": name, "project_id": "default_proj"})
            self.refresh_character_list()
            self.load_character_profile(name)

    def save_character_profile(self):
        """Sự kiện cập nhật chỉnh sửa hoặc lưu mới thông số hồ sơ xuống file SQLite"""
        if not self.selected_character:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một nhân vật từ danh sách lề trái!")
            return
            
        form_data = {}
        for field, widget in self.inputs.items():
            if isinstance(widget, ctk.CTkTextbox):
                form_data[field] = widget.get("1.0", "end-1c").strip()
            else:
                form_data[field] = widget.get().strip()
                
        # Tiến hành cập nhật bản ghi hiện tại trong Database
        character = self.char_service.get_character_by_name(self.selected_character)
        if character:
            character.name = form_data.get("Tên")
            character.gender = form_data.get("Giới tính")
            character.age = form_data.get("Tuổi")
            character.hair = form_data.get("Tóc")
            character.eyes = form_data.get("Mắt")
            character.clothes = form_data.get("Trang phục")
            character.personality = form_data.get("Tính cách")
            character.style = form_data.get("Prompt Style")
            character.negative_prompt = form_data.get("Negative Prompt")
            character.notes = form_data.get("Ghi chú")
            
            self.db.commit()
            messagebox.showinfo("Thành công", f"Đã lưu hồ sơ nhân vật '{character.name}' vào Cơ sở dữ liệu an toàn!")
            self.refresh_character_list()

    def test_prompt_generation(self):
        """Hàm kiểm tra nhanh tính năng sinh câu lệnh tự động"""
        if not self.selected_character:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn một nhân vật để test!")
            return
        # Gọi qua Prompt Builder lõi dịch vụ để lấy chuỗi kết quả giống hệt ảnh mẫu của bạn
        ai_prompt = self.char_service.build_ai_prompt(self.selected_character)
        messagebox.showinfo("Prompt Builder Output", f"Đoạn Prompt AI tự động xuất ra cho Studio:\n\n{ai_prompt}")

    def __del__(self):
        # Đóng phiên kết nối cơ sở dữ liệu khi giải phóng giao diện để không bị rò rỉ bộ nhớ
        try:
            self.db.close()
        except:
            pass
