'''
search_food/views.py
This file contains the principals views. That is the heart of the app.
'''
from urllib.request import urlopen
import json
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from unidecode import unidecode
from .models import Product, SubstituteProduct, Favorite, PBLanguage
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django_email_verification import sendConfirm
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.translation import gettext as _
from .translation import translate_po
import polib
from django.core import management


class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        return super().default(obj)


##########################################
#             USER ACCOUNT               #
##########################################


def user_account(request):
    '''
    Method post to retrieve all informations from the signup form.
    '''
    email = request.POST.get('email')
    password = request.POST.get('password1')
    username = request.POST.get('username')
    error_message = ""

    check_email_exist = User.objects.filter(email=email)
    if not check_email_exist:
        user = get_user_model().objects.create(
            username=username,
            password=password,
            email=email)
        user.set_password(password)
        sendConfirm(user)
    else:
        error_message = _("This email is already taken !")
        render(
        request,
        'standard/index.html', {'error_message': error_message}
        )

    return render(
        request,
        'standard/mail_confirmation.html', {'error_message': error_message}
        )


def login_user(request):
    '''
    Check login and password to login.
    '''
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    print(user)
    if user is not None and user.is_active:
        login(request, user)
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'standard/index.html', {
        'login_message':
        _('This user does not exists or you did not validate'
        'your email.'),
        'anchor': 'account'})


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


def password_reset_request(request): # pragma : no-cover
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject =_("Password Reset Requested")
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Pur Beurre',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, settings.EMAIL_HOST_USER, [
                                    user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse(_('Invalid header found.'))
                    return redirect("/search_food/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(
        request=request,
        template_name="password/password_reset.html",
        context={"password_reset_form": password_reset_form}
        )


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
    else:
        display_informations(final_term_string)

    informations_displayed = display_informations(final_term_string)
    print("------------All informations will be displayed------------")

    return informations_displayed


def call_api_for_product(product):
    '''
    Private method to call the OpenFF API, retrieve products and return the
    json dictionnary.
    '''
    url = "https://world.openfoodfacts.org/cgi/search.pl?search_terms=%s&" \
        "action=process&json=1&page_size=10" % (product)
    result = urlopen(url)
    json_result = json.load(result)
    product_dict = json_result["products"]

    return product_dict


def call_api_for_category(category):
    '''
    Private method to call the OpenFF API, retrieve category and return the
    json dictionnary.
    '''
    category_clean = unidecode(category)
    url = "https://world.openfoodfacts.org/cgi/search.pl?action=process&" \
        "tagtype_0=categories&tag_contains_0=contains&tag_0=%s&page_size=" \
        "100&axis_x=energy&axis_y=products_n&action=display&json=1" \
        % (category_clean)
    result = urlopen(url)
    json_result = json.load(result)
    categ_product = json_result['products']

    return categ_product

##########################################
#          SEARCH IN DATABASE            #
##########################################


def search_and_stock(request):
    '''
    Get the keyword from the input form the laucnh the OPen Food Facts API
    call.
    '''
    term = request.POST.get('search_term')
    if term:
        final_information = treat_input_term(term)
        if not final_information:
            return render(request, 'standard/product_not_found.html')
        else:
            original_search = final_information[0].search
            return render(request, 'standard/product.html', {
                'products': final_information, 'original': original_search})
    else:
        return render(request, 'standard/product_not_found.html')


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

    check_auth = request.user.username

    if check_auth != '':
        favorites = Favorite.objects.filter(user_associate=request.user)
    else:
        favorites = {}
    return render(request, 'standard/substitute.html', {
        'substitutes': substitutes,
        'favorites': favorites,
        'original': original_product})


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
            description = _("No description")
            name = _("No name")
            salt = 0.0
            fat = 0.0
            sugar = 0.0
            nutriscore = _("No nutriscore")
            barcode = 100000
            image = _("No image")

        if nutriscore == _("No nutriscore") or \
            name == _("No name") or \
                name == "":
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
    Change the nutriscore in the database entry to sort it simplier in the
    template
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
        message_nutriscore = _("No nutriscore.")
        return message_nutriscore
    return nutriscore


def check_search(search):  # pragma : no-cover
    '''
    Check if the search is in database or not.
    '''
    if Product.objects.filter(search=search.lower()):
        return Product.objects.filter(search=search.lower())
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
            description = _("No description")
            name = _("No name")
            salt = 0.0
            fat = 0.0
            sugar = 0.0
            nutriscore = _("No nutriscore")
            barcode = 100000
            image = _("No image")
            search = _("No research")

        else:
            if nutriscore == _("No nutriscore") or \
                name == _("No name") or \
                    name == "":
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
        test_existing_sub = SubstituteProduct.objects.filter(
            barcode=data_dict['barcode']).values('barcode')[0]['barcode']
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
        barcode=product_associate.barcode,
        image=product_associate.image)
    print("-----------The favorite was added into database---------------")


def delete_entries():  # pragma : no-cover
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
    if not request.POST:
        byte_barcode = request.body.decode('utf-8')
        barcode = int(byte_barcode.split('barcode=')[1])
    else:
        barcode = request.POST.get('barcode')
    user = request.user
    add_favorite_database(int(barcode), user)

    message = _("Well added to favorites")

    data = {
        'message': message,
    }
    return JsonResponse(data, safe=False)

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
        message_information = _("This product is not in database anymore ")
        return message_information


def display_favorite(request):
    '''
    Display the favorite products from the substitute saved by users.
    '''
    actual_user = request.user
    retrieve_favorite = Favorite.objects.filter(user_associate=actual_user)

    return render(request, 'standard/favorite.html', {
        'product': retrieve_favorite})


def mention(request):
    '''
    Display the legal mentions page.
    '''

    return render(request, 'standard/mention-legales.html')

##########################################
#             CRON OPERATION             #
##########################################


def cron_database_fill(request): # pragma : no-cover
    keyword = "Nutella"
    new_entry = list(treat_input_term(keyword))
    data = serialize('json', new_entry, cls=LazyEncoder)

    return JsonResponse(data, safe=False)

##########################################
#             LANGUAGES                  #
##########################################

def manage_languages(request): # pragma : no-cover
    '''
    Display the installed languages and languages to install.
    '''
    language_model = PBLanguage.objects.all()
    all_languages = dict(settings.LANGUAGES)
    language_installed = []
    code = []

    for key, item in all_languages.items():
        check_exist = language_model.filter(language_code=key)
        if check_exist:
            language_installed.append(item)
            code.append(key)

    return render(request, 'standard/manage_languages.html', {'installed': language_model, 'code': code})

def install_language(request): # pragma : no-cover
    '''
    Install the desire language for the website
    '''
    language_code = request.POST.get('language')
    all_languages = dict(settings.LANGUAGES)
    language_name = all_languages[language_code]

    try:
        translate_po(language_code)
        PBLanguage.objects.create(language_code=language_code, language_name=language_name)
        message = _("The translation is a success. You can swap language clicking the languages icon.")
    except:
        message = _("There was a problem during the translation please try again or contact the developer.")
    
    return redirect('/' + language_code)

def modify_language_display(request): # pragma : no-cover
    '''
    Manage the language to modify some translations.
    '''
    language_code = request.POST.get('language_code')
    if language_code == "zh-hans":
        language_code = "zh"
    path = 'locale/' + language_code + '/LC_MESSAGES/django.po'
    po = polib.pofile(path)
    po_file_dict = {}

    for entry in po:
        po_file_dict[entry.msgid] = entry.msgstr

    return render(request, 'standard/modify_language.html', {'po': po_file_dict, 'language_code': language_code})
    
def modify_language(request): # pragma : no-cover
    '''
    Modify and save translations in po file.
    '''
    create_dict = {}
    for k,v in request.POST.items():
        if k != 'csrfmiddlewaretoken' and k != 'language_code' and v:
            create_dict[k] = v
    
    language_code = request.POST.get('language_code')
    if language_code == "zh-hans":
        language_code = "zh"
    path = 'locale/' + language_code + '/LC_MESSAGES/django.po'
    po = polib.pofile(path)

    for entry in po:
        if entry.msgid in create_dict:
            entry.msgstr = create_dict[entry.msgid]
            
    po.save(path)
    management.call_command('compilemessages')
    
    return render(request, 'standard/modify_translate_done.html', {'message': _('Traductions are modified and saved.')})

def uninstall_language(request, code): # pragma : no-cover
    import os
    import shutil

    if code == "zh":
        current_language = PBLanguage.objects.filter(language_code="zh-hans")
    else:
        current_language = PBLanguage.objects.filter(language_code=code)
    
    current_language.delete()
    cwd = os.getcwd()
    path = cwd +'/locale/'+ code
    shutil.rmtree(path)
    
    return redirect('/en')
