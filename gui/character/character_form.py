import customtkinter as ctk
from PIL import Image
import os

class CharacterForm(ctk.CTkFrame):
	def __init__(self, parent, save_callback):
		super().__init__(parent)
		self.save_callback = save_callback
		
		# Tiêu đề Form chính
		self.form_title = ctk.CTkLabel(self, text="Hồ sơ chi tiết nhân vật", font=ctk.CTkFont(size=18, weight="bold"))
		self.form_title.pack(padx=20, pady=15, anchor="w")
		
		# Khung cuộn chứa nội dung hồ sơ nhân vật
		self.form_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
		self.form_scroll.pack(padx=15, pady=5, fill="both", expand=True)
		
		# --- BỔ SUNG PHÂN KHU HIỂN THỊ PORTRAIT (ẢNH CHÂN DUNG) THEO MẪU ---
		self.portrait_frame = ctk.CTkFrame(self.form_scroll, fg_color="transparent")
		self.portrait_frame.pack(fill="x", pady=(0, 15))
		
		# Nhãn chữ "Portrait" làm tiêu đề phân khu ảnh đại diện
		self.portrait_lbl = ctk.CTkLabel(self.portrait_frame, text="Portrait", width=120, anchor="w", font=ctk.CTkFont(size=13, weight="bold"))
		self.portrait_lbl.pack(side="left", padx=5)
		
		# Khung hộp chứa ảnh đại diện giả lập (Kích thước hình vuông chuẩn avatar)
		self.image_box = ctk.CTkLabel(
			self.portrait_frame, 
			text="[ No Image ]", 
			width=100, 
			height=100, 
			fg_color=("#E0E0E0", "#2B2B2B"),
			corner_radius=6
		)
		self.image_box.pack(side="left", padx=5)
		
		# Nút bấm hỗ trợ người dùng nhấn chọn tải ảnh từ máy tính lên
		self.btn_browse_image = ctk.CTkButton(
			self.portrait_frame, text="Tải ảnh lên...", width=100, height=30, fg_color="gray",
			command=self.browse_character_image
		)
		self.btn_browse_image.pack(side="left", padx=10, anchor="s")
		# ------------------------------------------------------------------

			   # Cập nhật danh sách trường chính xác theo đúng hình ảnh mới nhất từ ChatGPT
		self.fields = [
			"Tên", 
			"Biệt danh", 
			"Tuổi", 
			"Chiều cao", 
			"Màu tóc", 
			"Màu mắt", 
			"Trang phục", 
			"Vũ khí", 
			"Tính cách", 
			"Positive Prompt", 
			"Negative Prompt", 
			"Seed"
		]

		self.inputs = {}
		
		for field in self.fields:
			row_frame = ctk.CTkFrame(self.form_scroll, fg_color="transparent")
			row_frame.pack(fill="x", pady=4)
			
			lbl = ctk.CTkLabel(row_frame, text=field, width=120, anchor="w", font=ctk.CTkFont(size=13))
			lbl.pack(side="left", padx=5)
			
			if field in ["Trang phục", "Tính cách", "Positive Prompt", "Negative Prompt", "Ghi chú"]:
				entry = ctk.CTkTextbox(row_frame, height=65, corner_radius=6)
			else:
				entry = ctk.CTkEntry(row_frame, placeholder_text=f"Nhập {field.lower()}...")
				
			entry.pack(side="left", fill="x", expand=True, padx=5)
			self.inputs[field] = entry
			
		self.btn_save = ctk.CTkButton(
			self, text="[ Save Profile ]", fg_color="#2E7D32", hover_color="#1B5E20",
			font=ctk.CTkFont(size=14, weight="bold"), command=self.on_save_clicked
		)
		self.btn_save.pack(padx=20, pady=15, fill="x")

	def browse_character_image(self):
			"""Hàm xử lý khi nhấn nút Import Portrait theo đúng thiết kế của ChatGPT"""
			from tkinter import filedialog
			from core.project_manager import ProjectManager
			
			# 1. Cho người dùng chọn file ảnh từ máy tính
			file_path = filedialog.askopenfilename(
				filetypes=[("Image Files", "*.png *.jpg *.jpeg *.webp")]
			)
			
			if file_path:
				try:
					# 2. Khởi tạo ProjectManager để thực hiện sao chép tệp tin
					pm = ProjectManager()
					
					# Tạm thời lấy tên dự án mặc định là "ToanDanTaoPhong" như ảnh mẫu của bạn
					# Sau này khi làm phân hệ Project bạn sẽ truyền tên dự án đang mở vào đây
					current_project = "ToanDanTaoPhong" 
					
					# 3. Sao chép ảnh vào thư mục dự án và lấy đường dẫn đích
					saved_path = pm.save_character_image(current_project, file_path)
					
					# 4. Ghi đường dẫn tệp tin vào ô nhập liệu 'Ảnh đại diện' hoặc biến lưu trữ
					if "Ảnh đại diện" in self.inputs:
						self.inputs["Ảnh đại diện"].delete(0, "end")
						self.inputs["Ảnh đại diện"].insert(0, saved_path)
					
					# 5. Cập nhật ảnh hiển thị trực quan (Preview) lên khung hình
					self.load_portrait_preview(saved_path)
					
					print(f"Hệ thống: Đã copy ảnh vào {saved_path} và chuẩn bị lưu đường dẫn vào DB.")
					
				except Exception as e:
					from tkinter import messagebox
					messagebox.showerror("Lỗi Import", f"Không thể sao chép tệp tin ảnh: {e}")
	
	def load_portrait_preview(self, img_path):
		"""Hàm xử lý đọc file ảnh bằng Pillow và vẽ bản xem trước (Preview) lên giao diện"""
		if img_path and os.path.exists(img_path):
			try:
				pil_img = Image.open(img_path)
				ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(100, 100))
				self.image_box.configure(image=ctk_img, text="")
			except Exception as e:
				self.image_box.configure(image=None, text="[ Error Image ]")
		else:
			self.image_box.configure(image=None, text="[ No Image ]")

	def clear_form(self):
		self.image_box.configure(image=None, text="[ No Image ]")
		for field, widget in self.inputs.items():
			if isinstance(widget, ctk.CTkTextbox):
				widget.delete("1.0", "end")
			else:
				widget.delete(0, "end")

	def fill_form(self, character):
		self.clear_form()
		self.inputs["Tên"].insert(0, character.name or "")
		self.inputs["Biệt danh"].insert(0, character.alias or "")
		self.inputs["Giới tính"].insert(0, character.gender or "")
		self.inputs["Tuổi"].insert(0, character.age or "")
		self.inputs["Chiều cao"].insert(0, character.height or "")
		self.inputs["Cân nặng"].insert(0, character.weight or "")
		self.inputs["Tóc"].insert(0, character.hair or "")
		self.inputs["Mắt"].insert(0, character.eyes or "")
		self.inputs["Khuôn mặt"].insert(0, character.face or "")
		self.inputs["Màu da"].insert(0, character.skin or "")
		self.inputs["Trang phục"].insert("1.0", character.costume or "")
		self.inputs["Vũ khí"].insert(0, character.weapon or "")
		self.inputs["Tính cách"].insert("1.0", character.personality or "")
		self.inputs["Giọng nói"].insert(0, character.voice or "")
		self.inputs["Style"].insert(0, character.style or "")
		self.inputs["Positive Prompt"].insert("1.0", character.positive_prompt or "")
		self.inputs["Negative Prompt"].insert("1.0", character.negative_prompt or "")
		self.inputs["Mã Seed"].insert(0, character.seed or "")
		self.inputs["Ảnh đại diện"].insert(0, character.image or "")
		self.inputs["Ghi chú"].insert("1.0", character.notes or "")
		
		# Tải ảnh chân dung xem trước lên hộp hiển thị nếu hồ sơ có sẵn đường dẫn ảnh
		if character.image:
			self.load_portrait_preview(character.image)

	def get_data(self) -> dict:
		form_data = {}
		for field, widget in self.inputs.items():
			if isinstance(widget, ctk.CTkTextbox):
				form_data[field] = widget.get("1.0", "end-1c").strip()
			else:
				form_data[field] = widget.get().strip()
		return form_data

	def on_save_clicked(self):
		data = self.get_data()
		self.save_callback(data)
