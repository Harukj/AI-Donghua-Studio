import customtkinter as ctk

class StoryboardForm(ctk.CTkFrame):
	def __init__(self, parent, approve_callback):
		super().__init__(parent, fg_color="transparent")
		self.approve_callback = approve_callback
		
		# Khung cuộn chứa nội dung thuộc tính của phân cảnh để tránh tràn màn hình
		self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
		self.scroll_container.pack(fill="both", expand=True, padx=5, pady=5)

		# 1. PHÂN KHU CHARACTERS (Nhân vật)
		self.char_title = ctk.CTkLabel(self.scroll_container, text="Characters", font=ctk.CTkFont(size=13, weight="bold"), anchor="w")
		self.char_title.pack(fill="x", pady=(5, 2))
		self.char_check = ctk.CTkCheckBox(self.scroll_container, text="Tô Mộc", state="disabled")
		self.char_check.pack(anchor="w", padx=15, pady=2)

		# 2. PHÂN KHU ENVIRONMENT (Bối cảnh)
		self.env_title = ctk.CTkLabel(self.scroll_container, text="Environment", font=ctk.CTkFont(size=13, weight="bold"), anchor="w")
		self.env_title.pack(fill="x", pady=(10, 2))
		self.entry_env = ctk.CTkEntry(self.scroll_container, state="readonly")
		self.entry_env.pack(fill="x", padx=10, pady=2)

		# 3. PHÂN KHU CAMERA (Góc máy)
		self.cam_title = ctk.CTkLabel(self.scroll_container, text="Camera", font=ctk.CTkFont(size=13, weight="bold"), anchor="w")
		self.cam_title.pack(fill="x", pady=(10, 2))
		self.entry_cam = ctk.CTkEntry(self.scroll_container, state="readonly")
		self.entry_cam.pack(fill="x", padx=10, pady=2)

		# 4. PHÂN KHU MOOD (Bầu không khí)
		self.mood_title = ctk.CTkLabel(self.scroll_container, text="Mood", font=ctk.CTkFont(size=13, weight="bold"), anchor="w")
		self.mood_title.pack(fill="x", pady=(10, 2))
		self.entry_mood = ctk.CTkEntry(self.scroll_container, state="readonly")
		self.entry_mood.pack(fill="x", padx=10, pady=2)

		# 5. PHÂN KHU DURATION (Thời lượng)
		self.dur_title = ctk.CTkLabel(self.scroll_container, text="Duration", font=ctk.CTkFont(size=13, weight="bold"), anchor="w")
		self.dur_title.pack(fill="x", pady=(10, 2))
		self.entry_dur = ctk.CTkEntry(self.scroll_container, state="readonly")
		self.entry_dur.pack(fill="x", padx=10, pady=2)

		# 6. PHÂN KHU PROMPT (Câu lệnh AI)
		self.prompt_title = ctk.CTkLabel(self.scroll_container, text="Prompt", font=ctk.CTkFont(size=13, weight="bold"), anchor="w")
		self.prompt_title.pack(fill="x", pady=(10, 2))
		self.txt_prompt = ctk.CTkTextbox(self.scroll_container, height=60, corner_radius=6)
		self.txt_prompt.pack(fill="x", padx=10, pady=2)

		# 7. PHÂN KHU VIDEO STATUS (Trạng thái kết xuất)
		self.video_title = ctk.CTkLabel(self.scroll_container, text="Video", font=ctk.CTkFont(size=13, weight="bold"), anchor="w")
		self.video_title.pack(fill="x", pady=(10, 2))
		self.lbl_video_status = ctk.CTkLabel(self.scroll_container, text="Not Generated", text_color="#E65100", font=ctk.CTkFont(size=13, weight="bold"), anchor="w")
		self.lbl_video_status.pack(fill="x", padx=15, pady=2)

		# Nút bấm Duyệt/Chấp thuận phân cảnh phim để đưa vào hàng đợi
		self.btn_approve = ctk.CTkButton(
			self, text="[ Approve & Sync to LTX Queue ]", fg_color="#2E7D32", hover_color="#1B5E20",
			font=ctk.CTkFont(size=13, weight="bold"), command=self.approve_callback
		)
		self.btn_approve.pack(fill="x", padx=10, pady=10, side="bottom")

	def update_form_display(self, scene_data: dict):
		"""Đổ dữ liệu thuộc tính sạch của phân cảnh lên form hiển thị"""
		# Cập nhật Checkbox nhân vật
		if "Tô Mộc" in scene_data.get("character", ""):
			self.char_check.select()
		else:
			self.char_check.deselect()
			
		# Mở khóa tạm thời để điền text vào ô Entry Readonly
		for field, value in [("entry_env", scene_data.get("environment")), 
							 ("entry_cam", scene_data.get("camera")), 
							 ("entry_mood", scene_data.get("mood")), 
							 ("entry_dur", f"{scene_data.get('duration')}s")]:
			widget = getattr(self, field)
			widget.configure(state="normal")
			widget.delete(0, "end")
			widget.insert(0, value or "")
			widget.configure(state="readonly")
			
		# Điền chuỗi prompt nghệ thuật
		self.txt_prompt.delete("1.0", "end")
		self.txt_prompt.insert("1.0", scene_data.get("prompt") or "Chưa cấu hình prompt.")
		
		# Cập nhật nhãn trạng thái video
		status = scene_data.get("status", "draft")
		if status == "draft":
			self.lbl_video_status.configure(text="Not Generated", text_color="#E65100")
		elif status == "Approved":
			self.lbl_video_status.configure(text="Waiting in Queue", text_color="#1F6AA5")
		elif status == "Completed":
			self.lbl_video_status.configure(text="Render Success (.mp4)", text_color="#2E7D32")
