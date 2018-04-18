import logging

from apistar import Component
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from apistar_sqlalchemy import database

logger = logging.getLogger(__name__)


class SQLAlchemySessionComponent(Component):
    def __init__(self, url: str) -> None:
        """
        Configure a new database backend.

        :param url: SQLAlchemy database url.
        """
        self.engine = create_engine(url)
        database.Session.configure(bind=self.engine)
        logger.info('SQLAlchemy connection created')
        logger.debug('Engine connection to %s', url)

    def resolve(self) -> Session:
        return database.Session()
