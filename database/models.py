from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class Music(Base):
    __tablename__ = 'music'
    music_id = Column(Integer, autoincrement=True, primary_key=True)
    music_name = Column(String, nullable=False)
    singer_name = Column(String, nullable=False)
    type_format = Column(String, nullable=False)

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class User(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
