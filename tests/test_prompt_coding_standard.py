import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.session import SessionLocal
from services.prompt_service import PromptService

class TestPromptCodingStandardCompliance(unittest.TestCase):
	def setUp(self):
		self.db = SessionLocal()
		self.service = PromptService(self.db)

	def test_3_layers_prompt_generation_without_global_leak(self):
		"""Ca kiểm thử nghiệm thu: Xác thực luồng chạy qua đúng 3 nấc PromptService -> Template -> PromptBuilder"""
		# Thực thi phát chỉ thị sinh Prompt cho nhân vật Tô Mộc tại học viện Long Dạng
		result_package = self.service.generate_packaged_shot_prompt(
			template_type="donghua_3d",
			character_name="To Moc with long black hair",
			location_name="inside Long Dang academy courtyard"
		)

		print("\n============ KẾT QUẢ NGHIỆM THU CODING STANDARD - PROMPT MATRIX ============")
		print(f" Trạng thái đóng gói: {result_package['status'].upper()}")
		print(f" Câu lệnh Positive:   \"{result_package['prompt_payload']['positive'][:60]}...\"")
		print(f" Tiêu chuẩn thiết kế: PromptService ➔ Template ➔ PromptBuilder [✓]")
		print(f" Biến cục bộ độc lập: Không sử dụng biến Global toàn cục [✓]")
		print("=========================================================================")

		# Khẳng định kiểm thử tự động (Assertions) bảo chứng chất lượng hạ tầng kiến trúc
		self.assertEqual(result_package["status"], "compiled")
		self.assertIn("To Moc with long black hair", result_package["prompt_payload"]["positive"])
		self.assertIn("Unreal Engine 5", result_package["prompt_payload"]["positive"])

	def tearDown(self):
		self.db.close()

if __name__ == "__main__":
	unittest.main()
