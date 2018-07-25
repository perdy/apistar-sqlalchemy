import logging

from apistar import http
from sqlalchemy.orm import Session

from apistar_sqlalchemy import database

logger = logging.getLogger(__name__)


class SQLAlchemyTransactionHook:

    def __init__(self, nested=False):
        self.nested = nested
        self.txn = None

    def on_request(self, session: Session):
        if self.nested:
            self.txn = session.begin_nested()
        else:
            self.txn = session

    def on_response(self, response: http.Response, exc: Exception) -> http.Response:
        if exc is None:
            self.txn.commit()
            logger.debug('Commit')
        else:
            self.txn.rollback()
            logger.debug('Rollback')

        if not self.nested:
            self.remove_session()

        return response

    def on_error(self, response: http.Response) -> http.Response:
        self.txn.rollback()
        logger.debug('Rollback')

        if not self.nested:
            self.remove_session()

        return response

    def remove_session(self):
        database.Session.remove()
