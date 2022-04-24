from typing import List, Optional
from ninja import NinjaAPI
from stories.models import Story
from stories.schema import StorySchema, NotFoundSchema

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


