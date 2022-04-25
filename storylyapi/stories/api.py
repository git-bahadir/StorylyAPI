from typing import List, Optional
from ninja import NinjaAPI
from stories.models import Story, Event
from stories.schema import StorySchema, EventSchemaIn, EventSchemaOut, NotFoundSchema
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from django.db.models import Count, F, Value
 
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

api = NinjaAPI()

@api.get("stories/{app_token}", response={200: StorySchema, 404: NotFoundSchema})
def get_stories(request, app_token: str):
    try:
        story = Story.objects.get(id=app_token)
        print(type(story.ts))
        story.ts = story.ts.timestamp()
        return 200, story
    except Story.DoesNotExist:
        return 404, {'message': 'Story not found'}



@api.get("stories/cached/{app_token}", response={200: StorySchema, 404: NotFoundSchema})
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



@api.post("event/{app_token}", response={201: EventSchemaOut})
def create_event(request, app_token: str, event: EventSchemaIn):
    filtered_events = Event.objects.filter(
        app=app_token,
        event_type=event.event_type,
        story=event.story
    )

    if not filtered_events:
        created_event = Event(
            event_type=event.event_type,
            user_id=event.user_id,
            story_id=event.story,
            app_id=app_token,
            count=1
        )

        created_event.save()

        return 201, created_event

    else:
        filtered_events.update(count=F('count') + 1)
        return 201, Event.objects.get(id=filtered_events.first().id)



"""
sadece filterla sonra sumı arttır


aggregate ederken story_idden bağlı olan app_idsini çek sonra countu koy dbye sadece
date e göre zaten dbde dateli tutuyor

o dau kısmı için kafka streams lazım
"""