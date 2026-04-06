from pydantic import BaseModel
from typing import Optional, List


class CommunityCreate(BaseModel):
    category: str
    title: str
    content: str
    images: Optional[List[str]] = []


class CommunityUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    images: Optional[List[str]] = None
