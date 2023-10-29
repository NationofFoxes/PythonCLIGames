import json


def lambda_handler(event, context):
    # connect:
    # if new game_id, add new game to database
    # if existing game_id add new user/connection to database

    game_id = json.loads(event["body"])["gameId"]
    user_id = json.loads(event["body"])["userId"]
    connection_id = event["requestContext"]["connectionId"]
    isLocal = event.get("isLocal")
    
    # CONNECT TO DATABASE
    if isLocal:  # local database
        import test_database
        db = test_database.Database()
    else:  # remote database
        import boto3
        db = boto3.client("dynamodb")

    # GET GAME DATA FOR game_id
    game_data = db.get_item(TableName="cli_arcade_games", Key={"game_id": {"S": game_id}})

    # ADD users to users LIST FOR game_id
    if "Item" in game_data:  # there is game data for this game_id
        users_string = game_data["Item"]["users"]["S"]
        users_list = json.loads(users_string.replace("'", '"'))
        users_list += [{"user_id": user_id, "connection_id": connection_id}]
    else:  # this game_id doesn't exist yet
        users_list = [{"user_id": user_id, "connection_id": connection_id}]
    # this will create if doesnt exist, or overwrite if exists
    db.put_item(
        TableName="cli_arcade_games",
        Item={"game_id": {"S": game_id}, "users": {"S": str(users_list)}}
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }


#class Game:
#    def __init__(self, id):
#        self.id = id
#        self.connections = []

#    def connect(self, websocket):
#        self.connections += [websocket]
