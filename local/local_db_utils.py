import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("test_database.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS cli_arcade_games (
                game_id TEXT PRIMARY KEY,
                users TEXT,
                state TEXT,
                game_name TEXT,
                num_players TEXT
            )'''
        )
        return

    def get_item(self, TableName, Key):
        game_id = Key["game_id"]["S"]

        self.cursor.execute(
            f'SELECT game_id, users, state, game_name, num_players FROM {TableName} WHERE game_id = ?',
            (game_id,)
        )
        row = self.cursor.fetchone()
        if row:
            game_id = row[0]
            users = row[1]
            state = row[2]
            game_name = row[3]
            num_players = row[4]
            data = {"Item": {"game_id": {"S": game_id}, "users": {"S": users}, "state": {"S": state}, "game_name": {"S": game_name}, "num_players": {"S": num_players}}}
            return data
        else:
            return {}

    def put_item(self, TableName, Item):
        game_id = Item["game_id"]["S"]
        users = Item["users"]["S"]
        state = Item["state"]["S"]
        game_name = Item["game_name"]["S"]
        num_players = Item["num_players"]["S"]

        self.cursor.execute(
            f'''INSERT OR REPLACE INTO {TableName} (game_id, users, state, game_name, num_players)
                VALUES (?, ?, ?, ?, ?)''',
            (game_id, users, state, game_name, num_players)
        )
        self.conn.commit()
        return

    def delete(self, game_id=None):
        if game_id:
            self.cursor.execute(
                'DELETE FROM cli_arcade_games WHERE game_id = ?',
                (game_id,)
            )
        else:
            self.cursor.execute(
                'DELETE FROM cli_arcade_games',
            )
        self.conn.commit()
        return

    def disconnect(self):
        self.conn.close()
        return
