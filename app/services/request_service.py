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

def change_status(db: Session, request_id: int, new_status_id: int):
    # проверяем, что статус существует
    status = db.query(StatusModel).filter(StatusModel.id == new_status_id).first()
    if not status:
        raise ValueError("Указанный статус не существует")

    # ищем заявку
    request = db.query(RequestModel).filter(RequestModel.id == request_id).first()
    if not request:
        raise ValueError("Заявка не найдена")

    current_status_id = request.status_id

    if new_status_id == current_status_id:
        return request

    if current_status_id == 3:
        raise ValueError("Нельзя изменить статус выполненной заявки")

    if new_status_id < current_status_id:
        raise ValueError("Нельзя вернуть статус назад")

    if new_status_id > current_status_id + 1:
        raise ValueError("Нельзя перепрыгивать через статус")

    request.status_id = new_status_id
    db.commit()
    db.refresh(request)

    return request
	