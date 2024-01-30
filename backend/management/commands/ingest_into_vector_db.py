# python manage.py ingest_into_vector_db
import os
from django.core.management.base import BaseCommand
from backend.models import Product
from tqdm import tqdm
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document


load_dotenv(dotenv_path=Path(
    __file__).parent.parent.parent.parent.absolute() / '.env')

dim = 1536


def use_angle():
    print("Using Angle UAE")
    Product.objects.all()
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

    faiss.write_index(index, "products_angle.index")


def get_openai_embedding(text, client, model="text-embedding-3-small"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding


def use_openai():
    print("***Using OpenAI***")

    embeddings = OpenAIEmbeddings()
    # products_details = []
    # index = 0
    # batch_size = 100
    # for product in tqdm(total=Product.objects.count(), iterable=Product.objects.all()):
    #     text_for_vector = product.text_for_vector
    #     text_for_vector = text_for_vector.replace("\n", " ")
    #     products_details.append(
    #         Document(page_content=text_for_vector, metadata=dict(page=product.id)))

    # db = FAISS.from_documents(products_details, embeddings)
    # db.save_local("products_openai_index")

    new_db = FAISS.load_local("products_openai_index", embeddings)
    num_documents = len(new_db.index_to_docstore_id)
    print("Number of documents in the index: ", num_documents)
    from pprint import pprint
    pprint(new_db.similarity_search_with_score(
        query="Skinny fit jeans for men under 2000"))

    # db.save_local("products_openai_index")
    # new_db = FAISS.load_local("products_openai_index", embeddings)
    # print(new_db.similarity_search_with_score(
    #     "What is the best way to learn AI?"))

    # openai_embedding.embed_query(text_for_vector)
    # print(embeddings)
    # import pdb
    # pdb.set_trace()
    # break

    pass


class Command(BaseCommand):
    help = 'Create vector embeddings for products and ingest into vector DB'

    def add_arguments(self, parser):
        parser.add_argument('--model', action='store', type=str, required=True)

    def handle(self, *args, **options):
        # Parse the argument
        model_name = options['model']
        if model_name == 'openai':
            use_openai()  # index is already created
            pass
        else:
            from angle_emb import AnglE, Prompts
            import faiss
            use_angle()
