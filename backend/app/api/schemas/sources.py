from pydantic import BaseModel, HttpUrl, Field
from datetime import datetime
from typing import Any, Literal, Union

# --------------------------
# Source Types
# --------------------------
class BaseSourceConfig(BaseModel):
    type: str

class WebSourceConfig(BaseSourceConfig):
    type: Literal["web"]
    start_url: HttpUrl
    allowed_domains: list[str] = Field(default_factory=list)
    max_depth: int = Field(default=2, ge=0)

class GitSourceConfig(BaseSourceConfig):
    type: Literal["git"]
    repo_url: HttpUrl
    branch: str = "main"
    auth_token: str | None = None

class S3SourceConfig(BaseSourceConfig):
    type: Literal["s3"]
    bucket: str
    prefix: str | None = None
    region: str | None = None


SourceConfig = Union[
    WebSourceConfig,
    GitSourceConfig,
    S3SourceConfig,
    # DriveSourceConfig,
]

# --------------------------
# Route Schemas
# --------------------------

class SourceSchema(BaseModel):
    """The source registered"""
    id: int
    type: str
    name: str | None
    config: SourceConfig
    created_at: datetime

    class Config:
        from_attributes = True

class SourceCreateSchema(BaseModel):
    """The new source schema"""
    name: str | None = None
    config: SourceConfig

class SourceUpdateSchema(BaseModel):
    """The source being updated"""
    name: str | None = None
    config: dict[str, Any] | None = None
