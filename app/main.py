from fastapi import FastAPI
from . import models
from .database import engine
from .routes import jobs

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(jobs.router)

@app.get("/")
def read_root():
    return {"message": "Job Tracker API is running 🚀"}