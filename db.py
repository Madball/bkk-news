from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func
from urllib.parse import quote_plus
from os import getenv

Base = declarative_base()


class Article(Base):
	__tablename__ = 'news'

	id = Column(Integer, primary_key=True)
	author = Column(String(255), nullable=False, index=True)
	title = Column(String(255), nullable=False)
	picture_url = Column(String(255), nullable=True)
	body = Column(Text, nullable=False)
	created_at = Column(DateTime, nullable=False, default=func.now(), index=True)
	updated_at = Column(DateTime, nullable=False, default=func.now(), index=True)

	def __str__(self):
		return f'JOB #{self.id}'

	def as_dict(self):
		return {
			'id': self.id,
			'author': self.author,
			'title': self.title,
			'picture_url': self.picture_url,
			'body': self.body,
			'created_at': str(self.created_at),
			'updated_at': str(self.updated_at)
		}


def open_db(create: bool = False):
	db_user = getenv('DB_USER')
	db_pass = getenv('DB_PASS')
	db_host = getenv('DB_HOST')
	db_name = getenv('DB_NAME')
	engine = create_engine(f"mysql://{db_user}:{quote_plus(db_pass)}@{db_host}/{db_name}")

	if create:
		Article.__table__.create(engine)

	db_session = sessionmaker(bind=engine)()

	return db_session
