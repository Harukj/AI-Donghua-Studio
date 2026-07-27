import customtkinter as ctk

class ProductionDashboard(ctk.CTkFrame):
	def __init__(self, parent):
		super().__init__(parent, fg_color="transparent")
		
		# Tiêu đề giao diện tổng quan chuẩn hóa theo ảnh ChatGPT
		self.title_lbl = ctk.CTkLabel(self, text="Production Dashboard", font=ctk.CTkFont(size=18, weight="bold"))
		self.title_lbl.pack(padx=20, pady=15, anchor="w")
		
		# Khung hiển thị thông tin dự án phim cốt lõi
		self.info_card = ctk.CTkFrame(self, corner_radius=10)
		self.info_card.pack(fill="x", padx=20, pady=10)
		
		self.proj_name_lbl = ctk.CTkLabel(self.info_card, text="🎬 Dự án: Toàn Dân Tạo Mộng", font=ctk.CTkFont(size=15, weight="bold"))
		self.proj_name_lbl.pack(padx=20, pady=(15, 5), anchor="w")
		
		self.ep_num_lbl = ctk.CTkLabel(self.info_card, text="🎞️ Tiến trình sản xuất: Episode 15", font=ctk.CTkFont(size=13), text_color="gray")
		self.ep_num_lbl.pack(padx=20, pady=(0, 15), anchor="w")

		# Khay hiển thị trạng thái các bước phân khu kịch bản văn học (Novel Module)
		self.workflow_frame = ctk.CTkFrame(self)
		self.workflow_frame.pack(fill="both", expand=True, padx=20, pady=10)
		
		self.flow_title = ctk.CTkLabel(self.workflow_frame, text="Bảng điều phối mạch sản xuất tự động", font=ctk.CTkFont(size=14, weight="bold"))
		self.flow_title.pack(padx=15, pady=10, anchor="w")
		
		# Trực quan hóa các chỉ số thống kê
		steps = [
			("[✓] Novel Chapter 15 Loaded", "Đã nạp xong văn bản truyện chữ thô"),
			("[✓] AI Scene Analysis Completed", "AI đã phân rã thành công 42 phân cảnh điện ảnh"),
			("[ ] Render Queue Status", "Hàng đợi xếp hàng chờ kết xuất clip... (0/42 Scenes)")
		]
		for status, desc in steps:
			row = ctk.CTkFrame(self.workflow_frame, fg_color="transparent")
			row.pack(fill="x", padx=20, pady=4)
			
			lbl_stat = ctk.CTkLabel(row, text=status, width=220, anchor="w", font=ctk.CTkFont(weight="bold"))
			lbl_stat.pack(side="left")
			
			lbl_desc = ctk.CTkLabel(row, text=f"|  {desc}", text_color="gray")
			lbl_desc.pack(side="left", padx=10)
