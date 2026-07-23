import customtkinter as ctk
from tkinter import messagebox
from database.session import SessionLocal
from services.character_service import CharacterService
from gui.character.character_form import CharacterForm  # Import lớp form vừa tách

class CharacterWindow(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        self.db = SessionLocal()
        self.char_service = CharacterService(self.db)
        self.selected_character = None
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)
        
        # 1. PHÂN HỆ TRÁI: QUẢN LÝ DANH SÁCH
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.title_label = ctk.CTkLabel(
            self.left_frame, text="Character Bible v0.3", font=ctk.CTkFont(size=18, weight="bold")
        )
        self.title_label.pack(padx=15, pady=15, anchor="w")
        
        self.btn_add = ctk.CTkButton(
            self.left_frame, text="+ Add Character", fg_color="#1F6AA5", command=self.open_add_dialog
        )
        self.btn_add.pack(padx=15, pady=5, fill="x")
        
        self.list_frame = ctk.CTkScrollableFrame(self.left_frame, fg_color="transparent")
        self.list_frame.pack(padx=10, pady=5, fill="both", expand=True)
        
        # 2. PHÂN HỆ PHẢI: NHÚNG FORM ĐỘC LẬP
        # Truyền hàm 'self.save_character_profile' làm hành động callback khi nhấn lưu trên Form
        self.character_form = CharacterForm(self, save_callback=self.save_character_profile)
        self.character_form.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.refresh_character_list()

    def refresh_character_list(self):
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        from database.models.character import CharacterModel
        db_characters = self.db.query(CharacterModel).all()
        for char in db_characters:
            btn = ctk.CTkButton(
                self.list_frame, text=char.name, anchor="w", height=38, fg_color="transparent",
                text_color=("#000000", "#FFFFFF"), command=lambda n=char.name: self.load_character_profile(n)
            )
            btn.pack(fill="x", pady=2, padx=5)

    def load_character_profile(self, name):
        self.selected_character = name
        character = self.char_service.get_character_by_name(name)
        if character:
            # Ủy quyền cho form tự điền thông tin lên giao diện
            self.character_form.form_title.configure(text=f"Hồ sơ: {name}")
            self.character_form.fill_form(character)

    def open_add_dialog(self):
        dialog = ctk.CTkInputDialog(text="Tên nhân vật thương mại mới:", title="Add Character")
        input_name = dialog.get_input()
        if input_name and input_name.strip() != "":
            name = input_name.strip()
            self.char_service.add_character({"Tên": name, "project_id": "com_project"})
            self.refresh_character_list()
            self.load_character_profile(name)

    def save_character_profile(self, form_data):
        """Hàm nhận dữ liệu được trả về từ CharacterForm và tiến hành cập nhật SQLite"""
        if not self.selected_character:
            return
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
            messagebox.showinfo("Studio Commercial", f"Đã đồng bộ cấu trúc hồ sơ '{character.name}' vào hệ thống!")
            self.refresh_character_list()

    def __del__(self):
        try: self.db.close()
        except: pass
