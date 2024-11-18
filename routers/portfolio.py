import logging
from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from database import db
from helpers.models import Project, Skill, Education, Review, ProjectResponse,SkillResponse,EducationResponse,ReviewResponse
from bson import Binary, ObjectId
from typing import List, Optional
from helpers.upload import upload_image  # Ensure this is synchronous or refactor as async if needed

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Helper function to generate a new incrementing ID
async def get_next_id(collection_name: str) -> int:
    counter = await db.counters.find_one_and_update(
        {"_id": collection_name},
        {"$inc": {"sequence_value": 1}},
        upsert=True,
        return_document=True
    )
    return counter["sequence_value"]

# Create a new project with image upload
@router.post("/projects/", response_model=Project)
async def create_project(
    title: str,
    description: str,
    technologies: List[str],
    link: str,
    demolink: str,
    image: UploadFile = File(...),
):
    try:
        # Upload the image
        logging.info(f"Uploading image for project: {title}")
        image_url = upload_image(image)  # Ensure this is synchronous

        # Create a project instance (no id needed, database will handle it)
        project = Project(
            title=title,
            description=description,
            technologies=technologies,
            image=image_url,
            link=link,
            demolink=demolink,
        )
        project_dict = project.model_dump()

        # Insert into the database
        logging.info("Inserting project into the database.")
        await db.projects.insert_one(project_dict)
        logging.info(f"Project inserted.")

        return project_dict
    except Exception as e:
        logging.error(f"Error creating project: {e}")
        raise HTTPException(status_code=500, detail="Failed to create project.")

# Get all projects
@router.get("/projects/", response_model=List[ProjectResponse])
async def get_projects():
    try:
        logging.info("Fetching all projects.")
        projects = []
        
        async for project in db.projects.find():
            # Manually convert the _id to a string and include it as 'id'
            project["id"] = str(project["_id"])  # Convert ObjectId to string
            project_response = ProjectResponse(**project)  # Pass the updated project dict
            projects.append(project_response)
        
        return projects
    except Exception as e:
        logging.error(f"Error fetching projects: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch projects.")

# Create a new skill
@router.post("/skills/", response_model=Skill)
async def create_skill(
    name: str = Form(...),
    category: str = Form(...),
    proficiency: int = Form(..., ge=0, le=100),
):
    try:
        # Create a skill instance (no id needed, database will handle it)
        skill = Skill(
            name=name,
            category=category,
            proficiency=proficiency,
        )
        skill_dict = skill.model_dump()

        logging.info(f"Inserting skill: {name}")
        await db.skills.insert_one(skill_dict)
        logging.info(f"Skill inserted.")

        return skill_dict
    except Exception as e:
        logging.error(f"Error creating skill: {e}")
        raise HTTPException(status_code=500, detail="Failed to create skill.")

# Get all skills
@router.get("/skills/", response_model=List[SkillResponse])
async def get_skills():
    try:
        logging.info("Fetching all skills.")
        skills = []
        
        async for skill in db.skills.find():
            # Manually convert the _id to a string and include it as 'id'
            skill["id"] = str(skill["_id"])  # Convert ObjectId to string
            skill_response = SkillResponse(**skill)  # Pass the updated skill dict
            skills.append(skill_response)
        
        return skills
    except Exception as e:
        logging.error(f"Error fetching skills: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch skills.")
    

# Create a new education entry
@router.post("/education/", response_model=Education)
async def create_education(
    institution: str = Form(...),
    degree: str = Form(...),
    field_of_study: str = Form(...),
    start_year: str = Form(...),
    end_year: Optional[str] = Form(None),
):
    try:
        education = Education(
            institution=institution,
            degree=degree,
            field_of_study=field_of_study,
            start_year=start_year,
            end_year=end_year,
        )
        education_dict = education.model_dump()

        logging.info(f"Inserting education entry for {institution}")
        await db.education.insert_one(education_dict)
        logging.info(f"Education entry inserted.")

        return education_dict
    except Exception as e:
        logging.error(f"Error creating education entry: {e}")
        raise HTTPException(status_code=500, detail="Failed to create education entry.")

# Get all education entries
@router.get("/education/", response_model=List[EducationResponse])
async def get_education():
    try:
        logging.info("Fetching all education entries.")
        education_entries = []
        
        async for education in db.education.find():
            # Manually convert the _id to a string and include it as 'id'
            education["id"] = str(education["_id"])  # Convert ObjectId to string
            education_response = EducationResponse(**education)  # Pass the updated education dict
            education_entries.append(education_response)
        
        return education_entries
    except Exception as e:
        logging.error(f"Error fetching education entries: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch education entries.")

# Create a new review
@router.post("/reviews/", response_model=Review)
async def create_review(
    name: str = Form(...),
    role: str = Form(...),
    review: str = Form(...),
    company: str = Form(...),
    photo: UploadFile = File(...),
):
    try:
        logging.info(f"Uploading photo for review by {name}")
        photo_url = upload_image(photo)  # Ensure this is synchronous
        photo_url = str(photo_url)  # Convert to string if necessary

        logging.info(f"Creating review for {name}")
        # Create review dictionary (no id needed, database will handle it)
        review_dict = {
            "name": name,
            "role": role,
            "review": review,
            "company": company,
            "photo_url": photo_url,
        }

        # Insert into the database
        logging.info("Inserting review into the database.")
        result = await db.reviews.insert_one(review_dict)
        logging.info(f"Review inserted.")

        # Add the database-generated ID to the response (MongoDB assigns _id)
        review_dict["id"] = str(result.inserted_id)
        return review_dict
    except Exception as e:
        logging.error(f"Error creating review: {e}")
        raise HTTPException(status_code=500, detail="Failed to create review.")

# Get all reviews
@router.get("/reviews/", response_model=List[ReviewResponse])
async def get_reviews():
    try:
        logging.info("Fetching all reviews.")
        reviews = []
        
        async for review in db.reviews.find():
            # Manually convert the _id to a string and include it as 'id'
            review["id"] = str(review["_id"])  # Convert ObjectId to string
            review_response = ReviewResponse(**review)  # Pass the updated review dict
            reviews.append(review_response)
        
        return reviews
    except Exception as e:
        logging.error(f"Error fetching reviews: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch reviews.")
