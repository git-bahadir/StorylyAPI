from datetime import datetime
import json

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware

from stories.models import Story, Metadata, App

class Command(BaseCommand):
    help = 'Create sample stories from JSON files.'

    def handle(self, *args, **kwargs):
        with open(settings.BASE_DIR / 'stories' / 'data' / 'sample_stories.json') as f:
            data = json.load(f)

        for story_obj in data:
            metadata_objs = story_obj.pop('metadata')
            app_id = story_obj.pop('app_id')

            app = App(id=app_id)
            app.save()

            story = Story(
                app=app,
                ts=make_aware(datetime.fromtimestamp(story_obj['ts'])),
            )
            story.save()

            for metadata_obj in metadata_objs:
                metadata = Metadata(**metadata_obj, story_id=story.id)
                metadata.save()
            