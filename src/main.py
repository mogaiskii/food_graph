from fastapi import FastAPI

from src.db.main import make_connection, get_sessionmaker, destroy_connection
from src.settings import Settings


settings = Settings()

app = FastAPI()


db = make_connection(settings)
sessionmaker = get_sessionmaker(db)


@app.on_event("shutdown")
async def close_connection():
    destroy_connection(db)
