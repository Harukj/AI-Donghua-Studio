import os

class ProjectService:

    ROOT_FOLDER = "projects"

    def create_project(self, name):

        project = os.path.join(self.ROOT_FOLDER, name)

        folders = [

            "characters",

            "environments",

            "storyboard",

            "episodes",

            "audio",

            "videos",

            "exports",

            "assets",

            "cache"

        ]

        os.makedirs(project, exist_ok=True)

        for folder in folders:

            os.makedirs(
                os.path.join(project, folder),
                exist_ok=True
            )

        return project