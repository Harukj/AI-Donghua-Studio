import os
from sqlalchemy.orm import Session
from src.database.models.novel import NovelModel
from src.pipeline.novel_pipeline import NovelPipeline

class ProductionPipeline:
	def __init__(self, db_session: Session):
		"""Khởi tạo dây chuyền sản xuất Production Pipeline kết nối SQLite"""
		self.db = db_session
		self.novel_pipeline = NovelPipeline(db_session)

	def build_episode_package(self, project_id: str, episode_number: int, docx_file_path: str) -> dict:
		"""
		[PRODUCTION PIPELINE CORE WORKFLOW]
		Quản lý toàn bộ quá trình sản xuất của một Tập phim (Episode) theo sơ đồ của ChatGPT:
		Nhận kịch bản -> Bóc tách 30 Scenes -> Quản lý 30 Videos -> Liên kết AI Audio & Subtitle -> Đóng gói Final Render.
		"""
		print(f"\n=======================================================")
		print(f"[PRODUCTION PIPELINE] BẮT ĐẦU KHỞI CHẠY EPISODE {episode_number:02d}")
		print(f"=======================================================")

		# 1. KÍCH HOẠT NOVEL PIPELINE (BƯỚC 1: CHAPTER -> BƯỚC 2: SCENES SPLITTER)
		# Tự động quét 9 bước tuần tự để trích xuất thực thể và sinh ra các Scene Object sạch
		pipeline_result = self.novel_pipeline.run_pipeline(project_id, docx_file_path)
		scenes = pipeline_result["scenes"]
		
		# 2. XÁC ĐỊNH HỆ THỐNG THƯ MỤC CÔ LẬP SẢN XUẤT CHO TẬP PHIM (EPISODE WORKSPACE)
		folder_name = project_id.replace(" ", "_")
		episode_dir = os.path.join("projects", folder_name, f"episode_{episode_number:02d}")
		
		# Tự động sinh hệ thống thư mục con phục vụ đóng gói Final Render theo sơ đồ ChatGPT
		sub_production_dirs = ["videos", "audio", "subtitles", "exports"]
		for sub_dir in sub_production_dirs:
			path = os.path.join(episode_dir, sub_dir)
			if not os.path.exists(path):
				os.makedirs(path)

		# 3. QUẢN LÝ DANH SÁCH 30 VIDEOS & AI AUDIO TƯƠNG ỨNG VỚI CÁC PHÂN CẢNH
		video_assets = []
		audio_assets = []
		subtitle_assets = []
		
		total_duration = 0.0

		for scene in scenes:
			scene_id = scene.id
			
			# Định vị đường dẫn lưu tệp tin Video nháp thô cho từng Scene
			video_path = os.path.join(episode_dir, "videos", f"{scene_id.lower()}_clip.mp4")
			video_assets.append(video_path)
			
			# Định vị đường dẫn lưu tệp tin AI Audio (Lồng tiếng/SFX) cho từng Scene
			audio_path = os.path.join(episode_dir, "audio", f"{scene_id.lower()}_voice.mp3")
			audio_assets.append(audio_path)
			
			# Định vị đường dẫn lưu phụ đề văn bản (Subtitle) tương ứng
			sub_path = os.path.join(episode_dir, "subtitles", f"{scene_id.lower()}_sub.srt")
			subtitle_assets.append(sub_path)
			
			# Tích lũy tổng thời lượng của tập phim dựa trên quyết định điện ảnh của AI Director
			total_duration += getattr(scene, 'duration', 5.0)

		# 4. THIẾT LẬP ĐƯỜNG DẪN XUẤT PHIM TOÀN DIỆN [FINAL RENDER] SẴN SÀNG LÊN YOUTUBE
		final_render_export_path = os.path.join(episode_dir, "exports", f"episode_{episode_number:02d}_final.mp4")

		print(f"\n[SUCCESS] Đóng gói thành công dây chuyền Episode {episode_number:02d}:")
		print(f" -> Tổng số phân cảnh bóc tách: {len(scenes)} Scenes")
		print(f" -> Hệ thống quản lý tài nguyên: {len(video_assets)} Tệp clip Video và {len(audio_assets)} Tệp âm thanh")
		print(f" -> Tổng thời lượng tập phim dự kiến: {total_duration} giây")
		print(f" -> Đường dẫn lưu trữ kết xuất phim Final Render: {final_render_export_path}")
		print(f"=======================================================\n")

		return {
			"episode": episode_number,
			"total_scenes": len(scenes),
			"total_duration_seconds": total_duration,
			"video_queue": video_assets,
			"audio_queue": audio_assets,
			"subtitle_queue": subtitle_assets,
			"final_render_path": final_render_export_path
		}
