import pandas as pd
from django.core.management.base import BaseCommand
from backend.models import Product

import faiss
from angle_emb import AnglE, Prompts
from config import DATA_DIR


class Command(BaseCommand):
    help = 'Test FAISS'

    def handle(self, *args, **kwargs):
        # Load the pre-trained model
        angle = AnglE.from_pretrained(
            'WhereIsAI/UAE-Large-V1', pooling_strategy='cls').cuda()
        angle.set_prompt(prompt=Prompts.C)
        index_filepath = str(DATA_DIR / "products.index")
        # Load the Faiss index
        index = faiss.read_index(index_filepath)

        query = {"text": "black shirts under 1000"}
        # Encode the query
        query_embedding = angle.encode(
            [query], to_numpy=True)

        # Perform similarity search
        k = 5  # Number of neighbors to retrieve
        distances, indices = index.search(query_embedding, k)

        # Retrieve and print the results
        for distance, product_index in zip(distances[0], indices[0]):
            # Adjust this based on your Product model
            similar_product = Product.objects.all()[int(product_index)]
            print(
                f"Similarity: {1 - distance:.4f}, Product: {similar_product.text_for_vector}")
            break
