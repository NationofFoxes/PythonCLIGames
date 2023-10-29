import sqlite3


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("test_database.db")
        self.cursor = self.conn.cursor()

        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS cli_arcade_games (
                game_id TEXT PRIMARY KEY,
                users TEXT
            )'''
        )
        return

    def get_item(self, TableName, Key):
        game_id = Key["game_id"]["S"]

        self.cursor.execute(
            f'SELECT game_id, users FROM {TableName} WHERE game_id = ?',
            (game_id,)
        )
        row = self.cursor.fetchone()
        if row:
            game_id = row[0]
            users = row[1]
            data = {"Item": {"game_id": {"S": game_id}, "users": {"S": users}}}
            return data
        else:
            return {}

    def put_item(self, TableName, Item):
        game_id = Item["game_id"]["S"]
        users = Item["users"]["S"]

        self.cursor.execute(
            f'''INSERT OR REPLACE INTO {TableName} (game_id, users)
                VALUES (?, ?)''',
            (game_id, users)
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
