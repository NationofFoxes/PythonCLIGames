import importlib, json, re


class User:
    def __init__(self, user_dict):
        self.user_id = user_dict["user_id"]
        self.connection_id = user_dict["connection_id"]
    
    def to_dict(self):
        # get dict of user
        return {"user_id": self.user_id, "connection_id": self.connection_id}


class Websocket:
    def __init__(self, event, is_local, connection_id):
        self.event, self.is_local, self.connection_id = event, is_local, connection_id

    # async if offline
    def send(self, message, connection_id=None):
        # send over websocket connection

        if connection_id:
            to = connection_id
        else:
            to = self.connection_id

        if self.is_local:
            common = importlib.import_module('common')
            websocket = common.websocket_list[to]
            asyncio = importlib.import_module('asyncio')
            asyncio.create_task(websocket.send_json(message))
            return
        else:
            boto3 = importlib.import_module('boto3')
            connection_id = to  # self.event["requestContext"]["connectionId"]
            domain = self.event["requestContext"]["domainName"]
            stage = self.event["requestContext"]["stage"]
            client = boto3.client('apigatewaymanagementapi', endpoint_url=f'https://{domain}/{stage}')
            client.post_to_connection(
                ConnectionId=connection_id,
                Data=json.dumps(message)
            )
            return


class GameProps:
    available_games = [
        "tic_tac_toe",
    ]

    def __init__(self, event):
        # get event properties

        # these are sent every time
        self.event = event
        self.task = json.loads(event["body"])["task"]
        self.game_id = json.loads(event["body"])["gameId"]
        self.user_id = json.loads(event["body"])["userId"]
        self.game_name = json.loads(event["body"]).get("game_name", "")
        self.num_players = json.loads(event["body"]).get("num_players", "")
        if self.num_players:
            self.num_players = int(self.num_players)
        self.connection_id = event["requestContext"]["connectionId"]
        self.is_local = event.get("isLocal") == "true"
        
        # get database connection
        if self.is_local:  # local database
            local_db_utils = importlib.import_module('local_db_utils')
            self.db = local_db_utils.Database()
        else:  # remote database
            boto3 = importlib.import_module('boto3')
            self.db = boto3.client("dynamodb")

        # get websocket connection
        self.ws = Websocket(self.event, self.is_local, self.connection_id)

    def add_game_data(self, game_data):

        # get users and state data
        if "Item" not in game_data:  # very first connection
            users_json = [{"user_id": self.user_id, "connection_id": self.connection_id}]  # no existing users
            state_json = {"category": "get_game_name", "is_started": "false"}  # next is get_game_name
        else:  # not first connection, get users and state from database game_data
            users_string = game_data["Item"]["users"]["S"]
            state_string = game_data["Item"]["state"]["S"]
            if not self.game_name:
                self.game_name = game_data["Item"]["game_name"]["S"]
            if not self.num_players:
                self.num_players = game_data["Item"]["num_players"]["S"]
                if self.num_players:
                    self.num_players = int(self.num_players)
            users_json = json.loads(users_string.replace("'", '"'))
            state_json = json.loads(state_string.replace("'", '"'))

        # set state for this game instance
        self.state = state_json

        # set user objects for this game instance
        self.users = []
        next_user_index = None
        for i, user_json in enumerate(users_json):  # existing users
            self.users += [User(user_json)]
            if user_json["user_id"] == self.user_id:  # check if this user is already added
                next_user_index = (i + 1) % len(users_json)  # get next_user_index 

        # check if game is full, if not add this user and check again if full
        if self.num_players:
            self.is_full_game = len(self.users) == self.num_players
            if not self.is_full_game:  # if game isn't full, add this user
                self.users += [User({"user_id": self.user_id, "connection_id": self.connection_id})]
                self.is_full_game = len(self.users) == self.num_players  # check again
                if self.is_full_game:  # if wasn't full and now is full, this was the last player
                    self.state = {"category": "move", "is_started": "false"}  # next is player 1's move
                    next_user_index = 0

        if next_user_index is not None:  # get next player's connection_id from next_user_index
            self.next_connection_id = self.users[next_user_index].connection_id

        # get game logic
        if self.game_name:
            self.get_game_logic()

        return

    def get_game_logic(self):
        module_name = self.game_name + ".game"
        game_module = importlib.import_module(module_name)
        self.game_logic = game_module.Game(self.state, self.users)

    def set_game_name(self):
        self.game_name = json.loads(self.event["body"])["gameName"]
        self.get_game_logic()
        self.state = {"category": "get_num_players", "is_started": "false"}  # next is get_num_players
        return

    def set_num_players(self):
        self.num_players = int(json.loads(self.event["body"])["numPlayers"])
        self.state = {"category": "await_full_game", "is_started": "false"}  # next is await_full_game
        return

    def initialize_game(self):
        self.display, self.state = self.game_logic.initialize(self.users)
        return

    def is_valid_move(self):
        self.move = json.loads(self.event["body"])["move"]
        return self.game_logic.is_valid_move(self.move)

    def make_move(self):
        self.display, self.state = self.game_logic.move(self.move)
        return

    def save_to_db(self):
        self.db.put_item(  # this will create if doesnt exist, or overwrite if exists
            TableName="cli_arcade_games",
            Item=self.to_dict()
        )

    def send_updated_displays(self):
        # send updated display to player who made move
        self.ws.send({"task": "update_display_wait", "display": self.display})
        # send updated display to next player
        self.ws.send({"task": "update_display_your_turn", "display": self.display}, connection_id=self.next_connection_id)

    def to_dict(self):
        # get dict of game
        users = []
        # get dict of each user
        for user in self.users:
            users += [user.to_dict()]

        return {
            "game_id": {"S": self.game_id},
            "users": {"S": str(users)},
            "state": {"S": str(self.state)},
            "game_name": {"S": self.game_name},
            "num_players": {"S": str(self.num_players)},
        }

    #def add_prop(self, prop_name):
    #    value = json.loads(self.event["body"])[prop_name]
    #    snake_name = camel_to_snake(prop_name)
    #    setattr(self, snake_name, value)


def camel_to_snake(text):
    snake_case = re.sub(r'([a-z])([A-Z])', r'\1_\2', text)
    return snake_case.lower()
