from sqlalchemy import Integer, Text, String, DateTime, ForeignKey, func, Column, Index
from sqlalchemy.orm import declarative_base, relationship



Base = declarative_base()

class EmployeeModel(Base):
	__tablename__ = "employees"

	id = Column(Integer, primary_key=True, index=True)
	full_name = Column(String(255), nullable=False)
	job_title = Column(String(100), nullable=False)
	department_id = Column(Integer, ForeignKey("departments.id"))


class DepartmentModel(Base):
	__tablename__ = "departments"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String(100), nullable=False)


class StatusModel(Base):
	__tablename__ = "statuses"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String(20), nullable=False)

class RequestModel(Base):
	__tablename__ = "requests"

	id = Column(Integer, primary_key=True, index=True)
	created_at = Column(DateTime, nullable=False, default=func.now())
	author_id = Column(Integer, ForeignKey("employees.id"))
	executor_id = Column(Integer, ForeignKey("employees.id")) # Необязательное поле, так как у заявки может не быть назначен исполнитель изначально
	description = Column(Text, nullable=False)                 
	due_date = Column(DateTime, nullable=False)
	status_id = Column(Integer, ForeignKey("statuses.id"))

	# Добавляем составной индекс для ускорения поиска
	__table_args__ = (
		Index("idx_requests_performance", "executor_id", "status_id", "due_date"),
	)







