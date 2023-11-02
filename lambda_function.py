from utils import GameProps


def lambda_handler(event, context):
    
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
                    gp.save_to_db()  # save to db before letting players make moves
                    gp.send_updated_displays()  # next is player 1's move

                # game doesn't exist, player 1 is initializing a new game
                case "get_game_name":
                    gp.save_to_db()  # save to db before letting player 1 set_game_name
                    gp.ws.send({  # get_game_name
                        "task": "get_game_name",
                        "available_games": gp.available_games
                    })

                # any other player besides 1st and last is connecting
                case _:  # this includes case await_full_game
                    gp.save_to_db()  # save new player to db
                    gp.ws.send({  # make them wait til game is full
                        "task": "await_players"
                    })

        # task: set_game_name
        case "set_game_name":
            gp.set_game_name()  # next is get_num_players
            gp.save_to_db()  # save to db before letting player 1 set_num_players
            gp.ws.send({
                "task": "get_num_players",
                "available_options": gp.game_logic.available_player_num
            })

        # task: set_num_players
        case "set_num_players":
            gp.set_num_players()  # next is await_full_game
            gp.save_to_db()  # save num_players to db
            gp.ws.send({
                "task": "await_players"
            })

        # task: move
        case "move":
            if gp.is_valid_move():
                gp.make_move()
                gp.save_to_db()  # save to db before letting players make moves
                gp.send_updated_displays()  # next player's move
            else:
                gp.ws.send({"task": "retry_move"})

    return response
