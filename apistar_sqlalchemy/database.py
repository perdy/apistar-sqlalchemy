import os

from apistar.exceptions import ConfigurationError
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def get_engine():
    try:
        url = os.environ['SQLALCHEMY_URL']
    except KeyError:
        raise ConfigurationError('Environment variable SQLALCHEMY_URL must be defined')

    kwargs = {}
    if url.startswith('postgresql'):  # pragma: no cover
        kwargs['pool_size'] = os.environ.get('SQLALCHEMY_POOL_SIZE', 5)

    return create_engine(url, **kwargs)
