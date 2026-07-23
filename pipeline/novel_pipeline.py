import os
from sqlalchemy.orm import Session

# Import toàn bộ 6 module phân tích cốt lõi từ gói analyzer
from analyzer.chapter_analyzer import ChapterAnalyzer
from analyzer.scene_analyzer import SceneAnalyzer
from analyzer.character_detector import CharacterDetector
from analyzer.environment_detector import EnvironmentDetector
from analyzer.prop_detector import PropDetector
from analyzer.dialogue_detector import DialogueDetector

# Import các model dữ liệu để sẵn sàng ghi nhận xuống Bước 9 (Database)
from database.models.novel import NovelModel
from database.models.storyboard import StoryboardSceneModel

class NovelPipeline:
	def __init__(self, db_session: Session):
		"""Khởi tạo luồng Pipeline kết nối với phiên làm việc dữ liệu SQLite"""
		self.db = db_session

	def run_pipeline(self, project_id: str, file_path: str) -> dict:
		"""
		[NOVEL PIPELINE GENERAL WORKFLOW]
		Hàm điều phối chạy tuần tự 9 bước từ file Word thô cho đến khi ghi nhận dữ liệu
		"""
		print(f"\n[START] Kích hoạt luồng Novel Pipeline cho tệp tin: {os.path.basename(file_path)}")
		
		# --- BƯỚC 1 & 2: DOCX & PARSER ---
		# Sử dụng thư viện python-docx để đọc chữ thô
		from docx import Document
		if not os.path.exists(file_path):
			raise FileNotFoundError(f"Không tìm thấy tệp tin: {file_path}")
		doc = Document(file_path)
		raw_text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
		print("-> Bước 1 & 2: Trích xuất văn bản văn học (DOCX Parser) thành công.")

		# --- BƯỚC 3: CHAPTER ---
		# Gọi ChapterAnalyzer để ước lượng thông số tổng quan tác phẩm
		chapter_analyzer = ChapterAnalyzer(raw_text)
		chapter_info = chapter_analyzer.analyze()
		print(f"-> Bước 3: Đã phân tích tổng quan chương. Đếm được {chapter_info['word_count']} từ chữ thô.")

		# --- BƯỚC 4: SCENE SPLITTER ---
		# Bẻ nhỏ chương văn học thành từng phân cảnh hành động độc lập
		scene_analyzer = SceneAnalyzer(raw_text)
		raw_scenes = scene_analyzer.split_scenes()
		print(f"-> Bước 4: Bộ bẻ cảnh (Scene Splitter) đã chia nhỏ thành {len(raw_scenes)} phân cảnh điện ảnh.")

		processed_scenes = []
		
		# Duyệt qua từng phân cảnh để tiến hành trích xuất thực thể AI chuyên sâu
		for index, scene_content in enumerate(raw_scenes, start=1):
			scene_num = f"Scene {index:02d}"
			
			# --- BƯỚC 5: CHARACTER DETECTOR ---
			char_detector = CharacterDetector(scene_content)
			char_json = char_detector.detect_characters()
			characters = char_json["characters"]
			
			# --- BƯỚC 6: ENVIRONMENT DETECTOR ---
			env_detector = EnvironmentDetector(scene_content)
			env_json = env_detector.detect_environment()
			environment = env_json["environment"]
			
			# --- BƯỚC 7: PROPS DETECTOR ---
			prop_detector = PropDetector(scene_content)
			props = prop_detector.detect_props()
			
			# --- BƯỚC 8: DIALOGUE DETECTOR ---
			dialogue_detector = DialogueDetector(scene_content)
			dialogues = dialogue_detector.extract_dialogues()
			
			# --- BƯỚC 9: DATABASE (LƯU TRỮ TRỰC TIẾP TỪNG PHÂN CẢNH) ---
			# Đóng gói và lưu trữ cấu trúc kịch bản phân cảnh thô vào SQLite
			db_scene = StoryboardSceneModel(
				scene_number=scene_num,
				raw_text=scene_content,
				character_name=", ".join(characters),
				environment_name=environment,
				time_frame="Day", # Mặc định thiết lập
				mood_atmosphere="Epic", # Mặc định sắc thái nghệ thuật
				action_description=f"Hành động bóc tách: {scene_content[:100]}...",
				project_id=project_id
			)
			self.db.add(db_scene)
			
			# Gom dữ liệu để trả về nạp trực tiếp lên bảng biểu hiển thị giao diện người dùng
			processed_scenes.append({
				"scene_number": scene_num,
				"text": scene_content,
				"characters": characters,
				"environment": environment,
				"props": props,
				"dialogues": dialogues
			})

		# Lưu metadata tổng quan của bộ truyện chữ vào bảng novels [Bước 9]
		filename = os.path.basename(file_path)
		db_novel = NovelModel(
			project_id=project_id,
			title=filename.replace(".docx", "").replace("_", " "),
			filename=filename,
			chapter_count=1 # Mặc định đếm 1 chương thô
		)
		self.db.add(db_novel)
		
		# Thực thi lưu trữ tất cả các bản ghi xuống file SQLite an toàn
		self.db.commit()
		print("[SUCCESS] Luồng Novel Pipeline đã khép lại thành công 100% các bước.\n")
		
		return {
			"novel_title": db_novel.title,
			"scenes": processed_scenes
		}
