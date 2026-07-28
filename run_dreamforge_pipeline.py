import json
import sys
import os

# Tiêm đường dẫn chạy runtime an toàn cho Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database.session import SessionLocal
from src.database.base import Base
from src.database.engine import engine
from src.ai.prompt_builder.builder_v3 import PromptBuilder30

def run_dreamforge_production_pipeline():
	print("============ KÍCH HOẠT DÂY CHUYỀN SẢN XUẤT DREAMFORGE ENGINE V1.0 ============")
	
	# Khởi tạo hạ tầng bảng dữ liệu SQLite an toàn
	Base.metadata.create_all(bind=engine)
	db = SessionLocal()

	# 1. Văn bản kịch bản thô đầu vào lấy chính xác 100% từ ảnh mẫu của bạn
	raw_story_paragraph = "Tô Mộc bất ngờ quay đầu."
	print(f"Kịch bản truyện văn học đầu vào: \"{raw_story_paragraph}\"\n")

	# 2. Gói chỉ đạo nghệ thuật thực tế do AI Đạo diễn bóc tách từ ảnh mẫu của ChatGPT
	ai_director_directives = {
		"emotion": "surprised",
		"camera": "Close Up",
		"lens": "85mm",
		"movement": "Quick Pan",
		"lighting": "Cold Light",
		"duration": 3.5
	}

	# 3. Kích hoạt cỗ máy sinh câu lệnh Ma trận 3.0 trộn dữ liệu cơ học
	mixer = PromptBuilder30(db)
	final_production_package = mixer.build_matrix_prompt_v3(
		char_name="Tô Mộc",
		location_name="Học viện Long Dạng",
		raw_action_text=raw_story_paragraph,
		directives=ai_director_directives
	)

	# 4. Bung kết quả cấu trúc Token xuất xưởng ra màn hình Terminal
	print("-----------------------------------------------------------------------------")
	print(f"🎬 [FINAL VIDEO CONFIGURATION] | Thời lượng clip AI: {final_production_package['duration']} giây")
	print(f"\n Câu lệnh Positive Prompt cấp cho LTX Queue:\n \"{final_production_package['positive']}\"")
	print(f"\n Câu lệnh Negative Prompt cấp cho LTX Queue:\n \"{final_production_package['negative']}\"")
	print("-----------------------------------------------------------------------------")
	
	db.close()
	print("[SUCCESS] Quy trình sản xuất tự động khép kín của Sprint 10 vận hành hoàn hảo 100%!")

if __name__ == "__main__":
	run_dreamforge_production_pipeline()
