import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.session import SessionLocal
from database.base import Base
from database.engine import engine
from ai.prompt_builder.builder_v3 import PromptBuilder30
from plugins.ltx.ltx_adapter import LTXStudioAdapter

class TestLTXAdapterv08(unittest.TestCase):
	def setUp(self):
		Base.metadata.create_all(bind=engine)
		self.db = SessionLocal()
		self.builder = PromptBuilder30(self.db)
		self.adapter = LTXStudioAdapter()

	def test_9_layers_to_ltx_payload_mapping(self):
		"""Ca kiểm thử tối vĩ đại: Xác thực luồng chuyển đổi từ ma trận 9 tầng sang cấu trúc Payload API sạch lỗi"""
		# 1. Tạo lập ma trận dữ liệu qua Prompt Builder 3.0
		matrix_output = self.builder.build_matrix_prompt_v3(
			char_name="Tô Mộc",
			location_name="Học viện Long Dạng",
			raw_action_text="Bất ngờ quay đầu.",
			context_type="reaction"
		)

		# 2. Kích hoạt lớp trung gian LTX Adapter
		self.adapter.activate_plugin()
		self.adapter.initialize_api_connection()
		api_result = self.adapter.execute_ai_task(matrix_output)

		print("\n============ KẾT QUẢ NGHIỆM THU LTX ADAPTER PAYLOAD V0.8 ============")
		import json
		print(json.dumps(api_result["ltx_payload_sent"], indent=4))
		print("=====================================================================")

		# Khẳng định kiểm thử tự động (Assertions) bảo chứng chất lượng đầu ra API
		self.assertEqual(api_result["status"], "queued_success")
		self.assertIn("prompt_config", api_result["ltx_payload_sent"])
		self.assertIn("audio_track_sync", api_result["ltx_payload_sent"])
		
		self.adapter.deactivate_plugin()

	def tearDown(self):
		self.db.close()

if __name__ == "__main__":
	unittest.main()
