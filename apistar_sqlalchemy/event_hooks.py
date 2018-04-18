from apistar import http
from sqlalchemy.orm import Session

from apistar_sqlalchemy import database


class SQLAlchemyTransactionHook:
    def on_response(self, response: http.Response, session: Session) -> http.Response:
        session.commit()
        database.Session.remove()
        return response

    def on_error(self, response: http.Response, session: Session) -> http.Response:
        session.rollback()
        database.Session.remove()
        return response
