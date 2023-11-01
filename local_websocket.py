from fastapi import FastAPI, WebSocket
import uvicorn, secrets
from common import websocket_list
import backend_local


app = FastAPI()
        

@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):

    # connect

    await websocket.accept()

    connection_id = secrets.token_urlsafe(6)  # assign random connection_id
    websocket_list[connection_id] = websocket # keep track of all connected websockets

    # get messages

    while True:
        # get message from frontend
        message = await websocket.receive_text()

        # create event for lambda_handler
        event = {
            "requestContext": {
                "connectionId": connection_id
            },
            "body": message,
            "isLocal": "true",
        }

        # execute lambda
        await backend_local.lambda_handler(event, None)  # send
    
    return


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
