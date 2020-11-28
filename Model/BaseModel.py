import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from Configuration.Configuration import get_connection_path

Base = declarative_base()


class BaseModel(Base):
	@staticmethod
	def init_connection() -> Session:
		connection_string: str = get_connection_path()
		return Session(sqlalchemy.create_engine(connection_string))
