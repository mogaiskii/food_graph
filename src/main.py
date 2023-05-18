__all__ = ['settings', 'app']

from fastapi import WebSocket

from api.graphql.base import graphql_app
from app import app
from settings import settings

app.include_router(graphql_app, prefix="/graphql")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    print('Accepting client connection...')
    await websocket.accept()
    while True:
        try:
            # Wait for any message from the client
            await websocket.receive_text()
            # Send message to the client
            resp = {'value': 11}
            await websocket.send_json(resp)
        except Exception as e:
            print('error:', e)
            break
    print('Bye..')
