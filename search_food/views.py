from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from urllib.request import urlopen
import json
from django.http import JsonResponse
from django.contrib.auth import logout
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views import View

from unidecode import unidecode
from django.views.decorators.csrf import csrf_exempt
from .models import Product, SubstituteProduct, Favorite

from django.urls import reverse

# test

##########################################
#             USER ACCOUNT               #
##########################################

def user_account(request):
    '''
    Method post to retrieve all informations from the signup form.
    '''
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()

        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(request, user)

        messages.add_message(request, messages.INFO, form.cleaned_data['username'])
        return HttpResponseRedirect(reverse('signup'))

    else:
        form = UserCreationForm()
        return render(request, 'standard/index.html', {'form': form})

def login_user(request):
    '''
    Check login and password to login.
    '''
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)

    if user is not None and user.is_active:
        login(request, user)
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
    else:
        return render(request, 'standard/index.html', {'login_message':'The user doesn\'t exist','anchor':'account'})
    # return render(request, 'standard/index.html')

def logout_user(request):
    '''
    Logout the user if he's connnected.
    '''
    logout(request)
    return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)

def signup(request):
    '''
    Return a page when the user created an account.
    '''
    return render(request, 'standard/signup.html')


##########################################
#          CALL API AND PARSER           #
##########################################

def treat_input_term(keyword):
    '''
    This function split and treat the keywords and call OpenFF API.
    '''
    keyword = unidecode(keyword)
    list_term = keyword.split(" ")
    final_term_list = []

    for item in list_term:

        if list_term[len(list_term) - 1] == item:
            final_term_list.append(item)
        else:
            new_item = "".join(item + '%20')
            final_term_list.append(new_item)

    final_term_string = ''.join(final_term_list)

    product = call_api_for_product(final_term_string)

    check_existing_search = check_search(final_term_string)

    if not check_existing_search:
        create_entries(product, final_term_string)
        print("-----------------We create products in Database--------------------------")
    else:
        display_informations(final_term_string)
        print("-----------------Directly display the products because they already are in base--------------------------")

    informations_displayed = display_informations(final_term_string)
    print("------------All informations will be displayed------------")

    return informations_displayed

def call_api_for_product(product):
    '''
    Private method to call the OpenFF API, retrieve products and return the json dictionnary.
    '''
    url = "https://world.openfoodfacts.org/cgi/search.pl?search_terms=%s&action=process&json=1&page_size=10" % (product)
    result = urlopen(url)
    json_result = json.load(result)
    product_dict = json_result["products"]

    return product_dict

def call_api_for_category(category):
    '''
    Private method to call the OpenFF API, retrieve category and return the json dictionnary.
    '''
    category_clean = unidecode(category)
    url = "https://world.openfoodfacts.org/cgi/search.pl?action=process&tagtype_0=categories&tag_contains_0=contains&tag_0=%s\&page_size=100&axis_x=energy&axis_y=products_n&action=display&json=1" % (category_clean)
    result = urlopen(url)
    json_result = json.load(result)
    categ_product = json_result['products']

    return categ_product

##########################################
#          SEARCH IN DATABASE            #
##########################################

def search_and_stock(request):
    '''
    Get the keyword from the input form the laucnh the OPen Food Facts API call.
    '''
    term = request.POST.get('search_term')

    final_information = treat_input_term(term)
    original_search = final_information[0].search
    return render(request, 'standard/product.html', {'products': final_information, 'original': original_search})

def search_substitute(request):
    '''
    This search subsitutes from the category of the product.
    '''
    product = request.POST.get('product_barcode')
    original_product = Product.objects.get(barcode=product)
    product_category = search_categories(product)
    retrieve_substitute(product_category, original_product)

    print("------------Add Products with the same category------------")

    substitutes = display_substitutes(original_product)
    favorites = Favorite.objects.filter(user_associate=request.user)
    import pdb; pdb.set_trace()
    return render(request, 'standard/substitute.html', {'substitutes': substitutes, 'favorites': favorites, 'original': original_product})


def retrieve_substitute(product_category, original_product):
    '''
    This function call the OpenFF API and store it in database.
    '''
    categ_product = call_api_for_category(product_category)
    # Loop and search for products into this json dictionnary
    for product in categ_product:
        try:
            description = product["generic_name"]
            name = product["product_name"]
            salt = product["nutriments"]["salt"]
            sugar = product["nutriments"]["sugars"]
            fat = product["nutriments"]["fat"]
            nutriscore = product["nutrition_grades"]
            barcode = product["code"]
            image = product["image_front_url"]
            category = product["compared_to_category"]

        except KeyError:
            description = "Pas de description"
            name = "Pas de nom"
            salt = 0.0
            fat = 0.0
            sugar = 0.0
            nutriscore = "Pas de nutriscore"
            barcode = 100000
            image = "No image"

        if nutriscore == "Pas de nutriscore" or name == "Pas de nom" or name == "":
            pass
        else:
            nutriscore_db = change_nutriscore(nutriscore)

            data_dictionnary = {
                'product': name,
                'salt': salt,
                'sugar': sugar,
                'fat': fat,
                'description': description,
                'image': image,
                'nutriscore': nutriscore_db,
                'barcode': barcode,
                'category': category,
                'original': original_product,
            }
            add_substitute_products(data_dictionnary)

def change_nutriscore(nutriscore):
    '''
    Change the nutriscore in the database entry to sort it simplier in the template
    '''
    if nutriscore == "a":
        nutriscore = 1
    elif nutriscore == "b":
        nutriscore = 2
    elif nutriscore == "c":
        nutriscore = 3
    elif nutriscore == "d":
        nutriscore = 4
    elif nutriscore == "e":
        nutriscore = 5
    else:
        message_nutriscore = "Pas de Nutriscore ?"
        return message_nutriscore

    return nutriscore

def check_search(search):
    '''
    Check if the search is in database or not.
    '''
    if Product.objects.filter(search=search.lower()):
        return Product.objects.filter(search=search.lower())
    else:
        return False

def create_entries(informations, final_term_string):
    '''
    Create the entries in database for the searched product.
    '''
    print("-------------We are creating products-------------")

    for product in informations:
        try:
            description = product["generic_name"]
            name = product["product_name"]
            salt = product["nutriments"]["salt"]
            sugar = product["nutriments"]["sugars"]
            fat = product["nutriments"]["fat"]
            nutriscore = product["nutrition_grades"]
            barcode = product["code"]
            image = product["image_front_url"]
            category = product["compared_to_category"]
            search = final_term_string.lower()

        except KeyError:
            description = "Pas de description"
            name = "Pas de nom"
            salt = 0.0
            fat = 0.0
            sugar = 0.0
            nutriscore = "Pas de nutriscore"
            barcode = 100000
            image = "No image"
            search = "Pas de recherche"

        else:
            if nutriscore == "Pas de nutriscore" or name == "Pas de nom" or name == "":
                pass  # pragma : no-cover
            else:
                if Product.objects.filter(barcode=barcode):
                    pass  # pragma : no-cover
                else:
                    nutriscore_modified = change_nutriscore(nutriscore)
                    Product.objects.create(
                        name=name,
                        salt=salt,
                        sugar=sugar,
                        fat=fat,
                        nutriscore=nutriscore_modified,
                        barcode=barcode,
                        description=description,
                        image=image,
                        category=category,
                        search=search)
    print("---------------All products are correctly in base------------")

def add_substitute_products(data_dict):
    '''
    Add all substitute in the database.
    '''
    try:
        test_existing_sub = SubstituteProduct.objects.filter(barcode=data_dict['barcode']).values('barcode')[0]['barcode']
        if data_dict['barcode'] != str(test_existing_sub):
            SubstituteProduct.objects.create(
                name=data_dict['product'],
                salt=data_dict['salt'], sugar=data_dict['sugar'],
                fat=data_dict['fat'],
                nutriscore=data_dict['nutriscore'],
                barcode=data_dict['barcode'],
                description=data_dict['description'],
                image=data_dict['image'],
                category=data_dict['category'],
                original=data_dict['original'])
        else:
            print("Le produit existe déjà.")
    except IndexError:
        SubstituteProduct.objects.create(
                name=data_dict['product'],
                salt=data_dict['salt'], sugar=data_dict['sugar'],
                fat=data_dict['fat'],
                nutriscore=data_dict['nutriscore'],
                barcode=data_dict['barcode'],
                description=data_dict['description'],
                image=data_dict['image'],
                category=data_dict['category'],
                original=data_dict['original'])

def add_favorite_database(favorite, user):
    '''
    Add a substitute product in the database depends of the user.
    '''
    product_associate = SubstituteProduct.objects.get(barcode=favorite)
    SubstituteProduct.objects.filter(barcode=favorite).update(in_favorite=True)
    Favorite.objects.create(
        product_associate=product_associate.original,
        user_associate=user,
        product_name=product_associate.name,
        barcode=product_associate.barcode)
    print("-----------The favorite was added into database---------------")

def delete_entries(request):
    '''
    Erase all database entries. ONLY FOR THE ADMIN.
    '''
    delete_all_entries()

    print("--------------All entries cleaned-------------")

    return HttpResponseRedirect('/')

@csrf_exempt
def add_favorite(request):
    '''
    Add a substitute product in the database depend of the user.
    '''
    barcode = request.POST.get('barcode')
    user = request.user
    add_favorite_database(int(barcode), user)

    message = "bien ajouté aux favoris"

    data = {
        'message': message,
    }
    return JsonResponse(data)

def delete_all_entries():
    '''
    Delete all the entries in the database. ONLY FOR ADMIN.
    '''
    Product.objects.all().delete()
    SubstituteProduct.objects.all().delete()
    Favorite.objects.all().delete()

##########################################
#             RENDER TEMPLATE            #
##########################################

def index(request):
    '''
    Display the form in the main page.
    '''
    form = UserCreationForm
    return render(request, 'standard/index.html', {'form': form})

def display_informations(search):
    '''
    Search all original products in Database.
    '''
    return Product.objects.filter(search=search.lower())

def display_substitutes(original_product):
    '''
    Display all product substitute from the original product.
    '''
    return SubstituteProduct.objects.filter(original=original_product)

def search_categories(barcode):
    '''
    Search Categories in the database to retrieve them in the api.
    '''
    try:
        product_categories = Product.objects.get(barcode=barcode)
        return product_categories.category
    except Product.DoesNotExist:
        message_information = "Ce produit n'est pas ou plus présent dans la base."
        return message_information

def display_favorite(request):
    '''
    Display the favorite products from the substitute saved by users.
    '''
    actual_user = request.user
    retrieve_favorite = Favorite.objects.filter(user_associate=actual_user)

    return render(request, 'standard/favorite.html', {'product': retrieve_favorite})


