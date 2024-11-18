from fastapi import APIRouter, HTTPException
from app.database import db
from app.models import Project, Skill, Education, Review
from uuid import UUID
from bson import Binary

router = APIRouter()

# Helper function to convert string to UUID
def convert_str_to_uuid(str_id: str) -> UUID:
    try:
        return UUID(str_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format")

# Delete a project by UUID
@router.delete("/projects/{project_id}", response_model=Project)
async def delete_project(project_id: str):
    project_uuid = convert_str_to_uuid(project_id)
    result = db.projects.delete_one({"id": project_uuid})  # Assuming UUID is stored in the 'id' field
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {"message": f"Project with ID {project_id} has been deleted"}

# Delete a skill by UUID
@router.delete("/skills/{skill_id}", response_model=Skill)
async def delete_skill(skill_id: str):
    skill_uuid = convert_str_to_uuid(skill_id)
    result = db.skills.delete_one({"id": skill_uuid})  # Assuming UUID is stored in the 'id' field
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    return {"message": f"Skill with ID {skill_id} has been deleted"}

# Delete an education entry by UUID
@router.delete("/education/{education_id}", response_model=Education)
async def delete_education(education_id: str):
    education_uuid = convert_str_to_uuid(education_id)
    result = db.education.delete_one({"id": education_uuid})  # Assuming UUID is stored in the 'id' field
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Education entry not found")
    
    return {"message": f"Education entry with ID {education_id} has been deleted"}

# Delete a review by UUID
@router.delete("/reviews/{review_id}", response_model=Review)
async def delete_review(review_id: str):
    review_uuid = convert_str_to_uuid(review_id)
    result = db.reviews.delete_one({"id": review_uuid})  # Assuming UUID is stored in the 'id' field
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Review not found")
    
    return {"message": f"Review with ID {review_id} has been deleted"}
