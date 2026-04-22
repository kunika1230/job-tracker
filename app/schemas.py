from pydantic import BaseModel

class JobBase(BaseModel):
    company: str
    role: str
    status: str
    applied_date: str
    notes: str

class JobCreate(JobBase):
    pass

class JobResponse(JobBase):
    id: int

    class Config:
        from_attributes = True