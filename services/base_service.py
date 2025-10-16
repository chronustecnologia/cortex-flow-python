from sqlalchemy.orm import Session
from typing import TypeVar, Type, List

RepositoryType = TypeVar("RepositoryType")

class BaseService:
    def __init__(self, repository: Type[RepositoryType]):
        self.repository = repository

    def create(self, db: Session, obj_in):
        return self.repository(db).create(obj_in)

    def get(self, db: Session, id: int):
        return self.repository(db).get(id)

    def get_all(self, db: Session, skip: int = 0, limit: int = 100):
        return self.repository(db).get_all(skip=skip, limit=limit)

    def update(self, db: Session, id: int, obj_in):
        return self.repository(db).update(id, obj_in)

    def delete(self, db: Session, id: int):
        return self.repository(db).delete(id)

    def exists(self, db: Session, id: int):
        return self.repository(db).exists(id)
