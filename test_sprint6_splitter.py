from analyzer.scene_splitter import AdvancedSceneSplitter

def run_sprint6_test():
	print("============ KIỂM TRA NGHIỆM THU SPRINT 6 - SCENE SPLITTER ============")
	
	# 1. Khởi tạo đoạn văn bản kịch bản mẫu thô lấy chính xác 100% từ hình ảnh của ChatGPT
	mock_chapter_content = (
		"Tô Mộc mở mắt.\n"
		"Giáo viên bước vào.\n"
		"Mọi người kinh ngạc."
	)
	print(f"Văn bản truyện chữ đầu vào:\n{mock_chapter_content}\n")
	print("-----------------------------------------------------------------------")

	# 2. Gọi bộ tách bẻ cảnh nâng cao của Sprint 6
	splitter = AdvancedSceneSplitter(mock_chapter_content)
	scenes_output = splitter.execute_split()

	# 3. In kết quả xuất ra dạng cấu trúc đối tượng phân cảnh trực quan
	print("Kết quả phần mềm tự động chia thành:")
	for index, scene_text in enumerate(scenes_output, start=1):
		scene_num_str = f"Scene {index:03d}"
		print(f"\n {scene_num_str}")
		print(f"   {scene_text}")

	print("=======================================================================\n")

if __name__ == "__main__":
	run_sprint6_test()
