from typing import List, Optional
from ninja import NinjaAPI
from stories.models import Story
from stories.schema import StorySchema, NotFoundSchema
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
 
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

api = NinjaAPI()

@api.get("/{app_token}", response={200: StorySchema, 404: NotFoundSchema})
def get_stories(request, app_token: str):
    try:
        story = Story.objects.get(id=app_token)
        print(type(story.ts))
        story.ts = story.ts.timestamp()
        return 200, story
    except Story.DoesNotExist:
        return 404, {'message': 'Story not found'}



@api.get("/cached/{app_token}", response={200: StorySchema, 404: NotFoundSchema})
def cached_sample(request, app_token: str):
    cached_story = cache.get(app_token)
    if cached_story:
        return 200, cached_story

    try:
        story = Story.objects.get(id=app_token)
        print(type(story.ts))
        story.ts = story.ts.timestamp()
        cache.set(app_token, story, CACHE_TTL)
        return 200, story
    except Story.DoesNotExist:
        return 404, {'message': 'Story not found'}