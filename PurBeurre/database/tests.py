from django.test import TestCase
from database.models import Product, Category
from django.urls import reverse

class ProductTestCase(TestCase):
    '''
    Test for products in database
    '''
    def setUp(self):
        Product.objects.create(name="Nutella", salt=1.4, sugar=1.3, fat=1.2, barcode=1000000)

    def test_good_values(self):
        product = Product.objects.get(id=1)
        expected_object_name = f'{product.name}'
        self.assertEquals(expected_object_name, 'Nutella')

    # def test_post_list_values(self):
    #     response = self.client.get(reverse('search_and_stock'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'Nutella')
    #     self.assertTemplateUsed(response, 'standard/product.html')
