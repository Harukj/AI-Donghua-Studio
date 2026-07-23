from sqlalchemy.orm import Session
from services.character_service import CharacterService
from services.environment_service import EnvironmentService
from database.models.camera import CameraModel

class PromptEngine:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.char_service = CharacterService(db_session)
        self.env_service = EnvironmentService(db_session)

    def get_camera_prompt(self, camera_name: str) -> str:
        """Truy vấn từ khóa cấu hình của góc máy từ danh viện"""
        camera = self.db.query(CameraModel).filter(CameraModel.name == camera_name).first()
        if camera:
            return camera.camera_prompt
        # Nếu chưa có trong DB, trả về chính tên góc máy viết thường làm prompt dự phòng
        return f"{camera_name.lower()} shot"

    def generate_scene_prompt(self, character_name: str, env_name: str, camera_name: str) -> str:
        """
        [PROMPT ENGINE GENERAL LOGIC]
        Hàm ghép tự động hoàn chỉnh: Nhân vật + Bối cảnh + Góc máy
        """
        # 1. Lấy prompt tự động cấu hình từ Character Bible
        char_prompt = self.char_service.build_ai_prompt(character_name)
        
        # 2. Lấy prompt tự động cấu hình từ Environment Bible
        env_prompt = self.env_service.build_environment_prompt(env_name)
        
        # 3. Lấy prompt từ thư viện Camera
        camera_prompt = self.get_camera_prompt(camera_name)
        
        # 4. Tiến hành ghép tự động theo cấu trúc điện ảnh chuẩn cho AI
        # Cấu trúc: [Góc máy], [Nhân vật], [Bối cảnh]
        full_scene_prompt = f"{camera_prompt}, {char_prompt}, background is {env_prompt}"
        
        return full_scene_prompt
