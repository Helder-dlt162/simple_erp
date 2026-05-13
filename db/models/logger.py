from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    DateTime,
)
from sqlalchemy.sql import func
from db.base import base
import enum


class LogLevel(enum.Enum):
    DEBUG = 'debug'
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    CRITICAL = 'critical'


class Logger(base):
    __tablename__ = 'logger'

    id = Column(Integer, primary_key=True)
    level = Column(Enum(LogLevel), nullable=False)
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, server_default=func.current_timestamp())

    def __repr__(self):
        return f"<Logger(level={self.level}, message={self.message})>"
