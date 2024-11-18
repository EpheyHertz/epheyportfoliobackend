from fastapi import APIRouter, HTTPException
from database import db
from helpers.models import Project, Skill, Education, Review,DeleteResponse
from bson import ObjectId  # Import ObjectId for MongoDB

router = APIRouter()

# Delete a project by ID
@router.delete("/projects/{project_id}")
async def delete_project(project_id: str):  # Use string as Mongo's _id is a string
    try:
        result = await db.projects.delete_one({"_id": ObjectId(project_id)})  # Use ObjectId
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Project not found")
        
        return {"message": f"Project with ID {project_id} has been deleted"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting project: {str(e)}")

# Delete a skill by ID
@router.delete("/skills/{skill_id}")
async def delete_skill(skill_id: str):  # Use string as Mongo's _id is a string
    try:
        result = await db.skills.delete_one({"_id": ObjectId(skill_id)})  # Use ObjectId
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Skill not found")
        
        return {"message": f"Skill with ID {skill_id} has been deleted"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting skill: {str(e)}")

# Delete an education entry by ID
@router.delete("/education/{education_id}")
async def delete_education(education_id: str):  # Use string as Mongo's _id is a string
    try:
        result = await db.education.delete_one({"_id": ObjectId(education_id)})  # Use ObjectId
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Education entry not found")
        
        return {"message": f"Education entry with ID {education_id} has been deleted"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting education entry: {str(e)}")

# Delete a review by ID
@router.delete("/reviews/{review_id}")
async def delete_review(review_id: str):  # Use string as Mongo's _id is a string
    try:
        result = await db.reviews.delete_one({"_id": ObjectId(review_id)})  # Use ObjectId
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Review not found")
        
        return {"message": f"Review with ID {review_id} has been deleted"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting review: {str(e)}")
