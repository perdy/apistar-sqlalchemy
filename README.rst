API Star SQLAlchemy
===================
|build-status| |coverage| |version|

:Version: 0.3.1
:Status: Production/Stable
:Author: José Antonio Perdiguero López

SQLAlchemy integration for API Star.

Features
--------
This library provides **components** for injecting SQLAlchemy ORM sessions into your views and **event_hooks** to
handle commit/rollback behavior based on exceptions in your views.

Quick start
-----------
Install API Star SQLAlchemy:

.. code:: bash

    pip install apistar-sqlalchemy

Create an API Star application adding components and event hooks:

.. code:: python

    from apistar_sqlalchemy.components import SQLAlchemySessionComponent
    from apistar_sqlalchemy.event_hooks import SQLAlchemyTransactionHook

    routes = []

    components = [
        SQLAlchemySessionComponent(url='sqlite://'),
    ]

    event_hooks = [
        SQLAlchemyTransactionHook(),
    ]

    app = App(routes=routes, components=components, event_hooks=event_hooks)

Now you can inject SQLAlchemy Session into your views:

.. code:: python

    from sqlalchemy.orm import Session

    def sqlalchemy_view(session: Session):
        # do something
        return {'message': 'something done'}

Forget about **commit** and **rollback** because there is an event hook that will handle it for you.

Full example
------------

.. code:: python

    from typing import List

    from apistar import App, Route, http, types, validators
    from sqlalchemy import Column, Integer, String
    from sqlalchemy.orm import Session

    from apistar_sqlalchemy.components import SQLAlchemySessionComponent
    from apistar_sqlalchemy.event_hooks import SQLAlchemyTransactionHook
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

    components = [
        SQLAlchemySessionComponent(url='sqlite://'),
    ]

    event_hooks = [
        SQLAlchemyTransactionHook(),
    ]
    
    app = App(routes=routes, components=components, event_hooks=event_hooks)


.. |build-status| image:: https://travis-ci.org/PeRDy/apistar-sqlalchemy.svg?branch=master
    :alt: build status
    :scale: 100%
    :target: https://travis-ci.org/PeRDy/apistar-sqlalchemy
.. |coverage| image:: https://codecov.io/gh/PeRDy/apistar-sqlalchemy/branch/master/graph/badge.svg
    :alt: coverage
    :scale: 100%
    :target: https://codecov.io/gh/PeRDy/apistar-sqlalchemy/branch/master/graph/badge.svg
.. |version| image:: https://badge.fury.io/py/apistar-sqlalchemy.svg
    :alt: version
    :scale: 100%
    :target: https://badge.fury.io/py/apistar-sqlalchemy
