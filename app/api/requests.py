from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services import create_request
from app.core.database import get_db
from app.schemas.request import RequestCreateSchema





router = APIRouter()


@router.post("/requests")
def create_request_endpoint(
	request: RequestCreateSchema,
	db: Session = Depends(get_db)
):
	result = create_request(
		db,
		request.author_id,
		request.description,
		request.due_date
	)
	return result