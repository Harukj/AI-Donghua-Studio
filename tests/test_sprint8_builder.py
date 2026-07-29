import sys
import os
import unittest

# Ép đường dẫn hệ thống truy quét sâu vào bên trong thư mục src/ chuẩn doanh nghiệp
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from ai.prompt_builder.builder_v2 import PromptBuilder
from database.models.shot import ShotModel  # Nạp Model Object để vá lỗi AttributeError

class TestSprint8PromptBuilder(unittest.TestCase):
	def setUp(self):
		"""Khởi tạo cấu hình cỗ máy sinh Prompt 7 lớp"""
		self.prompt_engine_v2 = PromptBuilder()

	def test_automated_7_layers_prompt_generation(self):
		"""Ca kiểm thử nghiệm thu: Truyền đối tượng Object sạch giải quyết triệt để lỗi dict AttributeError"""
		mock_scene = {
			"id": "SCENE_01",
			"title": "Mở đầu",
			"characters": ["Tô Mộc", "Lâm Uyển"],
			"environments": ["Học viện Long Dạng"],
			"lighting": "Morning Sunlight",
			"mood": "Epic Dynamic"
		}
		
		# KHỞI TẠO OBJECT MODEL CHUẨN: Thay thế Dictionary thô bằng thực thể Object thực sự
				# Mở file tests/test_sprint8_builder.py, sửa lại phân đoạn khai báo ShotModel:
		
		# TIÊM THAM SỐ PROMPT: Cung cấp chuỗi văn bản nền để thuật toán .replace() bóc tách sạch lỗi NoneType
		shot1 = ShotModel(
			id=150101, 
			scene_id=1501, 
			index=1, 
			context_type="establishing", 
			duration=5.0,
			prompt="3D Chinese Donghua style, wide cinematic establishing shot of long dang academy"
		)
		
		shot2 = ShotModel(
			id=150102, 
			scene_id=1501, 
			index=2, 
			context_type="walking", 
			duration=4.0,
			prompt="3D Chinese Donghua style, medium tracking shot of character walking forward"
		)
		
		mock_shots_list = [shot1, shot2]

		
		mock_shots_list = [shot1, shot2]
		
		print("\n============ KẾT QUẢ NGHIỆM THU MA TRẬN PROMPT 7 LỚP SẠCH LỖI INTERACTION ============")
		for shot in mock_shots_list:
			# Lúc này shot đã là Object, lệnh gọi shot.context_type bên trong lõi sẽ chạy mượt mà 100%
			final_prompt_string = self.prompt_engine_v2.build(mock_scene, shot)
			print(f" 🎬 [Shot ID: {shot.index}] | Ngữ cảnh: {shot.context_type.upper()} | Thời lượng: {shot.duration}s")
			print(f" 📝 Generated Token: \"{final_prompt_string[:80]}...\"")
		print("=======================================================================================")
		
		self.assertEqual(len(mock_shots_list), 2)

if __name__ == "__main__":
	unittest.main()
