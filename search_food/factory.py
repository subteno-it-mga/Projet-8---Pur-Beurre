import factory
from django.contrib.auth import get_user_model

from django.contrib.auth.hashers import make_password
User = get_user_model()


# class UserValidFactory(factory.django.DjangoModelFactory):
#     '''
#     Create a user model to fill in the test database
#     '''
#     class Meta:
#         model = User
    
#     username = "testuser61700"
#     password = 'testpassword61700'
#     email = "gaucher_martin@yahoo.fr"


# class UserLoginFactory(factory.django.DjangoModelFactory):
#     '''
#     Create a user model to fill in the test database
#     '''
#     class Meta:
#         model = User
    
#     username = "jacques"
#     password = 'jaja61700'
#     email = "ja@ja.fr"

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username', 'password')

    username = 'jeff'
    password = make_password('testuserpassword61')
    email = "jeff@bezos.fr"
    is_superuser = False
    is_active = True
    

    # username = factory.Sequence(lambda n: 'somename%s' % n)
    # password = factory.Sequence(lambda p: 'mysuperpass%s' % p)

    # @classmethod
    # def _create(cls, model_class, *args, **kwargs):
    #     """Override the default ``_create`` with our custom call."""
    #     kwargs['password'] = make_password(kwargs['password'])
    #     return super(UserFactory, cls)._create(model_class, *args, **kwargs)

class ProductGenericFactory(factory.django.DjangoModelFactory):
    '''
    Create a product to fill in the test database
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
    Create a product to fill in the test database
    '''
    class Meta:
        model = 'search_food.SubstituteProduct'
        # django_get_or_create = ('name', 'description', 'nutriscore', 'category',
        # 'fat', 'sugar', 'salt', 'barcode', 'image', 'original')
    
    # name='gerblé'
    # category='pâte à tartiner'
    # description='testdescriptionsub'
    # nutriscore=1
    # fat=1
    # sugar=1
    # salt=1
    # image='sub.jpg'
    # barcode=12345678910
    # original= factory.RelatedFactory(ProductGenericFactory)

class FavoriteFactory(factory.django.DjangoModelFactory):
    '''
    Create a product to fill in the test database
    '''
    class Meta:
        model = 'search_food.Favorite'
        # django_get_or_create = ('product_name', 'barcode', 'product_associate',
        # 'user_associate')

    # product_name='gerblé_fav'
    # barcode=1234567891011
    # product_associate=ProductGenericFactory()
    # user_associate=factory.RelatedFactory(UserFactory)