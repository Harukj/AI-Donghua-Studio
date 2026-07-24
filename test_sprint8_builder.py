from ai.scene_splitter.shot_builder import ShotBuilder
from ai.prompt_builder.builder_v2 import PromptBuilderV2

def run_production_engine_test():
	print("============ NGHIỆM THU PRODUCTION ENGINE v0.6 (PROMPT BUILDER 2.0) ============")
	
	# Kịch bản phân cảnh mẫu thô từ ChatGPT
	mock_scene_content = "Tô Mộc bước vào học viện.\nLâm Uyển nhìn cậu.\nHai người nhìn nhau."
	
	# 1. Kích hoạt bộ bẻ cú máy ShotBuilder
	builder = ShotBuilder(scene_id=101, raw_scene_text=mock_scene_content)
	shots_list = builder.build_shots_from_scene()
	
	# 2. Khởi động bộ trộn thế hệ mới PromptBuilder2.0
	prompt_engine_v2 = PromptBuilderV2()
	
	print("\nKết quả sinh Prompt tự động nạp từ Camera Presets JSON:")
	for shot in shots_list:
		# Gọi lõi Prompt Builder 2.0 trộn chuỗi hướng đối tượng
		final_prompt_string = prompt_engine_v2.build_final_prompt_from_shot(shot)
		
		print(f"\n 🎬 [Shot ID: {shot.id}] | Loại: {shot.context_type.upper()} | Thời lượng: {shot.duration}s")
		print(f"   Câu lệnh Prompt xuất ra:\n   \"{final_prompt_string}\"")
		
	print("================================================================================\n")

if __name__ == "__main__":
	run_production_engine_test()
