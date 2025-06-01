from pydantic import BaseModel, Field, validator
from enum import Enum
from typing import Optional, List, Dict, Any, TYPE_CHECKING
from datetime import date
from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, Dict, Any
from datetime import date


class AccomplishmentType(str, Enum):
    """Accomplishment relationship types (verbs)"""
    BUILT = "BUILT"
    SHIPPED = "SHIPPED"
    LED = "LED"
    PUBLISHED = "PUBLISHED"
    WON = "WON"
    OPTIMIZED = "OPTIMIZED"
    MANAGED = "MANAGED"


class ThingType(str, Enum):
    """Thing node types (what was accomplished)"""
    # High overlap nodes (best for team formation)
    PROJECT = "PROJECT"
    SYSTEM = "SYSTEM"
    TEAM = "TEAM"
    PRODUCT = "PRODUCT"

    # Medium overlap nodes
    PROCESS = "PROCESS"
    INITIATIVE = "INITIATIVE"

    # Low overlap nodes (specialized)
    PAPER = "PAPER"
    AWARD = "AWARD"
    ALGORITHM = "ALGORITHM"
    CODE = "CODE"


class Domain(str, Enum):
    """Domain/category for filtering"""
    AI_ML = "AiMl"
    INFRASTRUCTURE = "Infrastructure"
    WEB = "Web"
    MOBILE = "Mobile"
    DATA = "Data"
    PRODUCT = "Product"
    RESEARCH = "Research"
    GENERAL = "General"


class Thing(BaseModel):
    """Node representing what was accomplished"""
    type: ThingType = Field(..., description="Type of thing")
    domain: Optional[Domain] = Field(None, description="Domain/category of thing")


class Accomplishment(BaseModel):
    """Relationship representing an accomplishment"""
    type: AccomplishmentType = Field(..., description="Type of accomplishment (verb)")
    thing: Thing = Field(..., description="What was accomplished")

    impact_description: Optional[str] = Field(None, description="Description of impact/results")
    year: Optional[int] = Field(None, description="Year of accomplishment")
    role: Optional[str] = Field(None, description="Role/capacity in the accomplishment")
    duration: Optional[str] = Field(None, description="How long the accomplishment took")
    team_size: Optional[int] = Field(None, description="Size of team involved")
    context: Optional[str] = Field(None, description="Additional context about the accomplishment")

class SkillCategory(str, Enum):
    """Standardized Skill categories"""
    AI_ML = "AI/ML"
    PROGRAMMING = "Programming" 
    DATA = "Data"
    INFRASTRUCTURE = "Infrastructure"
    PRODUCT = "Product"
    LEADERSHIP = "Leadership"
    SOFT_SKILLS = "Soft Skills"
    DESIGN = "Design"
    MARKETING = "Marketing"
    FINANCE = "Finance"
    LEGAL = "Legal"

class SkillName(str, Enum):
    """Standardized skill names"""
    # AI/ML Skills
    MACHINE_LEARNING = "Machine Learning"
    DEEP_LEARNING = "Deep Learning"
    NATURAL_LANGUAGE_PROCESSING = "Natural Language Processing"
    COMPUTER_VISION = "Computer Vision"
    DATA_SCIENCE = "Data Science"
    STATISTICS = "Statistics"
    
    # Programming Skills  
    PYTHON = "Python"
    JAVASCRIPT = "JavaScript"
    JAVA = "Java"
    CPP = "C++"
    R = "R"
    SQL = "SQL"
    
    # Data/Infrastructure Skills
    DATA_ENGINEERING = "Data Engineering"
    CLOUD_ARCHITECTURE = "Cloud Architecture"
    AWS = "AWS"
    DOCKER = "Docker"
    KUBERNETES = "Kubernetes"
    
    # Product/Business Skills
    PRODUCT_STRATEGY = "Product Strategy"
    PRODUCT_MANAGEMENT = "Product Management"
    DATA_ANALYSIS = "Data Analysis"
    BUSINESS_INTELLIGENCE = "Business Intelligence"
    
    # Soft Skills
    LEADERSHIP = "Leadership"
    TEAM_MANAGEMENT = "Team Management"
    COMMUNICATION = "Communication"
    PROJECT_MANAGEMENT = "Project Management"
    
    # Other Skills
    ADOBE_PHOTOSHOP = "Adobe Photoshop"
    SOCIAL_MEDIA_MARKETING = "Social Media Marketing"
    ACCOUNTING = "Accounting"
    LEGAL_RESEARCH = "Legal Research"

class Department(str, Enum):
    """Standardized department/division for organizational filtering"""
    ENGINEERING = "Engineering"
    DATA_SCIENCE = "Data Science"
    PRODUCT = "Product"
    DESIGN = "Design"
    MARKETING = "Marketing"
    SALES = "Sales"
    OPERATIONS = "Operations"
    FINANCE = "Finance"
    LEGAL = "Legal"
    HR = "HR"

class Level(str, Enum):
    """Estimated seniority levels for career progression"""
    JUNIOR = "Junior"      # Level 1
    MID = "Mid"           # Level 2  
    SENIOR = "Senior"     # Level 3
    PRINCIPAL = "Principal" # Level 4
    DIRECTOR = "Director"  # Level 5
    VP = "VP"             # Level 6

class Skill(BaseModel):
    """Skill node with standardized taxonomy"""
    name: SkillName = Field(..., description="Standardized skill name")
    category: SkillCategory = Field(..., description="Skill category for organization")
    description: str = Field(..., description="Additional skill description from resume and other input")

class HasSkill(BaseModel):
    """Relationship between Person and Skill with proficiency"""
    skill: Skill = Field(..., description="The skill")
    proficiency: int = Field(..., ge=1, le=5, description="Estimated Skill proficiency level (1-5)")
    years_experience: Optional[int] = Field(None, ge=0, description="Years of experience with this skill")
    context: Optional[str] = Field(None, description="Context where/how skill was used/acquired")
    is_primary: bool = Field(default=False, description="Whether this is a primary/core skill")

class Person(BaseModel):
    """Person/Employee node with professional information"""
    id: str = Field(..., description="Unique identifier for the person. This is required.")
    name: str = Field(..., description="Full name")
    email: Optional[str] = Field(None, description="Email address")
    
    # Professional information
    current_title: Optional[str] = Field(None, description="Current job title")
    department: Optional[Department] = Field(None, description="Current department")
    level: Optional[Level] = Field(None, description="Seniority level")
    hire_date: Optional[date] = Field(None, description="Date hired")
    
    # Skills and accomplishments
    skills: List[HasSkill] = Field(default_factory=list, description="List of skills with proficiency")
    accomplishments: List[Accomplishment] = Field(default_factory=list, description="List of accomplishments")
    
    # Career information
    years_experience: Optional[int] = Field(None, ge=0, description="Total years of professional experience")
    previous_companies: List[str] = Field(default_factory=list, description="Previous companies worked at")
    
    # Additional metadata
    location: Optional[str] = Field(None, description="Work location")
