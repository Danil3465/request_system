from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services import create_request as create_request_service, change_status
from app.core.database import get_db
from app.schemas.request import RequestCreateSchema, RequestStatusUpdateSchema
from app.models import RequestModel, EmployeeModel, StatusModel
from datetime import date
from sqlalchemy import func







router = APIRouter()


@router.post("/requests")
def create_request_endpoint(
    request: RequestCreateSchema,
    db: Session = Depends(get_db)
):
    result = create_request_service(
        db,
        request.author_id,
        request.description,
        request.due_date
    )
    return result


@router.patch("/requests/{request_id}/status")
def update_request_status(
    request_id: int,
    status_update: RequestStatusUpdateSchema,
    db: Session = Depends(get_db)
):
    try:
        updated_request = change_status(db, request_id, status_update.status_id)
        return updated_request
    except ValueError as v_e:
        raise HTTPException(status_code=400, detail=str(v_e))



@router.get("/requests/report")
def get_report(
    db: Session = Depends(get_db)
):

    status_report = db.query(
        StatusModel.name,
        func.count(RequestModel.id).label("count")
    ).join(
        RequestModel, StatusModel.id == RequestModel.status_id, isouter=True
    ).group_by(StatusModel.name).all()

   
    overdue_count = db.query(RequestModel).filter(
        RequestModel.due_date < date.today()
    ).count()

  
    executor_report = db.query(
        EmployeeModel.full_name,
        func.count(RequestModel.id).label("count")
    ).join(
        RequestModel, EmployeeModel.id == RequestModel.executor_id, isouter=True
    ).filter(
        RequestModel.status_id == 3  
    ).group_by(EmployeeModel.full_name).all()

    return {
        "status_report": [{"status": row.name, "count": row.count} for row in status_report],
        "overdue_count": overdue_count,
        "executor_report": [{"executor": row.full_name, "count": row.count} for row in executor_report]
    }



@router.get("/requests/{request_id}")
def get_request(
    request_id: int,
    db: Session = Depends(get_db)
):
    request = db.query(RequestModel).filter(RequestModel.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    return request


# Эндпоинт удаления (отключён, т.к. не был в ТЗ)
# Для включения раскомментируй декоратор:
#@router.delete("/requests/{request_id}")
def delete_request(
    request_id: int,
    db: Session = Depends(get_db)
):
    request = db.query(RequestModel).filter(RequestModel.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    db.delete(request)
    db.commit()
    return {"message": "Заявка удалена"}

@router.get("/requests")
def get_requests(
    status_id: int | None = None,
    executor_id: int | None = None,
    department_id: int | None = None,
    overdue: bool | None = None,
    db: Session = Depends(get_db)
):

    query = db.query(RequestModel)

    if status_id is not None:
        query = query.filter(RequestModel.status_id == status_id)
    
    if executor_id is not None:
        query = query.filter(RequestModel.executor_id == executor_id)
    
    if department_id is not None:
        query = query.filter(RequestModel.department_id == department_id)
    
    if overdue:
        query = query.filter(RequestModel.due_date < date.today())
    
    return query.all()
    
@router.patch("/requests/{request_id}/executor")
def update_executor(
    request_id: int,
    executor_id: int,  # или через Pydantic-схему
    db: Session = Depends(get_db)
):
    
    request = db.query(RequestModel).filter(RequestModel.id == request_id).first()
    if not request:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    
    
    employee = db.query(EmployeeModel).filter(EmployeeModel.id == executor_id).first()
    if not employee:
        raise HTTPException(status_code=400, detail="Сотрудник не найден")
    
    
    request.executor_id = executor_id
    db.commit()
    db.refresh(request)
    
    return request




