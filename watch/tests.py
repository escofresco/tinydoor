from django.test import Client, TestCase
from django.test.client import RequestFactory
from watch.views import HomeView


class HomeViewTests(TestCase):
    def setUp(self):
        """
        Initializes objects and variables which may
        be needed for multiple tests in this class.
        """
        self.client = Client()
        self.factory = RequestFactory()

    def test_true_is_true(self):
        '''Canary test to make sure environment is working correctly.'''
        self.assertEqual(True, True)

    def test_get_home_view(self):
        """
        User is able to access the home page and
        get a HTTP 200 response
        """
        request = self.factory.get('home')
        response = HomeView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_upload_file(self):
        """
        User is able to upload a file to the view,
        and is redirected (receives a HTTP 302).
        """


class WatchedViewTests(TestCase):
    def setUp(self):
        """
        Initializes objects and variables
        needed for every test in this class.
        """
        self.client = Client()
        self.factory = RequestFactory()
