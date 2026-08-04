from src.services.project_service import ProjectService

service = ProjectService()

def create_project(name):

    return service.create_project(name)