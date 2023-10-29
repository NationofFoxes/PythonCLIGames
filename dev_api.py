from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
import uvicorn, json, secrets
import connect, disconnect, move


app = FastAPI()

game_websockets = {}
# to do, this needs to be more similar to lambda in that it needs to be like a connect trigger and then after that a move trigger.
# the websockets will be not saved here since thats not possible in lambda, it can be got from websocket @connections.
# so the plan is to make a connect lambda and a move lambda,
# separate files, so do that here too.
# this dev_api file is fine, but have it just immediately call
# the lambda files for connect and move, because all logic
# needs to be in those, not in here, cuz all code in here
# doesnt actually exist anywhere in production because
# in production this is all replaced with websockets calling lambdas
# when triggered, thats it.


#@app.websocket("/game")
#async def game_endpoint(websocket: WebSocket):
#    await websocket.accept()

#    game_id = await websocket.receive_text()  # each player inputs the game_id

#    if game_id not in game_websockets:  # first player to put it in makes a new game
#        from tic_tac_toe.game import Game
#        game = Game()
#        game_websockets[game_id] = {
#            'game': game,
#            'players': [websocket],
#        }
#        await websocket.send_text(game.display())  # display the game to myself
#    else:  # player 2 adds himself as a player, and waits for player 1's move
#        game_websockets[game_id]['players'] += [websocket]
#        game = game_websockets[game_id]['game']
#        await websocket.send_text(game.display())  # display the game to myself
#        opponent = [player for player in game_websockets[game_id]['players'] if player != websocket][0]
#        opps_move_new_state = await websocket.receive_text()  # wait for opponent's move updated game state
#        await websocket.send_text(opps_move_new_state.display)  # display the updated game state
#    while 1:
#        is_invalid = True
#        while is_invalid:  # only move forward if my move is valid
#            my_move = await websocket.receive_text()  # get my move
#            if my_move == 'save':
#                print('SAVE')
#                websocket.close()
#                return
#            new_state = game.move(my_move)  # pass my move thru the game logic
#            is_invalid = new_state.is_invalid  # get move validity
#        for player in game_websockets[game_id]['players']:      
#            await player.send_text(new_state.display)  # display the updated game state to both players
#        opponent = [player for player in game_websockets[game_id]['players'] if player != websocket][0]
#        opps_move_new_state = await opponent.receive_text()  # wait for opponent's move updated game state
#        await websocket.send_text(opps_move_new_state.display)  # display the updated game state


#if __name__ == "__main__":
#    uvicorn.run(app, host="localhost", port=8000, log_level="info")



#mock

#class Game:
#    def __init__(self, id):
#        self.id = id
#        self.connections = []

#    def connect(self, websocket):
#        self.connections += [websocket]
        

# WebSocket route to handle connections, disconnects, and "turn" events
@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            message = await websocket.receive_text()
            try:
                event = {
                    "requestContext": {
                        "connectionId": secrets.token_urlsafe(6)
                    },
                    "body": message,
                    "isLocal": True,
                }
                print(f"{event=}")
                body = json.loads(message)
                if body["action"] == "connect":
                    # Handle $connect event
                    connect.lambda_handler(event, None)
                    response_data = {"action": "connect", "message": "Connected to the game"}
                    await websocket.send_json(response_data)
                elif body["action"] == "disconnect":
                    # Handle $disconnect event
                    response_data = {"action": "disconnect", "message": "Disconnected from the WebSocket"}
                    disconnect.lambda_handler(event, None)
                    await websocket.send_json(response_data)
                elif body["action"] == "move":
                    # Handle the custom "move" event
                    move.lambda_handler(event, None)
                    await websocket.send_json(response_data)
            except json.JSONDecodeError:
                # Handle invalid JSON messages
                await websocket.send_text("Invalid JSON format")
    except WebSocketDisconnect:
        clients.remove(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
