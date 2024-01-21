import pandas as pd
from django.core.management.base import BaseCommand
from django.utils import timezone
from backend.models import Product
from config import DATA_DIR
import spacy

nlp = spacy.load('en_core_web_sm')


class Command(BaseCommand):
    help = 'Ingest product data from CSV file'

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
        df = pd.read_csv(DATA_DIR / 'myntra_products_catalog.csv')
        for _, row in df.iterrows():
            product = Product()
            product.name = row['ProductName']
            product.brand = row['ProductBrand']
            product.price = row['Price (INR)']
            product.description = row['Description'].lower()
            product.primary_colour = row['PrimaryColor']
            product.gender = row["Gender"]
            product.text_for_vector = f"name = {product.name} \n brand = {product.brand} \n price = {product.price} \n  description = {product.description} \n primary_colour = {product.primary_colour} \n  gender = {product.gender}".lower()
            product.save()
