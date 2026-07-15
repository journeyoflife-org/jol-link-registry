"""Pydantic schemas for link resources."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl


class LinkBase(BaseModel):
    url: HttpUrl
    title: str = Field(max_length=512)
    description: str | None = None
    country_code: str = Field(min_length=2, max_length=2)
    category_id: uuid.UUID


class LinkCreate(LinkBase):
    pass


class LinkUpdate(BaseModel):
    url: HttpUrl | None = None
    title: str | None = Field(default=None, max_length=512)
    description: str | None = None
    country_code: str | None = Field(default=None, min_length=2, max_length=2)
    category_id: uuid.UUID | None = None
    is_active: bool | None = None


class LinkRead(LinkBase):
    id: uuid.UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_checked_at: datetime | None = None

    model_config = {"from_attributes": True}
