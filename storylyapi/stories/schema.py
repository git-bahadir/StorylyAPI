from datetime import date, datetime, time
from typing import List
from ninja import Schema, ModelSchema, Field
from stories.models import Story, App, Metadata
from ninja.orm import create_schema
from pydantic import BaseModel

AppSchema = create_schema(App)

#MetdataSchema = create_schema(Metadata)

#StorySchema = create_schema(Story)


class MetadataSchema(ModelSchema):
    class Config:
        model = Metadata
        model_fields = ["id", "metadata"]

class StorySchema(Schema):
    metadata: List[MetadataSchema]
    app_id: int = Field(alias="app.id")
    ts: int


class NotFoundSchema(Schema):
    message: str