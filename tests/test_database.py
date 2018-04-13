import os

import pytest
from apistar.exceptions import ConfigurationError
from sqlalchemy.engine import Engine

from apistar_sqlalchemy.database import get_engine


class TestCaseDatabase:
    def test_get_engine(self):
        os.environ['SQLALCHEMY_URL'] = 'sqlite://'
        engine = get_engine()
        assert isinstance(engine, Engine)
        del os.environ['SQLALCHEMY_URL']

    def test_get_engine_no_database_url(self):
        with pytest.raises(ConfigurationError):
            get_engine()
