from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, database

router = APIRouter(tags=["Jobs"])

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CREATE (POST)
@router.post("/jobs", response_model=schemas.JobResponse)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    new_job = models.Job(
        company=job.company,
        role=job.role,
        status=job.status,
        applied_date=job.applied_date,
        notes=job.notes
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job


# READ ALL (GET)
@router.get("/jobs", response_model=list[schemas.JobResponse])
def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(models.Job).all()
    return jobs


# READ ONE (GET by ID)
@router.get("/jobs/{job_id}", response_model=schemas.JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()

    if not job:
        return {"error": "Job not found"}

    return job


# UPDATE (PUT)
@router.put("/jobs/{job_id}", response_model=schemas.JobResponse)
def update_job(job_id: int, job: schemas.JobCreate, db: Session = Depends(get_db)):
    existing_job = db.query(models.Job).filter(models.Job.id == job_id).first()

    if not existing_job:
        return {"error": "Job not found"}

    existing_job.company = job.company
    existing_job.role = job.role
    existing_job.status = job.status
    existing_job.applied_date = job.applied_date
    existing_job.notes = job.notes

    db.commit()
    db.refresh(existing_job)

    return existing_job


# DELETE
@router.delete("/jobs/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()

    if not job:
        return {"error": "Job not found"}

    db.delete(job)
    db.commit()

    return {"message": "Job deleted successfully"}