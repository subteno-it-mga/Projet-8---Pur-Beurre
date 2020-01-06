import json
from urllib.request import urlopen
from .models import Product


def get_files():
    '''
    Get the informations from the openfoodfact API.
    '''
    product = 'nutella'
    url = "https://world.openfoodfacts.org/cgi/search.pl?search_terms=%s&action=process&json=1&page_size=10" % (product)
    result = urlopen(url)
    json_result = json.load(result)
    product_dict = json_result["products"]

    return product_dict

def pre_fill_database():
    '''
    We fill the database with the informations obtained from get_files function.
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