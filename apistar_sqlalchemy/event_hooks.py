from apistar import http
from sqlalchemy.orm import Session

from apistar_sqlalchemy import database


class SQLAlchemyTransactionHook:
    def __init__(self):
        database.Base.metadata.create_all(database.get_engine())

    def on_response(self, response: http.Response, session: Session) -> http.Response:
        session.commit()
        session.close()
        return response

    def on_error(self, response: http.Response, session: Session) -> http.Response:
        session.rollback()
        session.close()
        return response


event_hooks = [
    SQLAlchemyTransactionHook(),
]
