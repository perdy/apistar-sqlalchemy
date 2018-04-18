import logging

from apistar import http
from apistar.exceptions import HTTPException
from sqlalchemy.orm import Session

from apistar_sqlalchemy import database

logger = logging.getLogger(__name__)


class SQLAlchemyTransactionHook:
    def on_response(self, response: http.Response, session: Session, exc: Exception) -> http.Response:
        if exc is None:
            session.commit()
            logger.debug('Commit')
            self.remove_session()
        else:
            session.rollback()
            logger.debug('Rollback')
            self.remove_session()

        return response

    def on_error(self, response: http.Response, session: Session) -> http.Response:
        session.rollback()
        logger.debug('Rollback')
        self.remove_session()
        return response

    def remove_session(self):
        database.Session.remove()
