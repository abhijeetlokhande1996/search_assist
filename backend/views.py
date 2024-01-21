from angle_emb import AnglE, Prompts
import json
import faiss
from config import DATA_DIR

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from backend.models import Product

index_filepath = str(DATA_DIR / "products.index")
product_index_vstore = faiss.read_index(index_filepath)

ANGLE = AnglE.from_pretrained(
    'WhereIsAI/UAE-Large-V1', pooling_strategy='cls').cuda()
ANGLE.set_prompt(prompt=Prompts.C)
# Create your views here.


@csrf_exempt
def test(request):
    data = {"name": "John", "age": 30}
    print(product_index_vstore.ntotal)
    return JsonResponse(data)


@csrf_exempt
def search_similar_products(request):
    data = json.loads(request.body)
    query = {"text": data["query"]}

    # Encode the query
    query_embedding = ANGLE.encode(
        [query], to_numpy=True)

    # Perform similarity search
    k = 5  # Number of neighbors to retrieve
    distances, indices = product_index_vstore.search(query_embedding, k)

    response = {"products": [], "query": data["query"]}
    # Retrieve and print the results
    for distance, product_index in zip(distances[0], indices[0]):
        # Adjust this based on your Product model
        similar_product = Product.objects.all()[int(product_index)]
        response["products"].append({
            "id": similar_product.id,
            "product_name": similar_product.name,
            "price": similar_product.price,
            "description": similar_product.description,
        })

    return JsonResponse(response)
