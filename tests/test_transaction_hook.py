import pytest
from apistar import http
from apistar_sqlalchemy import database
from apistar_sqlalchemy.event_hooks import SQLAlchemyTransactionHook
from sqlalchemy import create_engine, event

from .models import PuppyModel


@pytest.fixture(scope='function')
def session():
    database.Session.remove()
    engine = create_engine('sqlite://')

    @event.listens_for(engine, 'connect')
    def do_connect(dbapi_connection, connection_record):
        # Disable pysqlite's emitting of the BEGIN statement entirely. Also
        # stops it from emitting COMMIT before any DDL. This issue is fixed in
        # Python 3.6 but not in Python 3.5. More information about the issue
        # can be found here: https://bugs.python.org/issue10740
        dbapi_connection.isolation_level = None

    database.Session.configure(bind=engine)
    database.Base.metadata.create_all(engine)
    return database.Session()


def test_nested_transaction_on_response(session):
    hook = SQLAlchemyTransactionHook(nested=True)
    resp = http.Response(content='test')

    txn = session.begin_nested()

    hook.on_request(session)
    puppy = PuppyModel()
    session.add(puppy)
    hook.on_response(resp, exc=None)

    txn.rollback()


def test_nested_transaction_on_error(session):
    hook = SQLAlchemyTransactionHook(nested=True)
    resp = http.Response(content='test')

    txn = session.begin_nested()

    hook.on_request(session)
    puppy = PuppyModel()
    session.add(puppy)
    hook.on_error(resp)

    txn.rollback()
