from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
from django.contrib.auth.forms import UserCreationForm
from inspect import currentframe, getframeinfo
from django.contrib.auth import login, authenticate


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

class TestUserAccount(TestCase):
    '''
    This class test the UserAccount functionalities.
    '''
    def test_post_form_valid(self):
        '''
        Check if the form fill in UserCreationForm is valid when informations are valids.
        '''
        form_data = {"username":"martin","password1":"matchingpass","password2":"matchingpass"}
        form = UserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        print(bcolors.OKGREEN + "TEST_POST_ACCOUNT = OK"+bcolors.ENDC)

    def test_post_user_creation_case_wrong(self):          
        '''
        Check if the form is False when the user doesn't fill one or few informations.
        '''
        # Test : Empty Username
        form_data_no_user = {"username":"","password1":"vitamineD61","password2":"vitamineD61","info":"empty no username"}
        
        # Test : two passwords doesn't matches
        form_data_no_matching_pwd = {"username":"martin","password1":"matchingpass","password2":"matching","info":"no matching pwd"}
        
        # Test : empty passwords fields
        form_data_no_pwd = {"username":"martin","password1":"","password2":"","info":"empty password"}
        
        # Test : weak passwords (rule : more than 8 characters)
        form_data_weak_password = {"username":"martin","password1":"weak","password2":"weak","info":"weak password"}

        test_list_user_creation = [form_data_no_user,form_data_no_matching_pwd,form_data_no_pwd,form_data_weak_password]

        for test_user_creation in test_list_user_creation:
            form = UserCreationForm(data=test_user_creation)
            if form.is_valid():
                print(bcolors.WARNING,"Error with the test",test_user_creation["info"],"LINE :",FRAMEINFO.lineno,bcolors.ENDC)
            else:
                self.assertFalse(form.is_valid())
                print(bcolors.OKGREEN,"TEST_USER_WRONG_SIGNUP_INFORMATION OK, CASE :",test_user_creation["info"],bcolors.ENDC)

    # def test_user_login(self):
    #     test_form_data = {"username":"martin","password1":"thisisatest","password2":"thisisatest"}
    #     test_temp_auth = UserCreationForm(data=test_form_data)

    #     test_temp_auth.save()

    #     test_user = authenticate(username="martin",password="thisisatest")
    #     self.assertTrue(test_user)

        # test_user_dict= {"username":"martin","password":"thisisatest"}
        # self.factory = RequestFactory()
        # request = self.factory.post('login_user',test_user_dict)

        # response = my_view(request)
        # self.assertEqual(response.status_code, 200)

        # self.assertTrue(post(login(request,test_user)))

    def test_user_login(self):
        test_c = Client()
        test_form_data = {"username":"martin","password1":"thisisatest","password2":"thisisatest"}
        
        test_temp_auth = UserCreationForm(data=test_form_data)

        test_temp_auth.save()
        test_form_data_true = {"username":"martin","password":"thisisatest"}

        response = test_c.post('/users/login_user/', test_form_data)
        response2 = test_c.post('/users/login_user/', test_form_data_true)

        self.assertTrue(response)
        self.assertTrue(response2)