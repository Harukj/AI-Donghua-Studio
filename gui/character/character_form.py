import customtkinter as ctk

class CharacterForm(ctk.CTkFrame):
    def __init__(self, parent, save_callback):
        super().__init__(parent)
        self.save_callback = save_callback
        
        # Tiêu đề Form
        self.form_title = ctk.CTkLabel(
            self, text="Hồ sơ chi tiết nhân vật", font=ctk.CTkFont(size=18, weight="bold")
        )
        self.form_title.pack(padx=20, pady=15, anchor="w")
        
        # Khung cuộn chứa các trường nhập liệu
        self.form_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.form_scroll.pack(padx=15, pady=5, fill="both", expand=True)
        
        # Định nghĩa các trường dữ liệu theo danh sách thương mại
        self.fields = ["Tên", "Giới tính", "Tuổi", "Tóc", "Mắt", "Trang phục", "Tính cách", "Prompt Style", "Negative Prompt", "Ghi chú"]
        self.inputs = {}
        
        for field in self.fields:
            row_frame = ctk.CTkFrame(self.form_scroll, fg_color="transparent")
            row_frame.pack(fill="x", pady=4)
            
            lbl = ctk.CTkLabel(row_frame, text=field, width=110, anchor="w", font=ctk.CTkFont(size=13))
            lbl.pack(side="left", padx=5)
            
            if field in ["Trang phục", "Tính cách", "Negative Prompt", "Ghi chú"]:
                entry = ctk.CTkTextbox(row_frame, height=65, corner_radius=6)
            else:
                entry = ctk.CTkEntry(row_frame, placeholder_text=f"Nhập {field.lower()}...")
                
            entry.pack(side="left", fill="x", expand=True, padx=5)
            self.inputs[field] = entry
            
        # Nút bấm lưu trữ tích hợp
        self.btn_save = ctk.CTkButton(
            self, text="[ Save Profile ]", fg_color="#2E7D32", hover_color="#1B5E20",
            font=ctk.CTkFont(size=14, weight="bold"), command=self.on_save_clicked
        )
        self.btn_save.pack(padx=20, pady=15, fill="x")

    def clear_form(self):
        """Xóa trắng toàn bộ dữ liệu trên Form"""
        for field, widget in self.inputs.items():
            if isinstance(widget, ctk.CTkTextbox):
                widget.delete("1.0", "end")
            else:
                widget.delete(0, "end")

    def fill_form(self, character):
        """Điền dữ liệu từ bản ghi database vào Form"""
        self.clear_form()
        self.inputs["Tên"].insert(0, character.name or "")
        self.inputs["Giới tính"].insert(0, character.gender or "")
        self.inputs["Tuổi"].insert(0, character.age or "")
        self.inputs["Tóc"].insert(0, character.hair or "")
        self.inputs["Mắt"].insert(0, character.eyes or "")
        self.inputs["Trang phục"].insert("1.0", character.clothes or "")
        self.inputs["Tính cách"].insert("1.0", character.personality or "")
        self.inputs["Prompt Style"].insert(0, character.style or "")
        self.inputs["Negative Prompt"].insert("1.0", character.negative_prompt or "")
        self.inputs["Ghi chú"].insert("1.0", character.notes or "")

    def get_data(self) -> dict:
        """Thu thập toàn bộ dữ liệu người dùng đang nhập trên giao diện"""
        form_data = {}
        for field, widget in self.inputs.items():
            if isinstance(widget, ctk.CTkTextbox):
                form_data[field] = widget.get("1.0", "end-1c").strip()
            else:
                form_data[field] = widget.get().strip()
        return form_data

    def on_save_clicked(self):
        """Gọi hàm callback báo về lớp cha xử lý lưu"""
        data = self.get_data()
        self.save_callback(data)
