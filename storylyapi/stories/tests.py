from django.test import Client
import unittest

class TestStories(unittest.TestCase):
    def setUp(self):
        self.client = Client()

        #setup database response
        # https://docs.djangoproject.com/en/4.0/topics/testing/overview/

    def test_get_stories(self):
        response = self.client.get('/stories/1')
        self.assertEqual(response.status_code, 200)

    def test_get_stories_not_found(self):
        response = self.client.get('/stories/2')
        self.assertEqual(response.status_code, 404)

    def test_get_stories_cached(self):
        response = self.client.get('/stories/cached/1')
        self.assertEqual(response.status_code, 200)

    def test_get_stories_cached_not_found(self):
        response = self.client.get('/stories/cached/2')
        self.assertEqual(response.status_code, 404)

    def test_create_event(self):
        response = self.client.post('/event/1', {'event_type': 'test', 'story': '1'})
        self.assertEqual(response.status_code, 201)

    def test_create_event_not_found(self):
        response = self.client.post('/event/2', {'event_type': 'test', 'story': '1'})
        self.assertEqual(response.status_code, 404)

    def test_create_event_not_found_story(self):
        response = self.client.post('/event/1', {'event_type': 'test', 'story': '2'})
        self.assertEqual(response.status_code, 404)

    def test_create_event_not_found_event_type(self):
        response = self.client.post('/event/1', {'event_type': 'test2', 'story': '1'})
        self.assertEqual(response.status_code, 404)

    #def test_create_event_not_found_event_type_story(self):
    #    response = self.client.post('/event/



# test for create event
#https://www.youtube.com/watch?v=IKnp2ckuhzg

#test models 
    
#https://www.youtube.com/watch?v=zUl-Tf-UEzw schema test



"""
@lgabs you can make use of unittest
For example:

# Create your tests here.
import unittest
from django.test import Client

class MyUnitTest(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.client = Client()

    def test_product_health(self):
        # Issue a GET request.
        response = self.client.get('/api/v1/products/ping')
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        # Check that the rendered json contains valid data.
        self.assertEqual(response.json().get('data'), 'Healthy')

$ ./manage.py test APP_NAME

Since it's under Django so you can also leverage Django default unit test.

from django.test import TestCase
class MyUnitTest(TestCase):
    pass

"""


#unittest apis


#RenewBookForm schema testi https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Testing


#make request https://www.rootstrap.com/blog/testing-in-django-django-rest-basics-useful-tools-good-practices/ orta sonlar
