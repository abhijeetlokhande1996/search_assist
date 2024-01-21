from django.apps import AppConfig
from config import DATA_DIR
from config import faiss_index
import faiss


class BackendConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "backend"

    def ready(self):
        index_filepath = str(DATA_DIR / "products.index")
        index = faiss.read_index(index_filepath)
        faiss_index = index
        print("Faiss Index loaded and assigned")
