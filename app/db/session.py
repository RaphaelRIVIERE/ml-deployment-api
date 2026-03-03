from fastapi import Request
from sqlalchemy.orm import Session
from typing import Generator


def get_db(request: Request) -> Generator[Session, None, None]:
    db = request.app.state.SessionLocal()
    try:
        yield db
    finally:
        db.close()
