import customtkinter as ctk
from tkinter import messagebox

class ExportWindow(ctk.CTkFrame):
	def __init__(self, parent):
		super().__init__(parent, fg_color="transparent")
		
		# Thiết lập bố cục lưới (Cột 0: Thông tin metadata, Cột 1: Xem trước & Xuất bản)
		self.grid_columnconfigure(0, weight=1)
		self.grid_columnconfigure(1, weight=1)
		self.grid_rowconfigure(0, weight=1)

		# 1. PHÂN VÙNG BÊN TRÁI: HỒ SƠ METADATA XUẤT PHIM (Chuẩn 5 thành phần của ChatGPT)
		self.left_panel = ctk.CTkFrame(self)
		self.left_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
		
		self.title_lbl = ctk.CTkLabel(self.left_panel, text="YouTube Export Manager", font=ctk.CTkFont(size=18, weight="bold"))
		self.title_lbl.pack(padx=20, pady=15, anchor="w")
		
		self.episode_lbl = ctk.CTkLabel(self.left_panel, text="Target: Episode 01", font=ctk.CTkFont(size=14, weight="medium", slant="italic"), text_color="gray")
		self.episode_lbl.pack(padx=20, pady=(0, 10), anchor="w")
		
		# Khung cuộn chứa biểu mẫu nhập liệu metadata
		self.form_scroll = ctk.CTkScrollableFrame(self.left_panel, fg_color="transparent")
		self.form_scroll.pack(fill="both", expand=True, padx=10, pady=5)
		
		# Khởi tạo chuẩn xác 5 trường dữ liệu theo ảnh mẫu
		self.fields = ["Video File Path", "Thumbnail Image", "Subtitle (.srt)", "Description", "SEO Tags"]
		self.inputs = {}
		
		for field in self.fields:
			row_frame = ctk.CTkFrame(self.form_scroll, fg_color="transparent")
			row_frame.pack(fill="x", pady=5)
			
			lbl = ctk.CTkLabel(row_frame, text=field, width=130, anchor="w", font=ctk.CTkFont(size=13, weight="bold"))
			lbl.pack(side="left", padx=5)
			
			if field == "Description":
				entry = ctk.CTkTextbox(row_frame, height=80, corner_radius=6)
			else:
				entry = ctk.CTkEntry(row_frame, placeholder_text=f"Đường dẫn hoặc nội dung {field.lower()}...")
				
			entry.pack(side="left", fill="x", expand=True, padx=5)
			self.inputs[field] = entry

		# Nạp dữ liệu giả lập thương mại để kiểm tra giao diện trực quan
		self.load_mock_metadata()

		# 2. PHÂN VÙNG BÊN PHẢI: KHÔNG GIAN BẤM LỆNH KẾT XUẤT VÀ PUBLISH YOUTUBE
		self.right_panel = ctk.CTkFrame(self)
		self.right_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
		
		self.workspace_lbl = ctk.CTkLabel(self.right_panel, text="Production Workspace", font=ctk.CTkFont(size=16, weight="bold"))
		self.workspace_lbl.pack(padx=20, pady=20, anchor="w")
		
		self.status_box = ctk.CTkTextbox(self.right_panel, height=200, corner_radius=6)
		self.status_box.pack(fill="x", padx=20, pady=10)
		self.status_box.insert("1.0", "Hệ thống Engine đã gộp 3 Phân cảnh thành công.\nSẵn sàng kích hoạt lệnh Final Render...\n")
		self.status_box.configure(state="disabled")
		
		# Nút bấm 1: Khởi chạy lệnh gộp tệp tin [ Final Render Movie ]
		self.btn_render = ctk.CTkButton(
			self.right_panel, text="🎬 [ Final Render Movie (.mp4) ]", fg_color="#E65100", hover_color="#BF360C",
			font=ctk.CTkFont(size=13, weight="bold"), command=self.execute_final_render
		)
		self.btn_render.pack(fill="x", padx=20, pady=10)
		
		# Nút bấm 2: Tự động tải lên mạng xã hội theo sơ đồ [ Upload to YouTube ]
		self.btn_upload = ctk.CTkButton(
			self.right_panel, text="🚀 [ Upload to YouTube Channel ]", fg_color="#C62828", hover_color="#B71C1C",
			font=ctk.CTkFont(size=13, weight="bold"), command=self.execute_youtube_upload
		)
		self.btn_upload.pack(fill="x", padx=20, pady=10)

	def load_mock_metadata(self):
		"""Nạp dữ liệu mẫu tự động điền để kiểm thử giao diện"""
		self.inputs["Video File Path"].insert(0, "projects/ToanDanTaoPhong/exports/episode_01_final.mp4")
		self.inputs["Thumbnail Image"].insert(0, "projects/ToanDanTaoPhong/assets/reference_images/thumb_ep1.png")
		self.inputs["Subtitle (.srt)"].insert(0, "projects/ToanDanTaoPhong/episode_01/subtitles/episode_01.srt")
		self.inputs["SEO Tags"].insert(0, "donghua 3d, hoat hinh trung quoc, ai movie, toan dan tao mong, ltx studio")
		self.inputs["Description"].insert("1.0", "Phim hoạt hình 3D Donghua: Toàn Dân Tạo Mộng - Tập 1\nSản xuất tự động bằng hệ thống AI Donghua Studio Engine v1.0.\n\nBản quyền thuộc về Harukj Studio 2026.")

	def execute_final_render(self):
		messagebox.showinfo("Export System", "Bắt đầu luồng gộp Video + Audio + Subtitle thương mại!\nTệp tin phim hoàn chỉnh đang được xuất bản vào thư mục 'exports/'.")

	def execute_youtube_upload(self):
		messagebox.showinfo("YouTube API", "Đã kích hoạt luồng kết nối OAuth2 API!\nĐang tự động đồng bộ đẩy Video, Phụ đề và SEO Tags lên kênh YouTube của bạn.")
