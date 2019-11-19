from django.test import TestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.contrib.auth.forms import UserCreationForm
from inspect import currentframe, getframeinfo
from django.contrib.auth import login, authenticate
from django.test.client import RequestFactory

FRAMEINFO = getframeinfo(currentframe())

class bcolors:
    '''
    Class to colorize test in terminal. OKGREEN for success and WARNING for fail.
    Here is two exemples :
    SUCCESS :
    print(bcolors.OKGREEN,"This test is a success :) ",bcolors.ENDC)

    FAIL :
    print(bcolors.WARING,"This test is a fail :( ",bcolors.ENDC)
    '''
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'

class TestBasicViews(TestCase):

    def test_home_page_status_code(self):
        '''
        Check if the returned status code of the page is 200
        '''
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

    def test_view_url_by_name(self):
        '''
        Check if the url returned is good
        '''
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
    
    def test_view_uses_correct_template(self):
        '''
        Test if we use the correct template and it returns a 200 status_code
        '''
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'standard/index.html')
        
    def test_home_page_contains_correct_html(self):
        '''
        Test if the html page contains the h1 title (only present in the index page)
        '''
        response = self.client.get('/')
        self.assertContains(response, '<h1 class="text-uppercase text-white font-weight-bold">Du gras oui, mais de qualité !</h1>')

    def test_home_page_does_not_contain_incorrect_html(self):
        '''
        Test if the page doesn't contain bad html
        '''
        response = self.client.get('/')
        self.assertNotContains(response, 'That\'s incorrect html')
