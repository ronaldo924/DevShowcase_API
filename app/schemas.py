from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl

class ProfileCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    bio: str | None = Field(default=None, max_length=1000)

class ProfileResponse(ProfileCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

class TechnologyCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)

class TechnologyResponse(TechnologyCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

class ProjectCreate(BaseModel):
    title: str = Field(min_length=2, max_length=150)
    description: str = Field(min_length=5, max_length=3000)
    url: HttpUrl
    profile_id: int
    technology_ids: list[int] = Field(default_factory=list)

class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str
    url: str
    profile_id: int
    technology_ids: list[int] = Field(default_factory=list)
