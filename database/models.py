from database import Base
from sqlalchemy import Column, Integer, String


class Music(Base):
    __tablename__ = 'music'
    file_id = Column(Integer, autoincrement=True, primary_key=True)
    music_name = Column(String)
    singer = Column(String)
    type_format = Column(String)
