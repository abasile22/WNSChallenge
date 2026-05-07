import threading
from datetime import date, datetime, timedelta, timezone
import os
import logging

from flask import Flask, render_template, request, jsonify

from app.adapters.controllers.meal_controller import MealController
from app.adapters.controllers.upload_controller import UploadController

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Routes:
    def __init__(self):
        app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ''))
        template_folder = os.path.join(app_dir, 'templates')
        static_folder = os.path.join(app_dir, 'static')
        self.app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
        self.meal_controller = MealController()
        self.upload_controller = UploadController()
        self.loading_state = {"complete": True}
        self.state_lock = threading.Lock()

    def create_app(self):
        self._setup_routes()
        return self.app

    def _setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template("data_load.html")

        @self.app.route('/api/meals/search')
        def index_render():
            meals = self.meal_controller.get_all_meals()
            tz_arg = timezone(timedelta(hours=-3))
            today = datetime.now(tz_arg).date().isoformat()
            return render_template("meals_search.html", meals=meals, today=today)

        @self.app.route('/api/loading', methods=['POST'])
        def save_meals():
            files = request.files.getlist("input_file")

            # Validar cantidad de archivos
            if len(files) != 3:
                meals = self.meal_controller.get_all_meals()
                error = f"Se requieren exactamente 3 archivos. Recibido: {len(files)}"
                return render_template("data_load.html", meals=meals, error=error)

            with self.state_lock:
                self.loading_state["complete"] = False

            thread = threading.Thread(target=self._process_files_async, args=(files,))
            thread.start()

            return render_template("loading.html")

        @self.app.route("/api/check-load-status")
        def check_load_status():
            from flask import jsonify
            with self.state_lock:
                is_complete = self.loading_state["complete"]
            return jsonify({"ready": is_complete})

        @self.app.route("/api/meals/data", methods=["POST"])
        def get_meal_data():
            body = request.get_json()

            if not body:
                logger.error("Body vacío o no es JSON")
                return jsonify({"error": "Body vacío o no es JSON"}), 400

            if 'meal' not in body or 'date' not in body:
                logger.error(f"Faltan campos. Body: {body}")
                return jsonify({"error": "Faltan campos: meal, date"}), 400

            tz_arg = timezone(timedelta(hours=-3))
            today = datetime.now(tz_arg).date()
            thirty_days_ago = today - timedelta(days=30)
            user_date = datetime.strptime(body['date'], "%Y-%m-%d").date()

            if user_date < thirty_days_ago or user_date > today:
                logger.error(f"Fecha fuera de rango. Body: {body}")
                return jsonify({"error": "La fecha ingresada no es válida, solo se permiten fechas dentro de los últimos 30 días."}), 400

            response = self.meal_controller.get_meal_data(body['meal'], body['date'])
            return response

    def _process_files_async(self, files):
        try:
            logger.info("Iniciando procesamiento de archivos...")
            files_data = [
                {
                    "filename": f.filename,
                    "content": f.read()
                }
                for f in files
            ]

            # Procesar directamente con use case
            from app.use_cases.process_files import ProcessFilesUseCase
            from app.adapters.repositories.meal_repository import MealRepository

            repo = MealRepository()
            use_case = ProcessFilesUseCase(repo)
            use_case.execute(files_data)
            repo.close()

            logger.info("Archivos procesados exitosamente")
        except Exception as e:
            logger.error(f"Excepción durante procesamiento: {str(e)}", exc_info=True)
        finally:
            with self.state_lock:
                self.loading_state["complete"] = True
