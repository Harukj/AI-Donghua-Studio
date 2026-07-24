from ai.scene_splitter.shot_builder import ShotBuilder

def run_sprint8_integration_test():
	print("============ KIỂM TRA NGHIỆM THU SPRINT 8 - SHOT BUILDER ============")
	
	# Nội dung văn bản phân cảnh thô lấy chính xác 100% từ ảnh mẫu kịch bản của ChatGPT
	mock_scene_content = (
		"Tô Mộc bước vào học viện.\n"
		"Lâm Uyển nhìn cậu.\n"
		"Hai người nhìn nhau."
	)
	print(f"Văn bản Phân cảnh đầu vào:\n{mock_scene_content}\n")
	print("---------------------------------------------------------------------")

	# Khởi chạy động cơ điều phối bẻ cú máy virtual camera v0.6
	builder = ShotBuilder(scene_id=101, raw_scene_text=mock_scene_content)
	shots_output = builder.build_shots_from_scene()

	print("Kết quả cỗ máy Engine tự động phân rã cấu trúc hướng đối tượng:\n")
	for shot in shots_output:
		print(f" -> Khởi tạo: Shot [ID: {shot.id}] Index: {shot.index} | Ngữ cảnh: {shot.context_type.upper()}")
		print(f"    Góc máy chỉ định: {shot.camera} ({shot.lens}) | Chuyển động: {shot.movement}")
		print(f"    Mã Prompt gộp: '{shot.prompt}'\n")
		
	print("=====================================================================\n")

if __name__ == "__main__":
	run_sprint8_integration_test()
