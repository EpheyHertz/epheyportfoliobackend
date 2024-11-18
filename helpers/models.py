from pydantic import BaseModel, Field
from typing import List, Optional

# Project model
class Project(BaseModel):
    title: str
    description: str
    technologies: List[str] = Field(default_factory=list)
    image: Optional[str] = None  # URL to the image
    link: Optional[str] = None  # GitHub link
    demolink: Optional[str] = None  # Live demo link
    created_at: Optional[str] = None  # You can use datetime if needed

class ProjectResponse(BaseModel):
    id: str
    title: str
    description: str
    technologies: List[str] = Field(default_factory=list)
    image: Optional[str] = None  # URL to the image
    link: Optional[str] = None  # GitHub link
    demolink: Optional[str] = None  # Live demo link
    created_at: Optional[str] = None  # Can be a datetime field if needed
    
    class Config:
        from_attributes = True
        populate_by_name = True  
# Skill model
class Skill(BaseModel):
    name: str
    category: str
    proficiency: int = Field(ge=0, le=100)  # Rate skill from 1-100

class SkillResponse(BaseModel):
    id: str 
    name: str
    category: str
    proficiency: int = Field(ge=0, le=100)  # Rate skill from 0-100
    
    class Config:
        from_attributes = True
        populate_by_name = True  

# Education model
class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: str
    start_year: str  # You can use datetime if needed
    end_year: Optional[str] = None  # Can be null if ongoing

class EducationResponse(BaseModel):
    id: str
    institution: str
    degree: str
    field_of_study: str
    start_year: str  # Can be a datetime if needed
    end_year: Optional[str] = None  # Can be null if ongoing
    
    class Config:
        from_attributes = True
        populate_by_name = True   
# Review model
class Review(BaseModel):
    name: str
    role: str
    review: str
    company: Optional[str] = None
    photo_url: Optional[str] = None  # URL to the photo

class ReviewResponse(BaseModel):
    id: str 
    name: str
    role: str
    review: str
    company: Optional[str] = None
    photo_url: Optional[str] = None  # URL to the photo
    
    class Config:
        from_attributes = True
        populate_by_name = True

class DeleteResponse(BaseModel):
    message: str  

