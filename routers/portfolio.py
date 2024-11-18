from fastapi import APIRouter, HTTPException, File, UploadFile,Form
from database import db
from helpers.models import Project, Skill, Education, Review
from bson import Binary, ObjectId
from typing import List, Optional
from uuid import uuid4, UUID
import uuid
from helpers.upload import upload_image  # Ensure this function is async if it involves I/O

router = APIRouter()

# Helper function to convert UUID to BSON Binary
def convert_uuid_to_bson(uuid_obj: UUID) -> Binary:
    return Binary.from_uuid(uuid_obj)

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
    # Upload the image and get the URL
    image_url = upload_image(image)  # Call the upload_image function without await if it's synchronous
    
    # Create a project instance
    project = Project(
        title=title,
        description=description,
        technologies=technologies,
        image=image_url,
        id=uuid4(),
        link=link,
        demolink=demolink,
    )
    
    # Convert the project instance to a dictionary
    project_dict = project.model_dump()
    project_dict["_id"] = convert_uuid_to_bson(project.id)  # Convert UUID to BSON Binary
    
    # Insert the project into the database
    result = db.projects.insert_one(project_dict)
    
    # Add the inserted ID to the project dictionary
    project_dict["id"] = str(project.id)  # Keep the UUID as a string for responses
    
    # Return the project dictionary
    return project_dict


@router.get("/projects/", response_model=List[Project])
async def get_projects():
    projects = []
    async for project in db.projects.find():
        project["id"] = str(project["_id"].as_uuid())  # Convert BSON Binary back to UUID
        projects.append(project)
    return projects

# Create a new skill
@router.post("/skills/", response_model=Skill)
async def create_skill(
    name: str = Form(...),  # Input field for name
    category: str = Form(...),  # Input field for category
    proficiency: int = Form(..., ge=0, le=100),  # Input field for proficiency, with validation
):
    # Create a skill instance with the received form data
    skill = Skill(
        name=name,
        category=category,
        proficiency=proficiency,
        id=uuid4(),  # Generate a new UUID
    )
    
    # Convert the skill instance to a dictionary
    skill_dict = skill.model_dump()
    skill_dict["_id"] = convert_uuid_to_bson(skill.id)  # Convert UUID to BSON Binary
    
    # Insert the skill into the database
    result = db.skills.insert_one(skill_dict)
    
    # Add the inserted ID to the skill dictionary (UUID as a string for responses)
    skill_dict["id"] = str(skill.id)
    
    # Return the skill dictionary with the inserted ID
    return skill_dict
# Get all skills
@router.get("/skills/", response_model=List[Skill])
async def get_skills():
    skills = []
    async for skill in db.skills.find():
        skill["id"] = str(skill["_id"].as_uuid())  # Convert BSON Binary back to UUID
        skills.append(skill)
    return skills

# Create a new education entry
@router.post("/education/", response_model=Education)
async def create_education(
    institution: str = Form(...),  # Input field for institution name
    degree: str = Form(...),  # Input field for degree name
    field_of_study: str = Form(...),  # Input field for field of study
    start_year: str = Form(...),  # Input field for start year
    end_year: Optional[str] = Form(None),  # Input field for end year (optional)
):
    # Create an education instance with the received form data
    education = Education(
        institution=institution,
        degree=degree,
        field_of_study=field_of_study,
        start_year=start_year,
        end_year=end_year,
        id=uuid4(),  # Generate a new UUID
    )
    
    # Convert the education instance to a dictionary
    education_dict = education.model_dump()
    education_dict["_id"] = convert_uuid_to_bson(education.id)  # Convert UUID to BSON Binary
    
    # Insert the education entry into the database
    result = db.education.insert_one(education_dict)
    
    # Add the inserted ID to the education dictionary (UUID as a string for responses)
    education_dict["id"] = str(education.id)
    
    # Return the education dictionary with the inserted ID
    return education_dict

# Get all education entries
@router.get("/education/", response_model=List[Education])
async def get_education():
    education_entries = []
    async for education in db.education.find():
        education["id"] = str(education["_id"].as_uuid())  # Convert BSON Binary back to UUID
        education_entries.append(education)
    return education_entries

# Create a new review
@router.post("/reviews/", response_model=Review)
async def create_review(
    name: str = Form(...),  # Input field for name
    role: str = Form(...),  # Input field for role
    text: str = Form(...),  # Input field for review text
    company: str = Form(...),  # Input field for review text
    photo: UploadFile = File(...),  # Input field for photo upload
):
    # Upload the photo and get the URL
    photo_url = upload_image(photo)  # Call the upload_image function
    photo_url=str(photo_url)
    # Create a Review instance with the provided data
    review = Review(
        name=name,
        role=role,
        text=text,
        company=company,
        photo_url=photo_url,
        id=uuid4(),  # Generate a new UUID for the review
    )
    
    # Convert the review instance to a dictionary
    review_dict = review.model_dump()
    review_dict["_id"] = convert_uuid_to_bson(review.id)  # Convert UUID to BSON Binary
    
    # Insert the review into the database
    result = db.reviews.insert_one(review_dict)
    
    # Add the inserted ID to the review dictionary (UUID as a string for responses)
    review_dict["id"] = str(review.id)
    
    # Return the review dictionary with the inserted ID
    return review_dict
# Get all reviews
@router.get("/reviews/", response_model=List[Review])
async def get_reviews():
    reviews = []
    async for review in db.reviews.find():
        review["id"] = str(review["_id"].as_uuid())  # Convert BSON Binary back to UUID
        reviews.append(review)
    return reviews
