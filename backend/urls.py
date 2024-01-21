from django.urls import include, path
from . import views


urlpatterns = [
    path("test/", views.test, name="test"),
    path("search_similar_products/", views.search_similar_products,
         name="search_similar_products"),

]
