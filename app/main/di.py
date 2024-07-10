from functools import partial, lru_cache
from logging import getLogger
from typing import Iterable

from fastapi import FastAPI, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app import Config
from app.db.sqlalchemy import SqlaGateway
from app.protocols import DatabaseGateway, Stub, UoW
from app.services import TaskService

logger = getLogger(__name__)


def all_depends(cls: type) -> None:
    init = cls.__init__
    total_ars = init.__code__.co_kwonlyargcount + init.__code__.co_argcount - 1
    init.__defaults__ = tuple(
        Depends() for _ in range(total_ars)
    )


def new_gateway(session: Session = Depends(Stub(Session))):
    yield SqlaGateway(session)


def new_uow(session: Session = Depends(Stub(Session))):
    return session


def create_session_maker():
    db_uri = get_config().db_uri
    if not db_uri:
        raise ValueError("DB_URI env variable is not set")

    engine = create_engine(db_uri)
    return sessionmaker(engine, autoflush=False, expire_on_commit=False)


def new_session(session_maker: sessionmaker) -> Iterable[Session]:
    with session_maker() as session:
        yield session


@lru_cache
def get_config() -> Config:
    return Config()


def init_dependencies(app: FastAPI):
    session_maker = create_session_maker()

    app.dependency_overrides[Session] = partial(new_session, session_maker)
    app.dependency_overrides[DatabaseGateway] = new_gateway
    app.dependency_overrides[UoW] = new_uow
    app.dependency_overrides[TaskService] = TaskService
    app.dependency_overrides[Config] = get_config
    all_depends(TaskService)
