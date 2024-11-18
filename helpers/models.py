from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID, uuid4
from database import db




# Project model
class Project(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    title: str
    description: str
    technologies: List[str] = Field(default_factory=list)
    image: Optional[str] = None  # URL to the image
    link: Optional[str] = None  # GitHub link
    demolink: Optional[ str] = None  # Live demo link
    created_at: Optional[str] = None  # You can use datetime if needed

# Skill model
class Skill(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    name: str
    category: str
    proficiency: int = Field(ge=0, le=100)  # Rate skill from 1-100

# Education model
class Education(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    institution: str
    degree: str
    field_of_study: str
    start_year: str  # You can use datetime if needed
    end_year: Optional[str] = None  # Can be null if ongoing

# Review model
class Review(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    name: str
    role: str
    text: str
    company: Optional[str]=None
    photo_url: Optional[ str] = None  # URL to the photo

