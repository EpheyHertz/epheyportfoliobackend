from fastapi import APIRouter, HTTPException
from database import db
from helpers.models import Project, Skill, Education, Review
from uuid import UUID
from bson import Binary

router = APIRouter()

# Helper function to convert string to UUID
def convert_str_to_uuid(str_id: str) -> UUID:
    try:
        return UUID(str_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
def convert_uuid_to_bson(uuid_obj: UUID) -> Binary:
    return Binary.from_uuid(uuid_obj)


# Delete a project by UUID
@router.delete("/projects/{project_id}", response_model=Project)
async def delete_project(project_id: UUID):
   
    result = await db.projects.delete_one({"id": convert_uuid_to_bson(project_id)})  # Assuming UUID is stored in the 'id' field
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {"message": f"Project with ID {project_id} has been deleted"}

# Delete a skill by UUID
@router.delete("/skills/{skill_id}", response_model=Skill)
async def delete_skill(skill_id: str):
    skill_uuid = convert_str_to_uuid(skill_id)
    result = await db.skills.delete_one({"id": convert_uuid_to_bson(skill_uuid)})  # Assuming UUID is stored in the 'id' field
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    return {"message": f"Skill with ID {skill_id} has been deleted"}

# Delete an education entry by UUID
@router.delete("/education/{education_id}", response_model=Education)
async def delete_education(education_id: str):
    education_uuid = convert_str_to_uuid(education_id)
    result = await db.education.delete_one({"id": convert_uuid_to_bson(education_uuid)})  # Assuming UUID is stored in the 'id' field
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Education entry not found")
    
    return {"message": f"Education entry with ID {education_id} has been deleted"}

# Delete a review by UUID
@router.delete("/reviews/{review_id}", response_model=Review)
async def delete_review(review_id: str):
    
    result = await db.reviews.delete_one({"id":convert_uuid_to_bson(review_id)})  # Assuming UUID is stored in the 'id' field
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Review not found")
    
    return {"message": f"Review with ID {review_id} has been deleted"}
