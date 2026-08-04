import unittest
from src.database.session import SessionLocal
from src.ai.prompt_builder.builder_v3 import PromptBuilder30
# Sửa lại dòng import trỏ thẳng vào Class AssetModel sạch chuẩn v1.0 của ChatGPT
from src.database.models.asset import AssetModel
class TestPromptBuilder30(unittest.TestCase):
	def setUp(self):
		"""Thiết lập phiên kết nối cơ sở dữ liệu SQLite trước khi test"""
		from src.database.session import SessionLocal
		# Nạp bộ công cụ tự động sinh cấu trúc bảng hệ thống DreamForge
		from src.database.base import Base
		from src.database.engine import engine
		
		# Ép lệnh SQLAlchemy tự động quét Model và tạo toàn bộ bảng nếu chưa có
		Base.metadata.create_all(bind=engine)
		
		self.db = SessionLocal()
		self.builder = PromptBuilder30(self.db)

	def test_matrix_20_modules_mixer(self):
		"""Ca kiểm thử tối thượng: Xác thực chuỗi câu lệnh sinh ra chứa đủ các nấc mô-đun đặc tả của ChatGPT"""
		char_name = "Tô Mộc"
		location_name = "Học viện Long Dạng"
		camera_preset = "Toàn cảnh"
		action_text = "Vung thần kiếm lao vào quyết đấu."

		# Kích hoạt động cơ trộn ma trận v3.0
		result = self.builder.build_matrix_prompt_v3(char_name, location_name, camera_preset, "action")
		
		print("\n============ KẾT QUẢ XUẤT BẢN MA TRẬN PROMPT BUILDER 3.0 ============")
		print(f" Positive Prompt:\n \"{result['positive']}\"\n")
		print(f" Negative Prompt:\n \"{result['negative']}\"")
		print("=====================================================================")

		# Khẳng định kiểm thử tự động (Assertions) để chứng minh bộ trộn hoạt động hoàn hảo
		self.assertIn("3d chinese donghua animation style", result["positive"].lower())
		self.assertIn("long dang academy", result["positive"].lower()) # Kiểm tra module bối cảnh nạp từ mẫu
		self.assertIn("wide shot", result["positive"].lower())         # Kiểm tra module góc máy nạp từ mẫu
		self.assertIn("unreal engine 5 render", result["positive"].lower()) # Kiểm tra chất lượng đầu ra

	def tearDown(self):
		self.db.close()

if __name__ == "__main__":
	unittest.main()
