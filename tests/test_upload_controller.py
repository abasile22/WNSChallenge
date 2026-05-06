import pytest
from unittest.mock import Mock, patch
from app.adapters.controllers.upload_controller import UploadController


class TestUploadController:
    @pytest.fixture
    def mock_meal_repository(self):
        return Mock()

    @pytest.fixture
    def mock_process_use_case(self):
        return Mock()

    def test_process_files_success(self, mock_meal_repository, mock_process_use_case):
        with patch('app.adapters.controllers.upload_controller.MealRepository', return_value=mock_meal_repository):
            with patch('app.adapters.controllers.upload_controller.ProcessFilesUseCase', return_value=mock_process_use_case):
                mock_files = [
                    Mock(filename="test.md", read=lambda: b"content1"),
                    Mock(filename="test.pdf", read=lambda: b"content2"),
                    Mock(filename="test.xlsx", read=lambda: b"content3"),
                ]

                controller = UploadController()
                result = controller.process_files(mock_files)

                assert result["success"] is True
                assert result["message"] == "Archivos procesados correctamente"
                mock_process_use_case.execute.assert_called_once()

    def test_process_files_wrong_count(self):
        with patch('app.adapters.controllers.upload_controller.MealRepository'):
            with patch('app.adapters.controllers.upload_controller.ProcessFilesUseCase'):
                mock_files = [
                    Mock(filename="test.md", read=lambda: b"content1"),
                    Mock(filename="test.pdf", read=lambda: b"content2"),
                ]

                controller = UploadController()
                result = controller.process_files(mock_files)

                assert result["success"] is False
                assert "Se requieren exactamente 3 archivos" in result["error"]

    def test_process_files_exception(self, mock_meal_repository, mock_process_use_case):
        with patch('app.adapters.controllers.upload_controller.MealRepository', return_value=mock_meal_repository):
            with patch('app.adapters.controllers.upload_controller.ProcessFilesUseCase', return_value=mock_process_use_case):
                mock_process_use_case.execute.side_effect = Exception("Processing error")

                mock_files = [
                    Mock(filename="test.md", read=lambda: b"content1"),
                    Mock(filename="test.pdf", read=lambda: b"content2"),
                    Mock(filename="test.xlsx", read=lambda: b"content3"),
                ]

                controller = UploadController()
                result = controller.process_files(mock_files)

                assert result["success"] is False
                assert "Processing error" in result["error"]
                mock_meal_repository.close.assert_called_once()

    def test_process_files_finally_closes_connection(self, mock_meal_repository, mock_process_use_case):
        with patch('app.adapters.controllers.upload_controller.MealRepository', return_value=mock_meal_repository):
            with patch('app.adapters.controllers.upload_controller.ProcessFilesUseCase', return_value=mock_process_use_case):
                mock_files = [
                    Mock(filename="test.md", read=lambda: b"content1"),
                    Mock(filename="test.pdf", read=lambda: b"content2"),
                    Mock(filename="test.xlsx", read=lambda: b"content3"),
                ]

                controller = UploadController()
                controller.process_files(mock_files)

                mock_meal_repository.close.assert_called_once()
