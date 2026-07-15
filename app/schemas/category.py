"""Pydantic schemas for category resources."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class CategoryBase(BaseModel):
    name: str = Field(max_length=255)
    slug: str = Field(max_length=255)
    description: str | None = None


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id: uuid.UUID
    created_at: datetime

    model_config = {"from_attributes": True}
