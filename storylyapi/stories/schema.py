from typing import List
from ninja import Schema, ModelSchema, Field
from stories.models import App, Metadata
from ninja.orm import create_schema

AppSchema = create_schema(App)

class MetadataSchema(ModelSchema):
    class Config:
        model = Metadata
        model_fields = ["id", "metadata"]

class StorySchema(Schema):
    metadata: List[MetadataSchema]
    app_id: int = Field(alias="app.id")
    ts: int

class EventSchemaIn(Schema):
    event_type: str
    story: int = Field(alias="story_id")
    user_id: int

class EventSchemaOut(Schema):
    event_type: str
    story: int = Field(alias="story_id")
    user_id: int

class NotFoundSchema(Schema):
    message: str