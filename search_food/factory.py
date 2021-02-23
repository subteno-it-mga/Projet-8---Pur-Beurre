import factory
from django.contrib.auth import get_user_model

from django.contrib.auth.hashers import make_password
User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username', 'password')

    username = 'jeff'
    password = make_password('testuserpassword61')
    email = "jeff@bezos.fr"
    is_superuser = False
    is_active = True

class UserAdminFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username', 'password')

    username = 'admin'
    password = make_password('admin')
    email = "admin@admin.fr"
    is_superuser = True
    is_active = True


class UserMailFactory(factory.django.DjangoModelFactory):
    '''
    This model will be use to tests email feature.
    '''
    class Meta:
        model = User


class ProductGenericFactory(factory.django.DjangoModelFactory):
    '''
    Create a generic product to fill in the test database
    '''
    class Meta:
        model = 'search_food.Product'
        django_get_or_create = ('name', 'description', 'nutriscore', 'category',
        'fat', 'sugar', 'salt', 'barcode', 'image', 'search')

    name='Nutella model'
    description='testdescription'
    category='pâte à tartiner'
    fat=1
    salt=1
    image='nutella.jpg'
    sugar=1
    nutriscore=4
    barcode=123456789
    search='nutella'


class ProductSubstituteFactory(factory.django.DjangoModelFactory):
    '''
    Create a product substitute to fill in the test database
    '''
    class Meta:
        model = 'search_food.SubstituteProduct'


class FavoriteFactory(factory.django.DjangoModelFactory):
    '''
    Create a favorite to fill in the test database
    '''
    class Meta:
        model = 'search_food.Favorite'


class PBLanguageFactory(factory.django.DjangoModelFactory):
    '''
    Factory of the model PBLanguage to tests languages installation and
    mangement
    '''
    class Meta:
        model = 'search_food.PBLanguage'

