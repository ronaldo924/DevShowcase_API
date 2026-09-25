from sqlalchemy import Column, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship
from .database import Base

project_technology = Table(
    "project_technology",
    Base.metadata,
    Column("project_id", ForeignKey("projects.id"), primary_key=True),
    Column("technology_id", ForeignKey("technologies.id"), primary_key=True),
)

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(180), nullable=False, unique=True, index=True)
    bio = Column(Text, nullable=True)

    projects = relationship(
        "Project",
        back_populates="profile",
        cascade="all, delete-orphan",
    )

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    url = Column(String(500), nullable=False)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)

    profile = relationship("Profile", back_populates="projects")
    technologies = relationship(
        "Technology",
        secondary=project_technology,
        back_populates="projects",
    )
    feedbacks = relationship(
        "Feedback",
        back_populates="project",
        cascade="all, delete-orphan",
    )

class Technology(Base):
    __tablename__ = "technologies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True, index=True)

    projects = relationship(
        "Project",
        secondary=project_technology,
        back_populates="technologies",
    )

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    comment = Column(Text, nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    project = relationship("Project", back_populates="feedbacks")
