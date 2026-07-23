import os
import shutil
from datetime import datetime
from sqlalchemy.orm import Session
from docx import Document
from database.models.novel import NovelModel

class NovelService:
	def __init__(self, db_session: Session):
		"""Khởi tạo service kết nối với phiên làm việc dữ liệu SQLite"""
		self.db = db_session

	def extract_text_from_docx(self, file_path: str) -> str:
		"""[Bước 4] Trích xuất toàn bộ văn bản từ file Word"""
		if not os.path.exists(file_path):
			raise FileNotFoundError(f"Không tìm thấy tệp tin: {file_path}")
		doc = Document(file_path)
		return "\n".join([p.text for p in doc.paragraphs])

	def process_novel_import(self, project_id: str, source_file_path: str) -> dict:
		"""
		[Bước 5 & Bước 6] 
		Sao chép file vật lý vào thư mục gốc của Project và lưu bản ghi vào Database.
		"""
		# 1. Trích xuất nội dung văn bản thô từ file Word
		raw_content = self.extract_text_from_docx(source_file_path)
		
		# 2. Xử lý lưu file vật lý biệt lập theo đúng sơ đồ [Bước 5]: projects/{project_name}/novel/
		folder_name = project_id.replace(" ", "_")
		target_dir = os.path.join("projects", folder_name, "novel")
		
		if not os.path.exists(target_dir):
			os.makedirs(target_dir)
			
		filename = os.path.basename(source_file_path)
		destination_path = os.path.join(target_dir, filename)
		
		# Luôn luôn copy file mới vào dự án để bảo vệ file gốc của người dùng
		shutil.copy2(source_file_path, destination_path)
		
		# 3. Thuật toán giả lập phân đoạn và đếm số chương truyện chữ
		paragraphs = [p.strip() for p in raw_content.split("\n\n") if p.strip()]
		chapters_data = []
		
		if len(paragraphs) <= 3:
			chapters_data = [{"title": "#1 khởi đầu", "text": raw_content}]
		else:
			chapters_data = [
				{"title": "#1 khởi đầu", "text": "\n\n".join(paragraphs[:len(paragraphs)//3])},
				{"title": "#2 thiên tài", "text": "\n\n".join(paragraphs[len(paragraphs)//3 : 2*len(paragraphs)//3])},
				{"title": "#3 tiến vào mộng võng", "text": "\n\n".join(paragraphs[2*len(paragraphs)//3:])}
			]
		
		# 4. Ghi nhận dữ liệu metadata vào bảng database SQLite chuẩn [Bước 6]
		db_novel = NovelModel(
			project_id=project_id,
			title=filename.replace(".docx", "").replace("_", " "),
			filename=filename,
			chapter_count=len(chapters_data)
		)
		self.db.add(db_novel)
		self.db.commit()
		self.db.refresh(db_novel)
		
		print(f"Hệ thống: Đã ghi nhận tác phẩm '{db_novel.title}' vào Database với ID: {db_novel.id}")
		
		return {
			"novel_title": db_novel.title,
			"chapters": chapters_data
		}
