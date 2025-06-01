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


# Domain nodes for technical areas
class Domain(str, Enum):
    """Domain categories for technical/business areas"""
    AI = "AI"                           # Machine learning, neural networks, AI systems
    DATA_ENGINEERING = "DATA_ENGINEERING"  # Data pipelines, ETL, data platforms
    ANALYTICS = "ANALYTICS"             # BI, reporting, dashboards, data analysis
    DATABASE = "DATABASE"               # Database systems, storage, optimization
    WEB = "WEB"                         # Frontend, web applications, web platforms
    MOBILE = "MOBILE"                   # iOS, Android, mobile applications
    CLOUD = "CLOUD"                     # AWS, Azure, GCP, cloud architecture
    DEVOPS = "DEVOPS"                   # CI/CD, deployment, automation
    SECURITY = "SECURITY"               # Cybersecurity, auth, compliance
    MICROSERVICES = "MICROSERVICES"     # Service architecture, APIs, distributed systems
    PLATFORM = "PLATFORM"               # Internal tools, developer platforms

# WorkType nodes for what type of work was done
class WorkType(str, Enum):
    """WorkType categories for type of work performed"""
    SYSTEM = "SYSTEM"           # Technical systems/platforms
    RESEARCH = "RESEARCH"       # Papers, studies, R&D
    PRODUCT = "PRODUCT"         # Customer-facing features/apps
    TEAM = "TEAM"               # Groups of people
    PROJECT = "PROJECT"         # Time-bounded initiatives
    PROCESS = "PROCESS"         # Workflows, procedures
    AWARD = "AWARD"             # Recognition, honors
    CODE = "CODE"               # Open source, libraries

class Thing(BaseModel):
    """Node representing what was accomplished"""
    type: WorkType = Field(..., description="Type of thing")
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

class HasSkill(BaseModel):
    """Relationship between Person and Skill with proficiency"""
    skill: Skill = Field(..., description="The skill")
    proficiency: Optional[int]  = Field(..., ge=1, le=5, description="Skill proficiency level (1-5): "
                                                                     "1=Beginner (basic familiarity, learning), "
                                                                     "2=Intermediate (can work with guidance), "
                                                                     "3=Proficient (can work independently), "
                                                                     "4=Advanced (can lead others, deep expertise), "
                                                                     "5=Expert (industry expert, thought leader)")
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
