import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

import random
from faker import Faker

from app.core.database import SessionLocal
from app.models import DepartmentModel, EmployeeModel, StatusModel, RequestModel

fake = Faker()

def seed_departments(db):
    existing = db.query(DepartmentModel).count()
    if existing > 0:
        print("Departments already exist. Skipping.")
        return

    departments_names = [
        "IT", "HR", "Finance", "Marketing", "Operations",
        "R&D", "Sales", "Legal", "Customer Support", "Logistics"
    ]

    for name in departments_names:
        db.add(DepartmentModel(name=name))

    db.commit()
    print(f"Created {len(departments_names)} departments.")

def seed_employees(db):
    existing = db.query(EmployeeModel).count()
    if existing > 0:
        print("Employees already exist. Skipping.")
        return

    department_ids = [dept.id for dept in db.query(DepartmentModel).all()]
    if not department_ids:
        print("No departments found. Please run seed_departments() first.")
        return

    employees = []
    for _ in range(1500):  # чуть больше 1000, чтобы был запас для тестов
        employee = EmployeeModel(
            full_name=fake.name(),
            job_title=fake.job(),
            department_id=random.choice(department_ids)
        )
        employees.append(employee)

    db.bulk_save_objects(employees)
    db.commit()
    print(f"Created {len(employees)} employees.")

def seed_requests(db):
    existing = db.query(RequestModel).count()
    if existing > 0:
        print("Requests already exist. Skipping.")
        return

    employee_ids = [emp.id for emp in db.query(EmployeeModel).all()]
    if not employee_ids:
        print("No employees found. Please run seed_employees() first.")
        return

    # проверяем, что статусы существуют, чтобы не получить ошибку внешнего ключа
    status_count = db.query(StatusModel).count()
    if status_count < 3:
        print("Please ensure statuses with IDs 1, 2, 3 exist in the database.")
        return

    total_requests = 1_500_000
    batch_size = 10_000
    created = 0

    for i in range(0, total_requests, batch_size):
        batch = []
        for _ in range(batch_size):
            created_at = fake.date_time_between(start_date="-90d", end_date="now")
            due_date = fake.date_between(start_date="-30d", end_date="+30d")  # часть заявок будет просрочена

            request = RequestModel(
                author_id=random.choice(employee_ids),
                executor_id=random.choice([None, random.choice(employee_ids)]),
                description=fake.sentence(),
                due_date=due_date,
                status_id=random.randint(1, 3),
                created_at=created_at
            )
            batch.append(request)

        db.bulk_save_objects(batch)
        db.commit()
        created += len(batch)
        print(f"Inserted {created} requests...")

    print(f"Created {created} requests.")

if __name__ == "__main__":
    db = SessionLocal()

    seed_departments(db)
    seed_employees(db)
    seed_requests(db)

    db.close()
    print("All data seeded successfully!")