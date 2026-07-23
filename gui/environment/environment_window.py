import customtkinter as ctk
from tkinter import messagebox
from database.session import SessionLocal
from services.environment_service import EnvironmentService

class EnvironmentWindow(ctk.CTkFrame):
	def __init__(self, parent):
		super().__init__(parent, fg_color="transparent")
		
		# Khởi tạo kết nối cơ sở dữ liệu và service bối cảnh
		self.db = SessionLocal()
		self.env_service = EnvironmentService(self.db)
		self.selected_env = None
		
		# Thiết lập bố cục lưới 2 phân vùng (Trái: Danh sách bối cảnh, Phải: Form thông số)
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=2)
		self.grid_rowconfigure(0, weight=1)
		
		# 1. PHÂN VÙNG BÊN TRÁI: DANH SÁCH BỐI CẢNH (ENVIRONMENT LIBRARY)
		self.left_frame = ctk.CTkFrame(self)
		self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
		
		self.title_label = ctk.CTkLabel(
			self.left_frame, text="Environment Library", font=ctk.CTkFont(size=18, weight="bold")
		)
		self.title_label.pack(padx=15, pady=15, anchor="w")
		
		self.btn_add_env = ctk.CTkButton(
			self.left_frame, text="+ Add Environment", fg_color="#1F6AA5",
			font=ctk.CTkFont(size=13, weight="bold"), command=self.open_add_env_dialog
		)
		self.btn_add_env.pack(padx=15, pady=5, fill="x")
		
		self.separator = ctk.CTkLabel(self.left_frame, text="----------------------------------------", text_color="gray")
		self.separator.pack(padx=15, pady=5)
		
		self.list_frame = ctk.CTkScrollableFrame(self.left_frame, fg_color="transparent")
		self.list_frame.pack(padx=10, pady=5, fill="both", expand=True)
		
		# 2. PHÂN VÙNG BÊN PHẢI: FORM CẤU HÌNH THÔNG SỐ ĐIỆN ẢNH
		self.right_frame = ctk.CTkFrame(self)
		self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
		
		self.form_title = ctk.CTkLabel(
			self.right_frame, text="Thông số không gian", font=ctk.CTkFont(size=18, weight="bold")
		)
		self.form_title.pack(padx=20, pady=15, anchor="w")
		
		self.form_scroll = ctk.CTkScrollableFrame(self.right_frame, fg_color="transparent")
		self.form_scroll.pack(padx=15, pady=5, fill="both", expand=True)
		
		# Các thuộc tính bối cảnh khớp hoàn toàn với thiết kế của Sprint kế tiếp
		self.fields = ["Tên bối cảnh", "Thời gian (Time)", "Thời tiết (Weather)", "Phong cách kiến trúc", "Prompt mô tả cảnh", "Style", "Negative Prompt"]
		self.inputs = {}
		
		for field in self.fields:
			row_frame = ctk.CTkFrame(self.form_scroll, fg_color="transparent")
			row_frame.pack(fill="x", pady=4)
			
			lbl = ctk.CTkLabel(row_frame, text=field, width=130, anchor="w", font=ctk.CTkFont(size=13))
			lbl.pack(side="left", padx=5)
			
			if field in ["Prompt mô tả cảnh", "Negative Prompt"]:
				entry = ctk.CTkTextbox(row_frame, height=70, corner_radius=6)
			else:
				entry = ctk.CTkEntry(row_frame, placeholder_text=f"Nhập {field.lower()}...")
				
			entry.pack(side="left", fill="x", expand=True, padx=5)
			self.inputs[field] = entry
			
		# Nút lưu thông tin bối cảnh
		self.btn_save = ctk.CTkButton(
			self.right_frame, text="[ Save Environment ]", fg_color="#2E7D32", hover_color="#1B5E20",
			font=ctk.CTkFont(size=14, weight="bold"), command=self.save_environment_profile
		)
		self.btn_save.pack(padx=20, pady=15, fill="x")
		
		# Tải dữ liệu bối cảnh từ database lên UI khi khởi động
		self.refresh_env_list()

	def refresh_env_list(self):
		"""Quét bảng 'environments' trong file SQLite để đưa danh sách lên UI lề trái"""
		for widget in self.list_frame.winfo_children():
			widget.destroy()
			
		from database.models.environment import EnvironmentModel
		db_envs = self.db.query(EnvironmentModel).all()
		
		if not db_envs:
			empty_lbl = ctk.CTkLabel(self.list_frame, text="Chưa có dữ liệu bối cảnh.", text_color="gray")
			empty_lbl.pack(pady=10)
			return
			
		for env in db_envs:
			btn = ctk.CTkButton(
				self.list_frame, text=env.name, anchor="w", height=38,
				fg_color="transparent", text_color=("#000000", "#FFFFFF"),
				command=lambda n=env.name: self.load_environment_profile(n)
			)
			btn.pack(fill="x", pady=2, padx=5)

	def load_environment_profile(self, name):
		"""Đọc thông tin chi tiết từ DB đưa ngược lên các ô nhập liệu"""
		self.selected_env = name
		self.form_title.configure(text=f"Bối cảnh: {name}")
		
		env = self.env_service.get_env_by_name(name)
		if not env:
			return
			
		# Xóa dữ liệu cũ trên form
		for field, widget in self.inputs.items():
			if isinstance(widget, ctk.CTkTextbox):
				widget.delete("1.0", "end")
			else:
				widget.delete(0, "end")
				
		# Điền dữ liệu thật
		self.inputs["Tên bối cảnh"].insert(0, env.name or "")
		self.inputs["Thời gian (Time)"].insert(0, env.time_of_day or "")
		self.inputs["Thời tiết (Weather)"].insert(0, env.weather or "")
		self.inputs["Phong cách kiến trúc"].insert(0, env.architecture_style or "")
		self.inputs["Prompt mô tả cảnh"].insert("1.0", env.description_prompt or "")
		self.inputs["Style"].insert(0, env.style or "")
		self.inputs["Negative Prompt"].insert("1.0", env.negative_prompt or "")

	def open_add_env_dialog(self):
		"""Hộp thoại thêm nhanh bối cảnh mẫu"""
		dialog = ctk.CTkInputDialog(text="Nhập tên bối cảnh mới (Ví dụ: Long Dang City):", title="Add Environment")
		input_name = dialog.get_input()
		if input_name and input_name.strip() != "":
			name = input_name.strip()
			# Khởi tạo bản ghi thô vào database
			self.env_service.add_environment({"name": name})
			self.refresh_env_list()
			self.load_environment_profile(name)

	def save_environment_profile(self):
		"""Sự kiện lưu dữ liệu bối cảnh xuống SQLite"""
		if not self.selected_env:
			messagebox.showwarning("Cảnh báo", "Vui lòng chọn một bối cảnh để lưu!")
			return
			
		form_data = {}
		for field, widget in self.inputs.items():
			if isinstance(widget, ctk.CTkTextbox):
				form_data[field] = widget.get("1.0", "end-1c").strip()
			else:
				form_data[field] = widget.get().strip()
				
		env = self.env_service.get_env_by_name(self.selected_env)
		if env:
			env.name = form_data.get("Tên bối cảnh")
			env.time_of_day = form_data.get("Thời gian (Time)")
			env.weather = form_data.get("Thời tiết (Weather)")
			env.architecture_style = form_data.get("Phong cách kiến trúc")
			env.description_prompt = form_data.get("Prompt mô tả cảnh")
			env.style = form_data.get("Style")
			env.negative_prompt = form_data.get("Negative Prompt")
			
			self.db.commit()
			messagebox.showinfo("Sprint 4", f"Đã cập nhật thư viện bối cảnh: '{env.name}'")
			self.refresh_env_list()

	def __del__(self):
		try: self.db.close()
		except: pass
