from pydantic import BaseModel, Field
from datetime import datetime

class Site(BaseModel):
    """The site registered"""
    id: int = Field(...)
    url: str = Field(...)
    name: str = Field(...)
    start_url: str = Field(...)
    allowed_domains: list[str]
    max_depth: int
    created_at: datetime = Field(...)

class SiteCreate(BaseModel):
    """A site being registered"""
    name: str = Field(...)
    url: str = Field(...)

class SiteUpdate(BaseModel):
    """The site being updated"""
    id: int = Field(...)
    url: str = Field(...)

