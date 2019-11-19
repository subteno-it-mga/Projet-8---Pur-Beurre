from django.test import TestCase
from database.main import DatabaseManagerClass
from api.main import CallAPIClass
from django.contrib.auth.models import User
from database.models import Product, SubstituteProduct, Favorite

class DatabaseTestCase(TestCase):
    '''
    Test for products in database
    '''

    def setUp(self):
        '''
        Setting up all objects for the test. All datas will be erase after the test
        '''
        # Create a test user in the database
        self.user_test = User.objects.create_user('testuser', 'user@user.fr', 'passwordtest')

        # Create a product in the database
        self.product_test_generic = Product.objects.create(
            name='Nutella',
            description='testdescription',
            category='pâte à tartiner',
            fat=1,
            salt=1,
            image='nutella.jpg',
            sugar=1,
            nutriscore=4,
            barcode=123456789)

        # Create a substitute from the product in the database
        self.product_substitute = SubstituteProduct.objects.create(
            name='gerblé',
            category='pâte à tartiner',
            description='testdescriptionsub',
            nutriscore=1,
            fat=1,
            sugar=1,
            salt=1,
            image='sub.jpg',
            barcode=12345678910,
            original=self.product_test_generic)

        # Create favorite datas from user and substitute
        self.user_favorite = Favorite.objects.create(
            product_name='gerblé_fav',
            barcode=1234567891011,
            product_associate=self.product_substitute,
            user_associate=self.user_test)

    def test_change_nutriscore(self):
        '''
        Test if the nutriscore is well substitute.
        '''
        # Test if the nutriscore change from strong to integer for a betttr sort in the template
        test_change_nutriscore = DatabaseManagerClass.change_nutriscore(self, "a")

        self.assertEqual(test_change_nutriscore, 1)
        self.assertNotEqual(test_change_nutriscore, 2)

    def test_create_entries(self):
        '''
        Test the entries in the database. Then look if the entry exists or not.
        '''
        # Initialize a json file, a database object, then save entries in the database.
        test_json_file = CallAPIClass.call_api_for_product(self, "nutella")
        DatabaseManagerClass.create_entries(self, test_json_file)

        # Check if the products was saved in the database
        self.assertTrue(Product.objects.all().count(), Product.objects.all().count() > 5)
        self.assertEqual(Product.objects.get(barcode=test_json_file[0]['code']).name, "Nutella")

        # Check if the entries in database are all unique by their barcodes.
        for product in Product.objects.all():
            self.assertEqual(Product.objects.filter(barcode=test_json_file[0]['code']).count(), 1)

    def test_delete_all_entries(self):
        '''
        Test if all entries are deleted well after calling the delete function.
        '''
        # Get the user by his username
        test_user_object = User.objects.get(username='testuser')

        # Call the function to delete all entries
        DatabaseManagerClass.delete_all_entries(self)

        # Test if the user is not deleted when we're calling the function to delete all entries
        self.assertEqual(test_user_object.username, 'testuser')

        # Test if the database is clean from product
        self.assertQuerysetEqual(SubstituteProduct.objects.filter(barcode=123456789), [])
        self.assertQuerysetEqual(SubstituteProduct.objects.filter(barcode=12345678910), [])
        self.assertQuerysetEqual(Favorite.objects.filter(barcode=1234567891011), [])

        # Check if we don't forget an entry in database so try to search any data in database
        self.assertQuerysetEqual(Product.objects.all(), [])
        self.assertQuerysetEqual(SubstituteProduct.objects.all(), [])
        self.assertQuerysetEqual(Favorite.objects.all(), [])

    def test_display_informations(self):
        '''
        Test if we retrieve correctly all products in database.
        '''
        # Call the function which is display all products in database
        test_display = DatabaseManagerClass.display_informations(self)

        # Test if the function return a queryset of all product in database.
        self.assertQuerysetEqual(test_display, ['<Product: Nutella>'])

    def test_display_substitutes(self):
        '''
        Test if the data are saved correctly in database.
        '''
        # Get the product registered before
        test_query_product = Product.objects.get(barcode=123456789)

        # Call the function wich display substitutes from the original product
        test_substitute_query = DatabaseManagerClass.display_substitutes(self, test_query_product)

        # Test if the function return a correct queryset from the original product
        self.assertQuerysetEqual(test_substitute_query, ['<SubstituteProduct: gerblé>'])

    def test_search_categories(self):
        '''
        Test the search categories function, depends on barcode
        '''
        # Get the product registered before
        test_query_product = Product.objects.get(barcode=123456789)

        # Two queries : one to trigger the good informaions and the other to return an error
        test_search_category = DatabaseManagerClass.search_categories(self, test_query_product.barcode)
        test_search_category_wrong = DatabaseManagerClass.search_categories(self, 10203040)

        # Check the values if we enter a good or a wrong barcode
        self.assertEqual(test_search_category, 'pâte à tartiner')
        self.assertEqual(test_search_category_wrong, "Ce produit n'est pas ou plus présent dans la base.")

    def test_substitute_products(self):
        '''
        Test if the substitute are correctly saved in database
        '''
        # Get the product registered before
        test_original_product = Product.objects.get(barcode=123456789)

        test_data_dictionnary = {
            'product': 'gerblé2',
            'salt': 1,
            'sugar': 1,
            'fat': 1,
            'description': 'subtestdescription',
            'image': 'subtest.jpg',
            'nutriscore': 4,
            'barcode': 1234567891011,
            'category': 'pâte à tartiner',
            'original': test_original_product,
        }

        # Call this function to save substitute products in database
        DatabaseManagerClass.substitute_products(self, test_data_dictionnary)

        # Retrieve the substitute from his barcode
        test_query_substitute = SubstituteProduct.objects.filter(barcode=1234567891011)

        # Test if he subsistute obect his created
        self.assertQuerysetEqual(test_query_substitute, ['<SubstituteProduct: gerblé2>'])

    def test_add_favorite_database(self):
        '''
        Test if the product are added as favorite in database.
        '''

        # We call the function to add a favorite in database with the substitute product and the user in parameter
        DatabaseManagerClass.add_favorite_database(self, self.product_substitute.barcode, self.user_test)

        # Test i we have all datas in the favorite database and if it's match with the substitute define
        self.assertQuerysetEqual(Favorite.objects.filter(barcode=12345678910), ['<Favorite: gerblé>'])
        self.assertEqual(Favorite.objects.get(barcode=12345678910).user_associate.username, 'testuser')
        self.assertEqual(Favorite.objects.get(barcode=12345678910).product_name, 'gerblé')
