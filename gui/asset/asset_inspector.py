import customtkinter as ctk

class AssetInspector(ctk.CTkFrame):
	def __init__(self, parent, save_callback):
		super().__init__(parent, fg_color="transparent")
		self.save_callback = save_callback
		
		# Khung cuộn chứa nội dung để tránh tràn màn hình khi hiển thị nhiều thông số
		self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
		self.scroll_container.pack(fill="both", expand=True, padx=5, pady=5)
		
		# Tiêu đề bảng thuộc tính
		self.title_lbl = ctk.CTkLabel(self.scroll_container, text="Asset Inspector", font=ctk.CTkFont(size=16, weight="bold"), anchor="w")
		self.title_lbl.pack(fill="x", pady=10)

		# Định nghĩa các trường nhập liệu chính xác 100% theo sơ đồ của ChatGPT
		self.fields = [
			"Tên tài nguyên", "Portrait Path", "Prompt", "Negative Prompt", 
			"Seed", "Motion", "Voice", "Tags", "Reference Images", "History"
		]
		self.inputs = {}

		for field in self.fields:
			row_frame = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
			row_frame.pack(fill="x", pady=4)
			
			lbl = ctk.CTkLabel(row_frame, text=field, width=130, anchor="w", font=ctk.CTkFont(size=13))
			lbl.pack(side="left", padx=5)
			
			if field in ["Prompt", "Negative Prompt", "History"]:
				entry = ctk.CTkTextbox(row_frame, height=65, corner_radius=6)
			else:
				entry = ctk.CTkEntry(row_frame, placeholder_text=f"Thông số {field.lower()}...")
				
			entry.pack(side="left", fill="x", expand=True, padx=5)
			self.inputs[field] = entry

		# --- PHÂN KHU THƯƠNG MẠI: VERSION MANAGER ---
		self.version_frame = ctk.CTkFrame(self.scroll_container)
		self.version_frame.pack(fill="x", pady=15, padx=5)
		
		self.version_title = ctk.CTkLabel(self.version_frame, text="⚙️ Version Manager", font=ctk.CTkFont(size=13, weight="bold"), anchor="w")
		self.version_title.pack(fill="x", padx=10, pady=5)
		
		# Menu thả xuống chọn phiên bản tài nguyên (Ví dụ: v1.0, v2.0)
		self.version_menu = ctk.CTkOptionMenu(self.version_frame, values=["v1.0 - Default Profile", "v2.0 - Battle Costume"])
		self.version_menu.pack(fill="x", padx=15, pady=5)
		# --------------------------------------------

		# Nút bấm lưu cập nhật thuộc tính tài nguyên
		self.btn_save = ctk.CTkButton(
			self, text="[ Save Asset Metadata ]", fg_color="#2E7D32", hover_color="#1B5E20",
			font=ctk.CTkFont(size=14, weight="bold"), command=self.on_save_clicked
		)
		self.btn_save.pack(padx=10, pady=10, fill="x", side="bottom")

	def clear_inspector(self):
		"""Xóa sạch form cũ"""
		for field, widget in self.inputs.items():
			if isinstance(widget, ctk.CTkTextbox): widget.delete("1.0", "end")
			else: widget.delete(0, "end")

	def load_asset_to_inspector(self, name: str, folder_type: str):
		"""Nạp dữ liệu thực thể lên form cho người dùng xem và chỉnh sửa"""
		self.clear_inspector()
		self.title_lbl.configure(text=f"Inspector > {name}")
		
		# Điền dữ liệu giả lập thông minh khớp 100% với tệp mẫu Tô Mộc của bạn
		self.inputs["Tên tài nguyên"].insert(0, name)
		self.inputs["Portrait Path"].insert(0, f"projects/ToanDanTaoPhong/assets/{folder_type}/{name.lower()}.png")
		
		if folder_type == "characters":
			self.inputs["Prompt"].insert("1.0", f"Masterpiece, Chinese Donghua style, character {name}, 3D render")
			self.inputs["Seed"].insert(0, "23561")
			self.inputs["Voice"].insert(0, f"{name} AI Voice v1")
			self.inputs["Tags"].insert(0, "main_character, warrior, academy_uniform")
			self.inputs["History"].insert("1.0", "Initial creation on v1.0 architecture pipeline.")
			self.version_menu.configure(values=["v1.0 - Academy Uniform", "v2.0 - Battle Armor"])
		else:
			self.inputs["Prompt"].insert("1.0", f"Environment background of {name}")
			self.version_menu.configure(values=["v1.0 - Base Environment"])

	def on_save_clicked(self):
		form_data = {}
		for field, widget in self.inputs.items():
			if isinstance(widget, ctk.CTkTextbox): form_data[field] = widget.get("1.0", "end-1c").strip()
			else: form_data[field] = widget.get().strip()
		form_data["active_version"] = self.version_menu.get()
		self.save_callback(form_data)
