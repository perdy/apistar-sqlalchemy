import os
from typing import List

import pytest
from apistar import ASyncApp, App, Route, TestClient, http, types, validators
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

os.environ.setdefault('SQLALCHEMY_URL', 'sqlite://')

# Import components and hooks based on previous url
from apistar_sqlalchemy.components import components
from apistar_sqlalchemy.event_hooks import event_hooks
from apistar_sqlalchemy import database


class PuppyModel(database.Base):
    __tablename__ = "Puppy"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


class PuppyType(types.Type):
    id = validators.Integer(allow_null=True, default=None)
    name = validators.String()


def list_puppies(session: Session) -> List[PuppyType]:
    return [PuppyType(puppy) for puppy in session.query(PuppyModel).all()]


def create_puppy(session: Session, puppy: PuppyType) -> http.JSONResponse:
    model = PuppyModel(**puppy)
    session.add(model)
    session.flush()
    return http.JSONResponse(PuppyType(model), status_code=201)


routes = [
    Route('/puppy/', 'POST', create_puppy),
    Route('/puppy/', 'GET', list_puppies),
]

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

    def test_insert_and_select_fail(self, client):
        # Failed to create a new record
        response = client.post('/puppy/', json={})
        assert response.status_code == 400

        # List all the existing records
        response = client.get('/puppy/')
        assert response.status_code == 200
        assert response.json() == []
