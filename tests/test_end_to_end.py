from typing import List

import pytest
from apistar import ASyncApp, App, Route, TestClient, http, types, validators
from sqlalchemy.orm import Session

from apistar_sqlalchemy import database
from apistar_sqlalchemy.components import SQLAlchemySessionComponent
from apistar_sqlalchemy.event_hooks import SQLAlchemyTransactionHook

from .models import PuppyModel


class PuppyType(types.Type):
    id = validators.Integer(allow_null=True, default=None)
    name = validators.String()


def list_puppies(session: Session) -> List[PuppyType]:
    return [PuppyType(puppy) for puppy in session.query(PuppyModel).all()]


def create_puppy(session: Session, puppy: PuppyType, raise_exception: http.QueryParam) -> http.JSONResponse:
    if raise_exception:
        raise Exception

    model = PuppyModel(**puppy)
    session.add(model)
    session.flush()
    return http.JSONResponse(PuppyType(model), status_code=201)


routes = [
    Route('/puppy/', 'POST', create_puppy),
    Route('/puppy/', 'GET', list_puppies),
]

components = [SQLAlchemySessionComponent(url='sqlite://')]
event_hooks = [SQLAlchemyTransactionHook()]

app = App(routes=routes, components=components, event_hooks=event_hooks)
async_app = ASyncApp(routes=routes, components=components, event_hooks=event_hooks)

engine = components[0].engine


class TestCaseEndToEnd:
    @pytest.fixture(scope='function', params=[app, async_app])
    def client(self, request):
        database.Base.metadata.create_all(engine)
        yield TestClient(request.param)
        database.Base.metadata.drop_all(engine)

    @pytest.fixture(scope='function')
    def puppy(self):
        return {'name': 'canna'}

    def test_insert_and_select_success(self, client, puppy):
        # Successfully create a new record
        response = client.post('/puppy/', json=puppy)
        created_puppy = response.json()
        assert response.status_code == 201
        assert created_puppy['name'] == 'canna'

        # List all the existing records
        response = client.get('/puppy/')
        assert response.status_code == 200
        assert response.json() == [created_puppy]

    def test_insert_and_select_handled_exception(self, client):
        # Failed to create a new record
        response = client.post('/puppy/', json={})
        assert response.status_code == 400

        # List all the existing records
        response = client.get('/puppy/')
        assert response.status_code == 200
        assert response.json() == []

    def test_insert_and_select_unhandled_exception(self, client, puppy):
        with pytest.raises(Exception):
            # Failed to create a new record
            response = client.post('/puppy/?raise_exception=true', json=puppy)
            assert response.status_code == 500

        # List all the existing records
        response = client.get('/puppy/')
        assert response.status_code == 200
        assert response.json() == []
