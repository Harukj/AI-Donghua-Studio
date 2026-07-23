import customtkinter as ctk

class EnvironmentForm(ctk.CTkFrame):
	def __init__(self, parent, save_callback):
		super().__init__(parent)
		self.save_callback = save_callback
		
		self.form_title = ctk.CTkLabel(self, text="Hồ sơ chi tiết bối cảnh", font=ctk.CTkFont(size=18, weight="bold"))
		self.form_title.pack(padx=20, pady=15, anchor="w")
		
		self.form_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
		self.form_scroll.pack(padx=15, pady=5, fill="both", expand=True)
		
		self.fields = ["Tên bối cảnh", "Thời gian", "Thời tiết", "Kiến trúc", "Mô tả bối cảnh", "Style", "Negative Prompt"]
		self.inputs = {}
		
		for field in self.fields:
			row_frame = ctk.CTkFrame(self.form_scroll, fg_color="transparent")
			row_frame.pack(fill="x", pady=4)
			
			lbl = ctk.CTkLabel(row_frame, text=field, width=120, anchor="w", font=ctk.CTkFont(size=13))
			lbl.pack(side="left", padx=5)
			
			if field in ["Mô tả bối cảnh", "Negative Prompt"]:
				entry = ctk.CTkTextbox(row_frame, height=75, corner_radius=6)
			else:
				entry = ctk.CTkEntry(row_frame, placeholder_text=f"Nhập {field.lower()}...")
				
			entry.pack(side="left", fill="x", expand=True, padx=5)
			self.inputs[field] = entry
			
		self.btn_save = ctk.CTkButton(
			self, text="[ Save Environment ]", fg_color="#2E7D32", hover_color="#1B5E20",
			font=ctk.CTkFont(size=14, weight="bold"), command=self.on_save_clicked
		)
		self.btn_save.pack(padx=20, pady=15, fill="x")

	def clear_form(self):
		for field, widget in self.inputs.items():
			if isinstance(widget, ctk.CTkTextbox): widget.delete("1.0", "end")
			else: widget.delete(0, "end")

	def on_save_clicked(self):
		form_data = {}
		for field, widget in self.inputs.items():
			if isinstance(widget, ctk.CTkTextbox): form_data[field] = widget.get("1.0", "end-1c").strip()
			else: form_data[field] = widget.get().strip()
		self.save_callback(form_data)
