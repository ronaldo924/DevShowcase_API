from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DevShowcase API",
    description="API Backend da plataforma DevShowcase.",
    version="1.0.0",
)

@app.get("/")
def root():
    return {"message": "DevShowcase API funcionando!"}

@app.post("/api/profiles", response_model=schemas.ProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(data: schemas.ProfileCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Profile).filter(models.Profile.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")

    profile = models.Profile(**data.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

@app.get("/api/profiles/{profile_id}", response_model=schemas.ProfileResponse)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.get(models.Profile, profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil não encontrado.")
    return profile

@app.post("/api/technologies", response_model=schemas.TechnologyResponse, status_code=status.HTTP_201_CREATED)
def create_technology(data: schemas.TechnologyCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Technology).filter(models.Technology.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tecnologia já cadastrada.")

    technology = models.Technology(name=data.name)
    db.add(technology)
    db.commit()
    db.refresh(technology)
    return technology

@app.get("/api/technologies", response_model=list[schemas.TechnologyResponse])
def list_technologies(db: Session = Depends(get_db)):
    return db.query(models.Technology).order_by(models.Technology.id).all()

@app.post("/api/projects", response_model=schemas.ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(data: schemas.ProjectCreate, db: Session = Depends(get_db)):
    profile = db.get(models.Profile, data.profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil não encontrado.")

    technologies = []
    if data.technology_ids:
        technologies = db.query(models.Technology).filter(
            models.Technology.id.in_(data.technology_ids)
        ).all()

        if len(technologies) != len(set(data.technology_ids)):
            raise HTTPException(status_code=400, detail="Uma ou mais tecnologias não existem.")

    project = models.Project(
        title=data.title,
        description=data.description,
        url=str(data.url),
        profile_id=data.profile_id,
        technologies=technologies,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return schemas.ProjectResponse(
        id=project.id,
        title=project.title,
        description=project.description,
        url=project.url,
        profile_id=project.profile_id,
        technology_ids=[technology.id for technology in project.technologies],
    )

@app.get("/api/projects", response_model=list[schemas.ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(models.Project).order_by(models.Project.id).all()

    return [
        schemas.ProjectResponse(
            id=project.id,
            title=project.title,
            description=project.description,
            url=project.url,
            profile_id=project.profile_id,
            technology_ids=[technology.id for technology in project.technologies],
        )
        for project in projects
    ]
