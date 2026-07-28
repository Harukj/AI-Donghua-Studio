import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from src.database.session import SessionLocal
from src.database.base import Base
from src.database.engine import engine
from src.database.models.shot import ShotModel
from src.database.models.episode import EpisodeModel
from src.services.review_export_service import ReviewAndExportService

class TestReviewAndExportSubsystem(unittest.TestCase):
	def setUp(self):
		"""Khởi tạo cấu trúc hạ tầng cơ sở dữ liệu giả lập sạch"""
		Base.metadata.drop_all(bind=engine)
		Base.metadata.create_all(bind=engine)
		
		self.db = SessionLocal()
		self.service = ReviewAndExportService(self.db)

		# Nạp dữ liệu tập phim mẫu và cú máy ở trạng thái chờ duyệt (rendered)
		self.test_ep = EpisodeModel(project_id="ToanDanTaoPhong", episode_number=15, status="In Progress")
		self.test_shot = ShotModel(id=150103, scene_id=1501, index=3, status="rendered", prompt="review component shot")
		
		self.db.add(self.test_ep)
		self.db.add(self.test_shot)
		self.db.commit()

	def test_studio_review_approval_and_final_export_pipeline(self):
		"""Ca kiểm thử tối vĩ đại: Xác thực vòng đời duyệt phim 9 tầng và tác vụ gộp nối file chặng cuối"""
		# 1. Nghiệm thu phân khu Review Workspace
		approval_success = self.service.approve_cinematic_shot_review(shot_id=150103)
		self.assertTrue(approval_success)
		
		# Kiểm tra xem trạng thái của Shot đã dịch chuyển chuẩn sang approved chưa
		updated_shot = self.db.query(ShotModel).filter(ShotModel.id == 150103).first()
		self.assertEqual(updated_shot.status, "approved")

		# 2. Nghiệm thu phân khu Export Center (Tác vụ Merge Video + Subtitle)
		export_result = self.service.execute_episode_final_export(project_id="ToanDanTaoPhong", episode_num=15)
		
		print("\n============ KẾT QUẢ NGHIỆM THU STUDIO REVIEW & EXPORT CENTER ============")
		print(f" 🎭 Review Workspace: Cú máy 150103 nạp trạng thái duyệt ➔ [{updated_shot.status.upper()}]")
		print(f" 🖼️ Export Center: Tệp tin ảnh bìa Thumbnail ➔ {export_result['thumbnail']}")
		print(f" 📝 Export Center: Mô tả SEO văn bản kịch bản ➔ {export_result['metadata']['description']}")
		print(f" 🎞️ File đích xuất bản YouTube: {export_result['output_video']}")
		print("==========================================================================")

		self.assertEqual(export_result["status"], "Exported Successfully")
		self.assertTrue(export_result["output_video"].endswith("Episode15.mp4"))
		
		# Đảm bảo trạng thái Tập phim đã được đóng băng chuyển sang Completed
		updated_ep = self.db.query(EpisodeModel).filter(EpisodeModel.episode_number == 15).first()
		self.assertEqual(updated_ep.status, "Completed")

	def tearDown(self):
		self.db.close()

if __name__ == "__main__":
	unittest.main()
