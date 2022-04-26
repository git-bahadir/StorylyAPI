import json
from django.test import TestCase, Client
from .models import Story, App, Metadata, Event
from datetime import datetime

class TestStories(TestCase):
    def setUp(self):
        Metadata.objects.create(metadata="{'test': 'test'}", story_id=1)
        App.objects.create(id=1)
        Story.objects.create(app_id=1, ts=datetime(2020,4,19,12,0,0))

        Event.objects.create(
            event_type='test',
            story_id=1,
            app_id=1,
            count=1,
            date=datetime.today()
        )
        self.client = Client()

    def test_get_stories(self):
        response = self.client.get('/api/v1/stories/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()
            .get('metadata'), [{'id': 1, 'metadata': "{'test': 'test'}"}])
        self.assertEqual(response.json()
            .get('ts'), 1587297600)


    def test_get_stories_not_found(self):
        response = self.client.get('/api/v1/stories/2')
        self.assertEqual(response.status_code, 404)

    def test_get_stories_cached(self):
        response = self.client.get('/api/v1/stories/cached/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()
            .get('metadata'), [{'id': 1, 'metadata': "{'test': 'test'}"}])
        self.assertEqual(response.json()
            .get('ts'), 1587297600)

    def test_get_stories_cached_not_found(self):
        response = self.client.get('/api/v1/stories/cached/2')
        self.assertEqual(response.status_code, 404)

    def test_create_event(self):
        response = self.client.post('/api/v1/event/1', data=json.dumps({
            "event_type":'test',
            "user_id":1,
            "story_id":1,
        }), content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()
            .get('event_type'), 'test')
        self.assertEqual(response.json()
            .get('story'), 1)
        self.assertEqual(response.json()
            .get('count'), 2)
        self.assertEqual(response.json()
            .get('date'), datetime.today().strftime('%Y-%m-%d'))


    def test_create_event_not_found_story(self):
        response = self.client.post('/event/2', data=json.dumps({
            "event_type":'test',
            "user_id":1,
            "story_id":1,
        }), content_type="application/json")

        self.assertEqual(response.status_code, 404)
    