from pydantic import BaseModel
from datetime import date

class RequestCreateSchema(BaseModel):
	author_id: int
	description: str
	due_date: date

class RequestStatusUpdateSchema(BaseModel):
    status_id: int

