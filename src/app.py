from fastapi import FastAPI

from db.main import make_connection, get_sessionmaker, destroy_connection
from settings import settings

app = FastAPI()


db = make_connection(settings)
SessionMaker = get_sessionmaker(db)


@app.on_event("shutdown")
async def close_connection():
    destroy_connection(db)
