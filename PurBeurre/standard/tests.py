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

    def test_index(self):
        '''
            Test if the http response for index is fine (code 200).
        '''
        response = self.client.get(reverse('index'))

        if response:
            self.assertEqual(response.status_code, 200)
            print(bcolors.OKGREEN + "TEST_BASIC_VIEW_INDEX = OK",bcolors.ENDC)
        else:
            print(bcolors.WARNING + "TEST_BASIC_VIEW_INDEX = FAIL  LINE = ",FRAMEINFO.lineno,bcolors.ENDC)

        try:
            self.client.get(reverse('indexNoReverseMatchError'))
        except NoReverseMatch:
            print(bcolors.OKGREEN + "TEST_BASIC_VIEW_REVERSE_INDEX = OK",bcolors.ENDC)
        

    # def test_favorite(self):
    #     '''
    #         Test if the http response for favorite page is fine (code 200).
    #     '''

    #     if self.client.get(reverse('favorite')):
    #         self.assertEqual(self.client.get(reverse('favorite')).status_code, 200)
    #         print(bcolors.OKGREEN + "TEST_FAVORITE = OK" + bcolors.ENDC)

    #     else:
    #         print(bcolors.WARNING + "TEST_FAVORITE = FAIL",FRAMEINFO.lineno,bcolors.ENDC)

    #     try:
    #         self.client.get(reverse('favoriteNoReverseMatchError'))
    #     except NoReverseMatch:
    #         print(bcolors.OKGREEN + "TEST_FAVORITE = OK" + bcolors.ENDC)
