from fastapi import APIRouter, HTTPException
from app.database import db
from app.models import Project, Skill, Education, Review
from bson import ObjectId

router = APIRouter()

# Helper function to convert string to ObjectId
def convert_str_to_objectid(str_id: str) -> ObjectId:
    try:
        return ObjectId(str_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid ID format")

# Delete a project by ID
@router.delete("/projects/{project_id}", response_model=Project)
async def delete_project(project_id: str):
    project_object_id = convert_str_to_objectid(project_id)
    result = db.projects.delete_one({"_id": project_object_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {"message": f"Project with ID {project_id} has been deleted"}

# Delete a skill by ID
@router.delete("/skills/{skill_id}", response_model=Skill)
async def delete_skill(skill_id: str):
    skill_object_id = convert_str_to_objectid(skill_id)
    result = db.skills.delete_one({"_id": skill_object_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    return {"message": f"Skill with ID {skill_id} has been deleted"}

# Delete an education entry by ID
@router.delete("/education/{education_id}", response_model=Education)
async def delete_education(education_id: str):
    education_object_id = convert_str_to_objectid(education_id)
    result = db.education.delete_one({"_id": education_object_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Education entry not found")
    
    return {"message": f"Education entry with ID {education_id} has been deleted"}

# Delete a review by ID
@router.delete("/reviews/{review_id}", response_model=Review)
async def delete_review(review_id: str):
    review_object_id = convert_str_to_objectid(review_id)
    result = db.reviews.delete_one({"_id": review_object_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Review not found")
    
    return {"message": f"Review with ID {review_id} has been deleted"}
