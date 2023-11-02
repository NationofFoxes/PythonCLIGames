import asyncio
from utils import GameProps


def lambda_handler(event, context):
    
    # GET EVENT AND DATABASE PROPERTIES
    # event, task, game_id, user_id, connection_id, is_local
    gp = GameProps(event)

    # GET GAME DATA FOR game_id FROM DATABASE
    game_data = gp.db.get_item(TableName="cli_arcade_games", Key={"game_id": {"S": gp.game_id}})
    gp.add_game_data(game_data)

    if gp.is_local:
        loop = event["loop"]
    else:
        loop = asyncio.new_event_loop()

    response = {"statusCode": 200}

    match gp.task:

        # task: connect
        case "connect":

            match gp.state["category"]:

                # came in with connect and next is move? last player just connected
                case "move":
                    # at this point all players have been connected, and its time to start playing
                    gp.initialize_game()  # first initialize the game
                    save_to_db(gp)  # save to db before letting players make moves
                    # next is player 1's move
                    # send updated display to player who made move
                    task1 = loop.create_task(gp.ws.send({"task": "update_display_wait", "display": gp.display}))
                    task2 = loop.create_task(gp.ws.send({"task": "update_display_your_turn", "display": gp.display}, connection_id=gp.next_connection_id))
                    task = asyncio.gather(task1, task2)

                # game doesn't exist, player 1 is initializing a new game
                case "get_game_name":
                    save_to_db(gp)  # save to db before letting player 1 set_game_name
                    task = loop.create_task(gp.ws.send({  # get_game_name
                        "task": "get_game_name",
                        "available_games": gp.available_games
                    }))

                # any other player besides 1st and last is connecting
                case _:  # this includes case await_full_game
                    save_to_db(gp)  # save new player to db
                    task = loop.create_task(gp.ws.send({  # make them wait til game is full
                        "task": "await_players"
                    }))

        # task: set_game_name
        case "set_game_name":
            gp.set_game_name()  # next is get_num_players
            save_to_db(gp)  # save to db before letting player 1 set_num_players
            task = loop.create_task(gp.ws.send({
                "task": "get_num_players",
                "available_options": gp.game_logic.available_player_num
            }))

        # task: set_num_players
        case "set_num_players":
            gp.set_num_players()  # next is await_full_game
            save_to_db(gp)  # save num_players to db
            task = loop.create_task(gp.ws.send({
                "task": "await_players"
            }))

        # task: move
        case "move":
            if gp.is_valid_move():
                gp.make_move()
                save_to_db(gp)  # save to db before letting players make moves
                # next player's move
                # send updated display to player who made move
                task1 = loop.create_task(gp.ws.send({"task": "update_display_wait", "display": gp.display}))
                task2 = loop.create_task(gp.ws.send({"task": "update_display_your_turn", "display": gp.display}, connection_id=gp.next_connection_id))
                task = asyncio.gather(task1, task2)
            else:
                task = loop.create_task(gp.ws.send({"task": "retry_move"}))

    if not gp.is_local:
        loop.run_until_complete(task)
    return response


def save_to_db(gp):
    gp.db.put_item(  # this will create if doesnt exist, or overwrite if exists
        TableName="cli_arcade_games",
        Item=gp.to_dict()
    )
    return
