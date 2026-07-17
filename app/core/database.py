from sqlalchemy import create_engine, sessionmaker

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

