from apistar import Component
from sqlalchemy.orm import Session, sessionmaker

from apistar_sqlalchemy import database


class SQLAlchemySessionComponent(Component):
    def __init__(self) -> None:
        """
        Configure a new database backend.

        Args:
          settings: The application settings dictionary.
        """
        self.metadata = database.Base.metadata
        self.engine = database.get_engine()
        self.Session = sessionmaker(bind=self.engine)

    def resolve(self) -> Session:
        return self.Session()


components = [
    SQLAlchemySessionComponent(),
]
