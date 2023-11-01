from utils_local import GameProps


# async if offline
async def lambda_handler(event, context):
    
    # GET EVENT AND DATABASE PROPERTIES
    # event, task, game_id, user_id, connection_id, is_local
    gp = GameProps(event)

    # GET GAME DATA FOR game_id FROM DATABASE
    game_data = gp.db.get_item(TableName="cli_arcade_games", Key={"game_id": {"S": gp.game_id}})
    gp.add_game_data(game_data)

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
                    # await if offline
                    await update_displays_await_move(gp)  # next is player 1's move
                    return response

                # game doesn't exist, player 1 is initializing a new game
                case "get_game_name":
                    save_to_db(gp)  # save to db before letting player 1 set_game_name
                    # await if offline
                    await gp.ws.send({  # get_game_name
                        "task": "get_game_name",
                        "available_games": gp.available_games
                    })
                    return response

                # any other player besides 1st and last is connecting
                case _:  # this includes case await_full_game
                    save_to_db(gp)  # save new player to db
                    # await if offline
                    await gp.ws.send({  # make them wait til game is full
                        "task": "await_players"
                    })
                    return response

        # task: set_game_name
        case "set_game_name":
            gp.set_game_name()  # next is get_num_players
            save_to_db(gp)  # save to db before letting player 1 set_num_players
            # await if offline
            await gp.ws.send({
                "task": "get_num_players",
                "available_options": gp.game_logic.available_player_num
            })
            return response

        # task: set_num_players
        case "set_num_players":
            gp.set_num_players()  # next is await_full_game
            save_to_db(gp)  # save num_players to db
            # await if offline
            await gp.ws.send({
                "task": "await_players"
            })
            return response

        # task: move
        case "move":
            if gp.is_valid_move():
                gp.make_move()
                save_to_db(gp)  # save to db before letting players make moves
                # await if offline
                await update_displays_await_move(gp)  # next player's move
                return response
            else:
                # await if offline
                await gp.ws.send({"task": "retry_move"})
                return response

    return response


def save_to_db(gp):
    gp.db.put_item(  # this will create if doesnt exist, or overwrite if exists
        TableName="cli_arcade_games",
        Item=gp.to_dict()
    )
    return


# async if offline
async def update_displays_await_move(gp):
    # send updated display to player who made move
    # await if offline
    await gp.ws.send({"task": "update_display_wait", "display": gp.display})
    # send updated display to next player
    # await if offline
    await gp.ws.send({"task": "update_display_your_turn", "display": gp.display}, connection_id=gp.next_connection_id)
    return
