import os
from sqlalchemy.orm import Session

# Import toàn bộ các bộ quét thực thể từ gói analyzer
from analyzer.chapter_analyzer import ChapterAnalyzer
from analyzer.scene_analyzer import SceneAnalyzer
from analyzer.character_detector import CharacterDetector
from analyzer.environment_detector import EnvironmentDetector
from analyzer.prop_detector import PropDetector
from analyzer.dialogue_detector import DialogueDetector

# Import mô hình Class Scene Object v1.0 để ép kiểu dữ liệu hướng đối tượng
from analyzer.scene_object import Scene

# Import các model cơ sở dữ liệu để ghi nhận dữ liệu xuống SQLite
from database.models.novel import NovelModel
from database.models.storyboard import StoryboardSceneModel

class NovelPipeline:
	def __init__(self, db_session: Session):
		"""Khởi tạo luồng Pipeline kết nối với phiên làm việc dữ liệu SQLite"""
		self.db = db_session

	def run_pipeline(self, project_id: str, file_path: str) -> dict:
		"""
		[NOVEL PIPELINE v1.0 CORE]
		Điều phối luồng chạy tuần tự qua các bộ lọc analyzer để sinh ra các Scene Object sạch.
		"""
		print(f"\n[START] Kích hoạt luồng Novel Pipeline cho tệp tin: {os.path.basename(file_path)}")
		
		# --- BƯỚC 1 & 2: DOCX & PARSER ---
		from docx import Document
		if not os.path.exists(file_path):
			raise FileNotFoundError(f"Không tìm thấy tệp tin: {file_path}")
		doc = Document(file_path)
		raw_text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

		# --- BƯỚC 3: CHAPTER ---
		chapter_analyzer = ChapterAnalyzer(raw_text)
		chapter_info = chapter_analyzer.analyze()

		# --- BƯỚC 4: SCENE SPLITTER ---
		scene_analyzer = SceneAnalyzer(raw_text)
		raw_scenes = scene_analyzer.split_scenes()

		processed_scenes = []
		
		# Duyệt qua từng đoạn văn bản để tiến hành bóc tách thực thể AI chuyên sâu
		for index, scene_content in enumerate(raw_scenes, start=1):
			scene_num = f"Scene {index:02d}"
			
			# --- BƯỚC 5: CHARACTER DETECTOR (Đầu ra JSON) ---
			char_detector = CharacterDetector(scene_content)
			char_json = char_detector.detect_characters()
			characters = char_json["characters"]
			
			# --- BƯỚC 6: ENVIRONMENT DETECTOR (Đầu ra JSON) ---
			env_detector = EnvironmentDetector(scene_content)
			env_json = env_detector.detect_environment()
			environments = [env_json["environment"]]
			
			# --- BƯỚC 7: PROPS DETECTOR ---
			prop_detector = PropDetector(scene_content)
			props = prop_detector.detect_props()
			
			# --- BƯỚC 8: DIALOGUE DETECTOR (Đầu ra JSON) ---
			dialogue_detector = DialogueDetector(scene_content)
			dialogue_json = dialogue_detector.extract_dialogues()
			dialogues = [dialogue_json] # Đóng gói dictionary thoại vào mảng list theo quy chuẩn Class
			
			# --- ÉP KIỂU SANG ĐỐI TƯỢNG SCENE OBJECT CHUẨN V1.0 ---
			# Thay thế hoàn toàn cho việc dùng Dict lỏng lẻo báo lỗi gạch đỏ của bạn
			scene_object = Scene(
				id=scene_num,
				chapter=1,
				title=f"Phân cảnh {scene_num}",
				summary=scene_content[:150],
				characters=characters,
				environments=environments,
				props=props,
				dialogues=dialogues,
				duration=5.0
			)
			
			# Nạp thực thể Object sạch vào danh sách để gửi trả về cho giao diện GUI hiển thị
			processed_scenes.append(scene_object)
			
			# --- BƯỚC 9: DATABASE (LƯU TRỮ TRỰC TIẾP TỪNG PHÂN CẢNH) ---
			db_scene = StoryboardSceneModel(
				scene_number=scene_object.id,
				raw_text=scene_content,
				character_name=", ".join(scene_object.characters),
				environment_name=", ".join(scene_object.environments),
				time_frame="Day",
				mood_atmosphere="Epic",
				action_description=scene_object.summary,
				project_id=project_id
			)
			self.db.add(db_scene)

		# Lưu thông tin metadata tổng quan của tác phẩm truyện chữ vào bảng novels [Bước 9]
		filename = os.path.basename(file_path)
		db_novel = NovelModel(
			project_id=project_id,
			title=filename.replace(".docx", "").replace("_", " "),
			filename=filename,
			chapter_count=1
		)
		self.db.add(db_novel)
		
		# Thực thi lưu trữ tất cả các bản ghi xuống file SQLite an toàn
		self.db.commit()
		print("[SUCCESS] Toàn bộ luồng Novel Pipeline v1.0 đã khép lại thành công.\n")
		
		return {
			"novel_title": db_novel.title,
			"scenes": processed_scenes
		}
