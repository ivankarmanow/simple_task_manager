from datetime import datetime
from typing import Optional

from sqlalchemy import Text, ForeignKey
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import MappedAsDataclass
from sqlalchemy.orm import mapped_column

from app.models.status import TaskStatus


class Base(MappedAsDataclass, DeclarativeBase, kw_only=True):
    ...


class Task(Base):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(primary_key=True, init=False)

    title: Mapped[str]
    description: Mapped[str] = mapped_column(Text)
    performers: Mapped[str] = mapped_column(Text)

    status: Mapped[TaskStatus] = mapped_column(insert_default=TaskStatus.ASSIGNED, default=TaskStatus.ASSIGNED)

    own_plan_time: Mapped[int]
    own_real_time: Mapped[Optional[int]] = mapped_column(init=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.current_timestamp(), init=False)
    started_at: Mapped[Optional[datetime]] = mapped_column(init=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(init=False)
    last_paused_at: Mapped[Optional[datetime]] = mapped_column(init=False)
    pause_time: Mapped[int] = mapped_column(default=0)

    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey('task.id'))
    parent: Mapped[Optional["Task"]] = relationship(back_populates="children", init=False)
    children: Mapped[list["Task"]] = relationship(back_populates="parent", remote_side=[id], init=False)
