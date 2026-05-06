from app.use_cases.process_files import ProcessFilesUseCase
from app.adapters.repositories.meal_repository import MealRepository


class UploadController:
    def __init__(self):
        self.meal_repository = MealRepository()
        self.process_files_use_case = ProcessFilesUseCase(self.meal_repository)

    def process_files(self, files: list) -> dict:
        try:
            if len(files) != 3:
                return {
                    "success": False,
                    "error": f"Se requieren exactamente 3 archivos. Recibido: {len(files)}"
                }

            files_data = [
                {
                    "filename": f.filename,
                    "content": f.read()
                }
                for f in files
            ]

            self.process_files_use_case.execute(files_data)

            return {
                "success": True,
                "message": "Archivos procesados correctamente"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
        finally:
            self.meal_repository.close()
