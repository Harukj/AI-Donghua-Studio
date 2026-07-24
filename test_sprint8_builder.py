from ai.prompt_builder.builder_v2 import PromptBuilder
from analyzer.scene_object import Scene # Import đối tượng cảnh quay mẫu
	
	# Khởi tạo một đối tượng Scene mẫu đại diện cho phân cảnh cha chứa bộ 7 lớp thông tin
	mock_scene = Scene(id="SCENE_01", chapter=1, title="Mở đầu", summary=mock_scene_content, characters=["Tô Mộc", "Lâm Uyển"], environments=["Học viện Long Dạng"], props=[], dialogues=[], duration=15.0)
	mock_scene.lighting = "Morning Sunlight"
	mock_scene.mood = "Epic Dynamic"

	prompt_engine_v2 = PromptBuilder()
	
	print("\nKết quả sinh Prompt tự động nạp từ ma trận 7 lớp thông tin:")
	for shot in shots_list:
		# Truyền đồng thời cả đối tượng Scene mẫu và Shot con vào đúng bộ khung hàm của ChatGPT
		final_prompt_string = prompt_engine_v2.build(mock_scene, shot)
		
		print(f"\n 🎬 [Shot ID: {shot.id}] | Loại: {shot.context_type.upper()} | Thời lượng: {shot.duration}s")
		print(f"   Câu lệnh Prompt xuất ra:\n   \"{final_prompt_string}\"")