from sqlalchemy.orm import Session
from core.logger import studio_logger

class ProductionWorkflowEngine:
	def __init__(self, db_session: Session):
		"""Khởi tạo Động cơ điều phối quy trình sản xuất tự động - Production Workflow v1.0"""
		self.db = db_session
		self.current_stage = "chapter" # Mặc định bắt đầu từ nấc chapter

	def advance_workflow_stage(self, current_stage: str) -> str:
		"""
		[PRODUCTION WORKFLOW PIPELINE - SPRINT 10]
		Điều phối chu trình dịch chuyển dữ liệu qua 5 nấc nghiêm ngặt của ChatGPT:
		chapter -> scene -> shot -> prompt -> videos.
		"""
		workflow_stages = ["chapter", "scene", "shot", "prompt", "videos"]
		stage_lower = current_stage.lower().strip()

		if stage_lower not in workflow_stages:
			raise ValueError(f"Nấc quy trình '{current_stage}' không tồn tại trong thiết kế của DreamForge!")

		current_index = workflow_stages.index(stage_lower)
		
		# Nếu đã chạm đến nấc cuối cùng (videos), khóa trạng thái hoàn thành
		if current_index == len(workflow_stages) - 1:
			next_stage = "videos"
			studio_logger.logger.info("[WORKFLOW] [✓] Toàn bộ chu trình sản xuất của phân cảnh đã hoàn thành xuất xưởng!")
		else:
			next_stage = workflow_stages[current_index + 1]
			studio_logger.logger.info(f"[WORKFLOW] Dịch chuyển mạch sản xuất: [{stage_lower.upper()}] ➔ ➔ ➔ [{next_stage.upper()}]")

		return next_stage
