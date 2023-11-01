import json
import local_db_utils, backend


# test data

test_event_1_1 = {
  "requestContext": {
    "connectionId": "connection1"
  },
  "body": "{\"action\":\"connect\",\"gameId\":\"game1\",\"userId\":\"user1\"}",
  "isLocal": True,
}

test_event_1_2 = {
  "requestContext": {
    "connectionId": "connection1"
  },
  "body": "{\"action\":\"set_game_name\",\"gameId\":\"game1\",\"userId\":\"user1\"}",
  "isLocal": True,
}

test_event_1_2 = {
  "requestContext": {
    "connectionId": "connection1"
  },
  "body": "{\"action\":\"set_game_name\",\"gameId\":\"game1\",\"userId\":\"user1\"}",
  "isLocal": True,
}

test_event_2 = {
  "requestContext": {
    "connectionId": "connection2"
  },
  "body": "{\"action\":\"connect\",\"gameId\":\"game1\",\"userId\":\"user2\"}",
  "isLocal": True,
}

test_event_3 = {
  "requestContext": {
    "connectionId": "connection3"
  },
  "body": "{\"action\":\"connect\",\"gameId\":\"game2\",\"userId\":\"user3\"}",
  "isLocal": True,
}

# begin testing

# prep
game_id_1 = json.loads(test_event_1["body"])["gameId"]
user_id_1 = json.loads(test_event_1["body"])["userId"]
connection_id_1 = test_event_1["requestContext"]["connectionId"]
game_id_2 = json.loads(test_event_2["body"])["gameId"]
user_id_2 = json.loads(test_event_2["body"])["userId"]
connection_id_2 = test_event_2["requestContext"]["connectionId"]
game_id_3 = json.loads(test_event_3["body"])["gameId"]
user_id_3 = json.loads(test_event_3["body"])["userId"]
connection_id_3 = test_event_3["requestContext"]["connectionId"]
db = local_db_utils.Database()
db.delete(game_id_1)
db.delete(game_id_2)
db.delete(game_id_3)
data = db.get_item(TableName="cli_arcade_games", Key={"game_id": {"S": game_id_1}})
assert not data
data = db.get_item(TableName="cli_arcade_games", Key={"game_id": {"S": game_id_2}})
assert not data
data = db.get_item(TableName="cli_arcade_games", Key={"game_id": {"S": game_id_3}})
assert not data

# test 1

# execute
backend.lambda_handler(test_event_1, None)

# check results
data = db.get_item(TableName="cli_arcade_games", Key={"game_id": {"S": game_id_1}})
assert data
rec_game_id = data["Item"]["game_id"]["S"]
rec_users = data["Item"]["users"]["S"]
assert rec_game_id == game_id_1
assert rec_users == str([{"user_id": user_id_1, "connection_id": connection_id_1}])
print("Test 1 PASSED")

# test 2

# execute
backend.lambda_handler(test_event_2, None)

# check results
data = db.get_item(TableName="cli_arcade_games", Key={"game_id": {"S": game_id_2}})
assert data
rec_game_id = data["Item"]["game_id"]["S"]
rec_users = data["Item"]["users"]["S"]
assert rec_game_id == game_id_2
assert rec_users == str([{"user_id": user_id_1, "connection_id": connection_id_1}, {"user_id": user_id_2, "connection_id": connection_id_2}])
print("Test 2 PASSED")

# test 3

# execute
backend.lambda_handler(test_event_3, None)

# check results
data = db.get_item(TableName="cli_arcade_games", Key={"game_id": {"S": game_id_3}})
assert data
rec_game_id = data["Item"]["game_id"]["S"]
rec_users = data["Item"]["users"]["S"]
assert rec_game_id == game_id_3
assert rec_users == str([{"user_id": user_id_3, "connection_id": connection_id_3}])
# double check game 1
data = db.get_item(TableName="cli_arcade_games", Key={"game_id": {"S": game_id_2}})
assert data
rec_game_id = data["Item"]["game_id"]["S"]
rec_users = data["Item"]["users"]["S"]
assert rec_game_id == game_id_2
assert rec_users == str([{"user_id": user_id_1, "connection_id": connection_id_1}, {"user_id": user_id_2, "connection_id": connection_id_2}])
print("Test 3 PASSED")

# cleanup

db.delete(game_id_1)
db.delete(game_id_2)
db.delete(game_id_3)
db.disconnect()
print("All Tests PASSED!")
