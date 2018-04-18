from apistar import Component
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from apistar_sqlalchemy import database


class SQLAlchemySessionComponent(Component):
    def __init__(self, url: str) -> None:
        """
        Configure a new database backend.

        :param url: SQLAlchemy database url.
        """
        self.engine = create_engine(url)
        database.Session.configure(bind=self.engine)

    def resolve(self) -> Session:
        return database.Session()
