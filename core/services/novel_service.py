import os
from docx import Document
from core.project_manager import ProjectManager

class NovelService:
	def __init__(self, db_session=None):
		self.db = db_session
		self.project_manager = ProjectManager()

	def extract_text_from_docx(self, file_path: str) -> str:
		"""
		[BƯỚC 4 - ĐỌC DOCX] 
		Sử dụng thư viện python-docx để trích xuất toàn bộ văn bản từ file Word
		"""
		if not os.path.exists(file_path):
			raise FileNotFoundError(f"Không tìm thấy tệp tin: {file_path}")
			
		doc = Document(file_path)
		full_text = []
		
		# Duyệt qua từng đoạn văn bản trong file theo cấu trúc gợi ý của ChatGPT
		for p in doc.paragraphs:
			full_text.append(p.text)
			
		# Nối các đoạn văn lại bằng dấu xuống dòng
		return "\n".join(full_text)

	def process_novel_import(self, current_project: str, source_file_path: str) -> dict:
		"""
		[BƯỚC 5 - LƯU VÀO PROJECT]
		Sao chép file vào thư mục dự án và bóc tách nội dung thô
		"""
		# Đọc toàn bộ nội dung chữ trước
		raw_content = self.extract_text_from_docx(source_file_path)
		
		# Xác định thư mục đích để cô lập tài nguyên theo Project (projects/{project_name}/assets/novel/)
		folder_name = current_project.replace(" ", "_")
		target_dir = os.path.join("projects", folder_name, "assets", "novel")
		
		if not os.path.exists(target_dir):
			os.makedirs(target_dir)
			
		filename = os.path.basename(source_file_path)
		destination_path = os.path.join(target_dir, filename)
		
		# Lưu bản sao file Word vào thư mục dự án
		import shutil
		shutil.copy2(source_file_path, destination_path)
		
		# Giả lập thuật toán tự tách chương dựa theo từ khóa "Chương" hoặc dấu ngắt dòng lớn
		# Để đồng bộ tạm thời với giao diện Bước 2 của bạn
		paragraphs = [p.strip() for p in raw_content.split("\n\n") if p.strip()]
		chapters_data = []
		
		if len(paragraphs) <= 3:
			# Nếu file ngắn, đưa toàn bộ vào 1 chương giả lập
			chapters_data = [
				{"title": "#1 Khởi đầu", "text": raw_content}
			]
		else:
			# Chia nhỏ văn bản để nạp lên danh sách chương
			chapters_data = [
				{"title": "#1 Khởi đầu", "text": "\n\n".join(paragraphs[:max(1, len(paragraphs)//3)])},
				{"title": "#2 Thiên tài", "text": "\n\n".join(paragraphs[len(paragraphs)//3 : 2*len(paragraphs)//3])},
				{"title": "#3 Tiến vào mộng võng", "text": "\n\n".join(paragraphs[2*len(paragraphs)//3:])}
			]
			
		return {
			"novel_title": filename.replace(".docx", "").replace("_", " "),
			"saved_file_path": destination_path,
			"chapters": chapters_data
		}
