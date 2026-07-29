# Mở file tests/test_sprint6_splitter.py và ghi đè dải dòng từ 1 đến 5 bằng khối lệnh sau:
import sys
import os
import unittest

# Ép Python đưa thư mục src/ chuẩn doanh nghiệp vào danh sách tìm kiếm module
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

# Thực hiện nạp chính xác thực thể từ file splitter.py nằm trong src/ai/scene_splitter/
# (Vui lòng kiểm tra kỹ xem tên Class bên trong file splitter.py của bạn là SceneSplitterEngine hay tên khác)
from ai.scene_splitter.splitter import SceneSplitterEngine


def run_sprint6_architecture_test():
	print("============ NGHIỆM THU KIẾN TRÚC MỚI SPRINT 6 (DATACLASS) ============")
	
	# Văn bản truyện chữ mẫu thô chuẩn tuyệt đối từ hình ảnh của bạn
	mock_script = "Tô Mộc mở mắt.\nGiáo viên bước vào.\nMọi người kinh ngạc."
	
	# Khởi chạy động cơ bẻ cảnh hướng đối tượng v1.0
	engine = SceneSplitterEngine(chapter_number=1, chapter_title="Khởi Đầu", raw_content=mock_script)
	scene_objects_list = engine.split_into_objects()
	
	print(f"Hệ thống: Đã tự động sinh ra {len(scene_objects_list)} thực thể SceneObject.\n")
	
	# Kiểm tra kiểu dữ liệu đầu ra để chứng minh "Mọi module đều làm việc với Scene Object"
	for obj in scene_objects_list:
		print(f" -> Khởi tạo thành công: {obj.id}")
		print(f"    Nội dung kịch bản chữ thô: '{obj.summary}'")
		print(f"    Kiểu dữ liệu thực thể: {type(obj)}\n")
		
	print("=======================================================================\n")

if __name__ == "__main__":
	run_sprint6_architecture_test()
