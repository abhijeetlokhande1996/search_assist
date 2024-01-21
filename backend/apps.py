from django.apps import AppConfig
from config import DATA_DIR
import faiss


class BackendConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend"

    def ready(self):
        pass
