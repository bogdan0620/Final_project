from fastapi import FastAPI
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

from music import music_api
from user import user_api


# uvicorn main:app --reload
