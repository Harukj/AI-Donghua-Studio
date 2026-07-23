import customtkinter as ctk

class EnvironmentForm(ctk.CTkFrame):
	def __init__(self, parent, save_callback):
		super().__init__(parent)
		self.save_callback = save_callback
		
		# Tiêu đề biểu mẫu
		self.form_title = ctk.CTkLabel(self, text="Hồ sơ chi tiết bối cảnh", font=ctk.CTkFont(size=18, weight="bold"))
		self.form_title.pack(padx=20, pady=15, anchor="w")
		
		# Khung cuộn chứa nội dung nhập liệu để tránh bị tràn màn hình
		self.form_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
		self.form_scroll.pack(padx=15, pady=5, fill="both", expand=True)
		
		# Cập nhật mảng danh sách trường chính xác 100% theo thứ tự trên hình ảnh của bạn
		self.fields = [
			"Tên",
			"Loại",
			"Prompt",
			"Negative Prompt",
			"Lighting",
			"Weather",
			"Time",
			"Default Camera",
			"Seed",
			"Thumbnail"
		]
		self.inputs = {}
		
		# Tự động sinh giao diện các ô nhập liệu
		for field in self.fields:
			row_frame = ctk.CTkFrame(self.form_scroll, fg_color="transparent")
			row_frame.pack(fill="x", pady=4)
			
			lbl = ctk.CTkLabel(row_frame, text=field, width=120, anchor="w", font=ctk.CTkFont(size=13))
			lbl.pack(side="left", padx=5)
			
			# Phân loại ô nhập văn bản dài (Textbox) và ô nhập dòng ngắn (Entry)
			if field in ["Prompt", "Negative Prompt"]:
				entry = ctk.CTkTextbox(row_frame, height=65, corner_radius=6)
			else:
				entry = ctk.CTkEntry(row_frame, placeholder_text=f"Nhập {field.lower()}...")
				
			entry.pack(side="left", fill="x", expand=True, padx=5)
			self.inputs[field] = entry
			
		# Nút bấm lưu trữ [ Save ] dưới cùng biểu mẫu
		self.btn_save = ctk.CTkButton(
			self, text="[ Save Environment ]", fg_color="#2E7D32", hover_color="#1B5E20",
			font=ctk.CTkFont(size=14, weight="bold"), command=self.on_save_clicked
		)
		self.btn_save.pack(padx=20, pady=15, fill="x")

	def clear_form(self):
		"""Xóa sạch nội dung cũ trên Form biểu mẫu"""
		for field, widget in self.inputs.items():
			if isinstance(widget, ctk.CTkTextbox):
				widget.delete("1.0", "end")
			else:
				widget.delete(0, "end")

	def on_save_clicked(self):
		"""Thu thập dữ liệu văn bản và kích hoạt Callback chuyển tiếp lệnh lưu"""
		form_data = {}
		for field, widget in self.inputs.items():
			if isinstance(widget, ctk.CTkTextbox):
				form_data[field] = widget.get("1.0", "end-1c").strip()
			else:
				form_data[field] = widget.get().strip()
		self.save_callback(form_data)
