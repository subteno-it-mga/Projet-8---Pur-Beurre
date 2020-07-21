'''
search_food/database_fill.py
This file  contains the custom command to pre-fill the database.
'''
import json
from urllib.request import urlopen
from .models import Product, User


def get_files():
    '''
    Get the informations from the openfoodfact API.
    '''
    db_product = 'nutella'
    db_url = "https://world.openfoodfacts.org/cgi/search.pl?search_terms=%s&" \
        "action=process&json=1&page_size=10" % (db_product)
    db_result = urlopen(db_url)
    db_json_result = json.load(db_result)
    db_product_dict = db_json_result["products"]

    return db_product_dict


def pre_fill_database():
    '''
    We fill the database with the informations obtained from get_files
    function.
    '''
    product = get_files()
    try:
        description = product[0]["generic_name"]
        name = product[0]["product_name"]
        salt = product[0]["nutriments"]["salt"]
        sugar = product[0]["nutriments"]["sugars"]
        fat = product[0]["nutriments"]["fat"]
        nutriscore = product[0]["nutrition_grades"]
        barcode = product[0]["code"]
        image = product[0]["image_front_url"]
        category = product[0]["compared_to_category"]

        Product.objects.create(
            description=description,
            name=name,
            salt=salt,
            sugar=sugar,
            fat=fat,
            nutriscore=nutriscore,
            barcode=barcode,
            image=image,
            category=category,
            search='nutella-fill'
        )
        print("Product is in database.")

    except KeyError:

        print("Can't access to the data.")


def clean_database():
    '''
    Clean database for the custom command
    '''
    product_delete = Product.objects.filter(search="nutella-fill")
    product_delete.delete()
    print("Product deleted.")

def create_user(name, mail, password):
    '''
    Fill database for tests
    '''
    User.objects.create_user(
            name, mail, password)