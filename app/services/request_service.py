from sqlalchemy.orm import Session
from app.models import RequestModel, StatusModel

def create_request(db:Session, author_id: int, description: str, due_date: str):
	status = db.query(StatusModel).filter(StatusModel.name == "Новая").first()
	new_request = RequestModel(
		author_id = author_id,
		description = description,
		due_date = due_date,
		status_id = status.id		
	)
	db.add(new_request)
	db.commit()
	db.refresh(new_request)
	
	return new_request

def change_status():
	