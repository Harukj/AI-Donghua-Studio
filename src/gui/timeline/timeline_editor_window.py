import customtkinter as ctk
from tkinter import messagebox

class TimelineEditorWindow(ctk.CTkFrame):
	def __init__(self, parent):
		super().__init__(parent, fg_color="transparent")
		
		# Thiết lập bố cục lưới chính (Cột 0: Timeline lề trái, Cột 1: Shot Preview lề phải)
		self.grid_columnconfigure(0, weight=3)
		self.grid_columnconfigure(1, weight=1)
		self.grid_rowconfigure(0, weight=1)

		# 1. PHÂN KHU BÊN TRÁI: TIMELINE EDITOR (GIỐNG ADOBE PREMIERE)
		self.timeline_panel = ctk.CTkFrame(self)
		self.timeline_panel.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
		
		self.lbl_timeline_title = ctk.CTkLabel(self.timeline_panel, text="Timeline Editor (Premiere Style)", font=ctk.CTkFont(size=16, weight="bold"))
		self.lbl_timeline_title.pack(padx=20, pady=15, anchor="w")
		
		self.timeline_scroll = ctk.CTkScrollableFrame(self.timeline_panel, fg_color="transparent")
		self.timeline_scroll.pack(fill="both", expand=True, padx=10, pady=5)

		# 2. PHÂN KHU BÊN PHẢI: SHOT PREVIEW (KHI CLICK SHOT)
		self.preview_panel = ctk.CTkFrame(self)
		self.preview_panel.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
		
		self.lbl_preview_title = ctk.CTkLabel(self.preview_panel, text="Shot Preview", font=ctk.CTkFont(size=16, weight="bold"))
		self.lbl_preview_title.pack(padx=15, pady=15, anchor="w")
		
				# Mở file gui/timeline/timeline_editor_window.py, tìm đến danh sách fields cũ và sửa lại:
		self.preview_container = ctk.CTkFrame(self.preview_panel, fg_color="transparent")
		self.preview_container.pack(fill="both", expand=True, padx=15, pady=5)
		
		self.inputs = {}
		# Bổ sung Voice và Subtitle chính xác theo sơ đồ cây của ChatGPT
		fields = ["Video Path", "Prompt", "Duration (s)", "Camera Preset", "Voice Path", "Subtitle Text"]
		for field in fields:
			lbl = ctk.CTkLabel(self.preview_container, text=field, font=ctk.CTkFont(size=12, weight="bold"), anchor="w")
			lbl.pack(fill="x", pady=(6, 1))
			
			if field in ["Prompt", "Subtitle Text"]:
				entry = ctk.CTkTextbox(self.preview_container, height=60, corner_radius=6)
			else:
				entry = ctk.CTkEntry(self.preview_container, placeholder_text=f"Thông số {field.lower()}...")
			entry.pack(fill="x", pady=2)
			self.inputs[field] = entry


		# Vẽ biểu đồ dòng thời gian mẫu của Tập 1 khớp 100% hình ảnh cấu trúc cây của ChatGPT
		self.render_premiere_timeline()

	def render_premiere_timeline(self):
		"""Dựng thanh Timeline phân cấp Episode -> Scene -> Shot trực quan"""
		# Nhãn Tập phim
		ep_lbl = ctk.CTkLabel(self.timeline_scroll, text="🎬 episode #1", font=ctk.CTkFont(size=14, weight="bold"), text_color="#1F6AA5")
		ep_lbl.pack(anchor="w", padx=10, pady=10)

		# --- PHÂN CẢNH 1 ---
		scene1_frame = ctk.CTkFrame(self.timeline_scroll, fg_color="transparent")
		scene1_frame.pack(fill="x", padx=20, pady=5)
		
		s1_lbl = ctk.CTkLabel(scene1_frame, text="📖 scene 1", font=ctk.CTkFont(size=13, weight="bold"))
		s1_lbl.pack(anchor="w", padx=5)

		# Khối Shot 1 của Scene 1
		self.create_shot_timeline_block(scene1_frame, shot_name="shot1", duration_val=4, color="#E65100", 
												# Thêm tham số voice và subtitle vào cấu hình Dictionary của shot1
		meta_s1 = {
			"path": "projects/cache/shot_10101.mp4", 
			"prompt": "3D Donghua, wide shot, To Moc walking into academy", 
			"duration": "4.0", 
			"camera": "Wide Shot",
			"voice": "projects/ToanDanTaoPhong/assets/audio/tomoc_action_01.mp3",
			"subtitle": "Tô Mộc bước vào học viện Long Dạng."
		})

		self.create_shot_timeline_block(scene1_frame, shot_name="shot1", duration_val=4, color="#E65100")

		# --- PHÂN CẢNH 2 ---
		scene2_frame = ctk.CTkFrame(self.timeline_scroll, fg_color="transparent")
		scene2_frame.pack(fill="x", padx=20, pady=15)
		
		s2_lbl = ctk.CTkLabel(scene2_frame, text="📖 scene 2", font=ctk.CTkFont(size=13, weight="bold"))
		s2_lbl.pack(anchor="w", padx=5)

		# Khối Shot 1 của Scene 2
		self.create_shot_timeline_block(scene2_frame, shot_name="shot1", duration_val=5, color="#2E7D32",
												# Thêm tham số voice và subtitle vào cấu hình Dictionary của shot1
		meta_s1 = {
			"path": "projects/cache/shot_10101.mp4", 
			"prompt": "3D Donghua, wide shot, To Moc walking into academy", 
			"duration": "4.0", 
			"camera": "Wide Shot",
			"voice": "projects/ToanDanTaoPhong/assets/audio/tomoc_action_01.mp3",
			"subtitle": "Tô Mộc bước vào học viện Long Dạng."
		})

	def create_shot_timeline_block(self, parent_frame, shot_name, duration_val, color, meta):
		"""Tạo một khối Shot nằm ngang thể hiện thời lượng tuyến tính thời gian thực"""
		row = ctk.CTkFrame(parent_frame, fg_color="transparent")
		row.pack(fill="x", pady=4, padx=15)
		
		# Nhãn tên Shot lề trái
		lbl = ctk.CTkLabel(row, text=f"{shot_name}:", width=60, anchor="w", font=ctk.CTkFont(size=12))
		lbl.pack(side="left", padx=5)
		
		# Khối nút bấm nằm ngang đại diện cho thanh clip (Độ rộng tỷ lệ thuận với thời lượng duration)
		block_width = duration_val * 45
		btn_block = ctk.CTkButton(
			row, text=f"[ {duration_val}s ]", width=block_width, height=28, fg_color=color,
			font=ctk.CTkFont(size=11, weight="bold"),
			command=lambda m=meta, n=shot_name: self.on_timeline_shot_clicked(n, m)
		)
		btn_block.pack(side="left", padx=5)

	def on_timeline_shot_clicked(self, shot_name, meta):
		"""[LUỒNG INTERACTIVE: UNREAL SEQUENCER STYLE] Đổ đầy đủ 6 lớp thông tin đa phương tiện"""
		self.lbl_preview_title.configure(text=f"Preview > {shot_name.upper()}")
		
		# Làm sạch các ô dữ liệu cũ
		for field, widget in self.inputs.items():
			if isinstance(widget, ctk.CTkTextbox): widget.delete("1.0", "end")
			else: widget.delete(0, "end")
		
		# Điền các thông số cơ bản cũ
		self.inputs["Video Path"].insert(0, meta["path"])
		self.inputs["Prompt"].insert("1.0", meta["prompt"])
		self.inputs["Duration (s)"].insert(0, meta["duration"])
		self.inputs["Camera Preset"].insert(0, meta["camera"])
		
		# NẠP HAI THÀNH PHẦN ĐA PHƯƠNG TIỆN MỚI CỦA CHATGPT
		self.inputs["Voice Path"].insert(0, meta.get("voice", "projects/assets/audio/tomoc_voice_01.mp3"))
		self.inputs["Subtitle Text"].insert("1.0", meta.get("subtitle", "Tô Mộc bất ngờ quay đầu."))

