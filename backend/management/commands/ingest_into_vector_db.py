# python manage.py ingest_into_vector_db
from django.core.management.base import BaseCommand
from langchain_community.vectorstores import FAISS
from angle_emb import AnglE, Prompts

from backend.models import Product
import faiss
from tqdm import tqdm


class Command(BaseCommand):
    help = 'Create vector embeddings for products and ingest into vector DB'

    def handle(self, *args, **kwargs):

        # IndexFlatL2 for L2 (Euclidean) distance

        # Product.objects.all()
        angle = AnglE.from_pretrained(
            'WhereIsAI/UAE-Large-V1', pooling_strategy='cls').cuda()
        angle.set_prompt(prompt=Prompts.C)
        candidates_for_embedding = []
        batch_size = 10
        dim = 1024
        index = faiss.IndexFlatL2(dim)

        for product in tqdm(total=Product.objects.count(), iterable=Product.objects.all()):
            candidates_for_embedding.append({'text': product.text_for_vector})
            if len(candidates_for_embedding) >= batch_size:
                vecs = angle.encode(candidates_for_embedding, to_numpy=True)
                assert vecs.shape[1] == dim
                index.add(vecs)
                candidates_for_embedding = []  # reset
        if candidates_for_embedding:
            vecs = angle.encode(candidates_for_embedding, to_numpy=True)
            index.add(vecs)

        faiss.write_index(index, "products.index")
