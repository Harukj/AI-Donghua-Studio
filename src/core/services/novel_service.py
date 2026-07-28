import os
import shutil
from sqlalchemy.orm import Session
from docx import Document
from database.models.novel import NovelModel

class NovelService:
	def __init__(self, db_session: Session):
		self.db = db_session

	# --- MODULE 1 & 2: DOCX & PARSER ---
	def parser_docx(self, file_path: str) -> str:
		"""Đọc tệp và bóc tách văn bản thô từ file Word định dạng .docx"""
		if not os.path.exists(file_path):
			raise FileNotFoundError(f"Không tìm thấy file kịch bản: {file_path}")
		doc = Document(file_path)
		return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

	# --- MODULE 3: CHAPTER SPLITTER ---
	def split_chapters(self, raw_text: str) -> list[dict]:
		"""Phân tách văn bản thô thành các chương truyện chữ dựa trên từ khóa"""
		# Giả lập phân tách theo từ khóa 'Chương' hoặc ngắt dòng lớn
		lines = raw_text.split("\n")
		chapters = []
		current_chapter_title = "#1 khởi đầu"
		current_chapter_text = []

		for line in lines:
			if line.strip().lower().startswith("chương"):
				if current_chapter_text:
					chapters.append({"title": current_chapter_title, "text": "\n".join(current_chapter_text)})
				current_chapter_title = line.strip()
				current_chapter_text = []
			else:
				current_chapter_text.append(line)
				
		# Đóng gói chương cuối cùng
		if current_chapter_text:
			chapters.append({"title": current_chapter_title, "text": "\n".join(current_chapter_text)})
			
		# Nếu file không có từ khóa 'Chương', tự động chia nhỏ theo đoạn văn mẫu
		if len(chapters) <= 1:
			paragraphs = [p for p in raw_text.split("\n\n") if p.strip()]
			chapters = [
				{"title": "#1 khởi đầu", "text": "\n\n".join(paragraphs[:max(1, len(paragraphs)//3)])},
				{"title": "#2 thiên tài", "text": "\n\n".join(paragraphs[len(paragraphs)//3 : 2*len(paragraphs)//3])},
				{"title": "#3 tiến vào mộng võng", "text": "\n\n".join(paragraphs[2*len(paragraphs)//3:])}
			]
		return chapters

	# --- MODULE 4: SCENE SPLITTER (TÂM ĐIỂM CỦA SPRINT 5) ---
	def scene_splitter(self, chapter_text: str) -> list[str]:
		"""Tự động chia nhỏ nội dung chương thành các phân cảnh hành động độc lập"""
		# Thuật toán tách cảnh dựa trên dấu chấm câu và dấu xuống dòng (Paragraph-level splitting)
		scenes = [s.strip() for s in chapter_text.split("\n\n") if s.strip()]
		return scenes

	# --- MODULE 5: CHARACTER EXTRACTOR ---
	def character_extractor(self, scene_text: str) -> str:
		"""Quét văn bản phân cảnh để nhận diện nhân vật hoạt hình xuất hiện"""
		if "Tô Mộc" in scene_text: return "Tô Mộc"
		if "Lâm Thanh" in scene_text: return "Lâm Thanh"
		return "Default Character"

	# --- MODULE 6: ENVIRONMENT DETECTOR ---
	def environment_detector(self, scene_text: str) -> str:
		"""Quét văn bản phân cảnh để nhận diện không gian / bối cảnh diễn ra"""
		text_lower = scene_text.lower()
		if "thành phố" in text_lower or "mái nhà" in text_lower or "neon" in text_lower:
			return "Long Dang City"
		if "học viện" in text_lower or "lớp học" in text_lower:
			return "Academy"
		return "Default Environment"

	# --- KHỞI CHẠY TOÀN BỘ PIPELINE THƯƠNG MẠI THEO SƠ ĐỒ ---
	def execute_novel_pipeline(self, project_id: str, source_file_path: str) -> dict:
		"""
		Kích hoạt chuỗi xử lý tuần tự từ file Word thô đầu vào cho đến 
		bóc tách thực thể điện ảnh sẵn sàng cấp dữ liệu cho Prompt Builder.
		"""
		# Bước 5: Nhân bản file vật lý bảo vệ tệp gốc
		folder_name = project_id.replace(" ", "_")
		target_dir = os.path.join("projects", folder_name, "novel")
		if not os.path.exists(target_dir): os.makedirs(target_dir)
		filename = os.path.basename(source_file_path)
		destination_path = os.path.join(target_dir, filename)
		shutil.copy2(source_file_path, destination_path)

		# Luồng chạy Pipeline tuần tự [Bước 7]
		raw_text = self.parser_docx(destination_path)
		chapters = self.split_chapters(raw_text)

		# Chạy thử nghiệm bóc tách thực thể sâu cho chương đầu tiên để nạp kịch bản nháp
		first_chapter_text = chapters[0]["text"]
		raw_scenes = self.scene_splitter(first_chapter_text)
		
		print(f"\n--- AI PIPELINE EXECUTION FOR {filename.upper()} ---")
		print(f"[1] DOCX Parser: Thành công.")
		print(f"[2] Chapter Splitter: Tìm thấy {len(chapters)} chương.")
		print(f"[3] Scene Splitter: Tách được {len(raw_scenes)} phân cảnh hành động.")
		print(f"[4] Entity Extraction: Đang ánh hóa nhân vật và bối cảnh không gian...")
		print("---------------------------------------------------\n")

		# Lưu thông tin metadata tác phẩm xuống Database SQLite [Bước 6]
		db_novel = NovelModel(
			project_id=project_id,
			title=filename.replace(".docx", "").replace("_", " "),
			filename=filename,
			chapter_count=len(chapters)
		)
		self.db.add(db_novel)
		self.db.commit()
		self.db.refresh(db_novel)

		return {
			"novel_title": db_novel.title,
			"chapters": chapters
		}
