from pydantic import BaseModel, Field, validator
from enum import Enum
from typing import Optional, List, Dict, Any, TYPE_CHECKING
from datetime import date

# Import accomplishment models
if TYPE_CHECKING:
    from .accomplishment_models import Accomplishment
else:
    try:
        from .accomplishment_models import Accomplishment, is_ai_relevant
    except ImportError:
        # Define placeholder for when accomplishment_models isn't available
        class Accomplishment(BaseModel):
            pass
        def is_ai_relevant(accomplishment) -> bool:
            return False

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
    
    # Irrelevant Skills (for filtering demonstration)
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
    description: Optional[str] = Field(None, description="Additional skill description from resume and other input")
    #market_demand: Optional[str] = Field(None, description="Market demand level (High/Medium/Low)")
    
    # Skill metadata
    #is_technical: bool = Field(default=True, description="Whether this is a technical skill")
    #is_ai_relevant: bool = Field(default=False, description="Whether this skill is AI/ML relevant")
    
    @validator('is_ai_relevant', always=True)
    def set_ai_relevance(cls, v, values):
        """Auto-set AI relevance based on category and name"""
        if 'category' in values and values['category'] == SkillCategory.AI_ML:
            return True
        if 'name' in values and values['name'] in {
            SkillName.PYTHON, SkillName.R, SkillName.DATA_ENGINEERING, 
            SkillName.DATA_ANALYSIS, SkillName.STATISTICS
        }:
            return True
        return v
    
    @validator('is_technical', always=True) 
    def set_technical_flag(cls, v, values):
        """Auto-set technical flag based on category"""
        technical_categories = {
            SkillCategory.AI_ML, SkillCategory.PROGRAMMING, 
            SkillCategory.DATA, SkillCategory.INFRASTRUCTURE
        }
        if 'category' in values and values['category'] in technical_categories:
            return True
        return False
        
    class Config:
        schema_extra = {
            "examples": [
                {
                    "name": "Machine Learning",
                    "category": "AI/ML",
                    "description": "Supervised and unsupervised learning algorithms",
                    "market_demand": "High",
                    "is_technical": True,
                    "is_ai_relevant": True
                },
                {
                    "name": "Python", 
                    "category": "Programming",
                    "description": "Python programming language",
                    "market_demand": "High",
                    "is_technical": True,
                    "is_ai_relevant": True
                },
                {
                    "name": "Leadership",
                    "category": "Leadership", 
                    "description": "Team leadership and people management",
                    "market_demand": "High",
                    "is_technical": False,
                    "is_ai_relevant": False
                }
            ]
        }

class HasSkill(BaseModel):
    """Relationship between Person and Skill with proficiency"""
    skill: Skill = Field(..., description="The skill")
    proficiency: int = Field(..., ge=1, le=10, description="Skill proficiency level (1-10)")
    years_experience: Optional[int] = Field(None, ge=0, description="Years of experience with this skill")
    context: Optional[str] = Field(None, description="Context where skill was used/acquired")
    is_primary: bool = Field(default=False, description="Whether this is a primary/core skill")
    last_used: Optional[int] = Field(None, description="Year skill was last used")
    
    @validator('is_primary')
    def validate_primary_skill(cls, v, values):
        """Primary skills should have high proficiency"""
        if v and 'proficiency' in values and values['proficiency'] < 7:
            raise ValueError("Primary skills must have proficiency >= 7")
        return v
    
    class Config:
        schema_extra = {
            "examples": [
                {
                    "skill": {
                        "name": "Machine Learning",
                        "category": "AI/ML",
                        "is_ai_relevant": True
                    },
                    "proficiency": 8,
                    "years_experience": 4,
                    "context": "Built recommendation systems and fraud detection models",
                    "is_primary": True,
                    "last_used": 2024
                },
                {
                    "skill": {
                        "name": "Python",
                        "category": "Programming", 
                        "is_ai_relevant": True
                    },
                    "proficiency": 9,
                    "years_experience": 6,
                    "context": "Primary development language for ML and backend systems",
                    "is_primary": True,
                    "last_used": 2024
                }
            ]
        }

class Person(BaseModel):
    """Person/Employee node with professional information"""
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
    remote_eligible: bool = Field(default=True, description="Eligible for remote work")
    
    # Computed properties
    @property
    def ai_skills(self) -> List[HasSkill]:
        """Get AI-relevant skills"""
        return [hs for hs in self.skills if hs.skill.is_ai_relevant]
    
    @property
    def primary_skills(self) -> List[HasSkill]:
        """Get primary/core skills"""
        return [hs for hs in self.skills if hs.is_primary]
    
    @property
    def ai_accomplishments(self) -> List[Accomplishment]:
        """Get AI-relevant accomplishments""" 
        return [acc for acc in self.accomplishments if is_ai_relevant(acc)]
    
    @property
    def leadership_accomplishments(self) -> List[Accomplishment]:
        """Get leadership-related accomplishments"""
        from .accomplishment_models import AccomplishmentType
        leadership_types = {AccomplishmentType.LED, AccomplishmentType.MANAGED}
        return [acc for acc in self.accomplishments if acc.type in leadership_types]
    
    @property
    def technical_accomplishments(self) -> List[Accomplishment]:
        """Get technical accomplishments (built, shipped, optimized)"""
        from .accomplishment_models import AccomplishmentType
        technical_types = {AccomplishmentType.BUILT, AccomplishmentType.SHIPPED, AccomplishmentType.OPTIMIZED}
        return [acc for acc in self.accomplishments if acc.type in technical_types]
    
    @property
    def research_accomplishments(self) -> List[Accomplishment]:
        """Get research/publication accomplishments"""
        from .accomplishment_models import AccomplishmentType
        return [acc for acc in self.accomplishments if acc.type == AccomplishmentType.PUBLISHED]
    
    def get_skills_by_category(self, category: SkillCategory) -> List[HasSkill]:
        """Get skills filtered by category"""
        return [hs for hs in self.skills if hs.skill.category == category]
    
    def get_max_proficiency_in_category(self, category: SkillCategory) -> int:
        """Get highest proficiency level in a skill category"""
        skills_in_category = self.get_skills_by_category(category)
        return max([hs.proficiency for hs in skills_in_category], default=0)
    
    def get_accomplishments_by_type(self, accomplishment_type) -> List[Accomplishment]:
        """Get accomplishments filtered by type"""
        return [acc for acc in self.accomplishments if acc.type == accomplishment_type]
    
    def get_accomplishments_by_thing_type(self, thing_type) -> List[Accomplishment]:
        """Get accomplishments filtered by thing type"""
        return [acc for acc in self.accomplishments if acc.thing.type == thing_type]
    
    def has_built_ai_systems(self) -> bool:
        """Check if person has built AI/ML systems"""
        from .accomplishment_models import AccomplishmentType, ThingType, Domain
        for acc in self.accomplishments:
            if (acc.type == AccomplishmentType.BUILT and 
                acc.thing.type == ThingType.SYSTEM and
                acc.thing.domain == Domain.AI_ML):
                return True
        return False
    
    def has_led_teams(self) -> bool:
        """Check if person has leadership experience"""
        from .accomplishment_models import AccomplishmentType, ThingType
        for acc in self.accomplishments:
            if (acc.type == AccomplishmentType.LED and 
                acc.thing.type == ThingType.TEAM):
                return True
        return False
    
    def collaboration_score(self) -> int:
        """Calculate collaboration potential based on team projects"""
        from .accomplishment_models import ThingType
        team_projects = 0
        for acc in self.accomplishments:
            if acc.thing.type in {ThingType.PROJECT, ThingType.TEAM}:
                team_projects += 1
        return min(team_projects * 2, 10)  # Cap at 10
    
    class Config:
        schema_extra = {
            "examples": [
                {
                    "name": "Alice Johnson",
                    "email": "alice.johnson@company.com",
                    "current_title": "Senior AI Engineer", 
                    "department": "Engineering",
                    "level": "Senior",
                    "hire_date": "2020-01-15",
                    "years_experience": 8,
                    "previous_companies": ["TechCorp", "DataStartup"],
                    "location": "San Francisco, CA",
                    "remote_eligible": True,
                    "skills": [
                        {
                            "skill": {"name": "Machine Learning", "category": "AI/ML"},
                            "proficiency": 8,
                            "years_experience": 4,
                            "is_primary": True
                        },
                        {
                            "skill": {"name": "Python", "category": "Programming"},
                            "proficiency": 9, 
                            "years_experience": 6,
                            "is_primary": True
                        }
                    ],
                    "accomplishments": [
                        {
                            "type": "BUILT",
                            "thing": {
                                "name": "Fraud Detection System",
                                "type": "SYSTEM",
                                "domain": "AI/ML",
                                "impact": "HIGH",
                                "year": 2024
                            },
                            "context": "Led technical design and implementation",
                            "year": 2024,
                            "role": "Technical Lead"
                        },
                        {
                            "type": "LED",
                            "thing": {
                                "name": "AI Engineering Team",
                                "type": "TEAM", 
                                "domain": "AI/ML",
                                "impact": "MEDIUM",
                                "year": 2023
                            },
                            "context": "Managed team of 6 engineers",
                            "year": 2023,
                            "team_size": 6
                        }
                    ]
                }
            ]
        }

# Utility functions

def get_ai_relevant_skills() -> List[SkillName]:
    """Get list of AI-relevant skill names"""
    ai_skills = [skill for skill in SkillName if skill.value in {
        "Machine Learning", "Deep Learning", "Natural Language Processing", 
        "Computer Vision", "Data Science", "Statistics", "Python", "R",
        "Data Engineering", "Data Analysis"
    }]
    return ai_skills

def get_skills_by_category(category: SkillCategory) -> List[SkillName]:
    """Get skills filtered by category"""
    category_mapping = {
        SkillCategory.AI_ML: [
            SkillName.MACHINE_LEARNING, SkillName.DEEP_LEARNING, 
            SkillName.NATURAL_LANGUAGE_PROCESSING, SkillName.COMPUTER_VISION,
            SkillName.DATA_SCIENCE, SkillName.STATISTICS
        ],
        SkillCategory.PROGRAMMING: [
            SkillName.PYTHON, SkillName.JAVASCRIPT, SkillName.JAVA,
            SkillName.CPP, SkillName.R, SkillName.SQL
        ],
        SkillCategory.DATA: [
            SkillName.DATA_ENGINEERING, SkillName.DATA_ANALYSIS,
            SkillName.BUSINESS_INTELLIGENCE
        ],
        SkillCategory.INFRASTRUCTURE: [
            SkillName.CLOUD_ARCHITECTURE, SkillName.AWS, 
            SkillName.DOCKER, SkillName.KUBERNETES
        ],
        SkillCategory.PRODUCT: [
            SkillName.PRODUCT_STRATEGY, SkillName.PRODUCT_MANAGEMENT
        ],
        SkillCategory.LEADERSHIP: [
            SkillName.LEADERSHIP, SkillName.TEAM_MANAGEMENT
        ],
        SkillCategory.SOFT_SKILLS: [
            SkillName.COMMUNICATION, SkillName.PROJECT_MANAGEMENT
        ]
    }
    return category_mapping.get(category, [])

# Forward reference resolution
Person.model_rebuild()
