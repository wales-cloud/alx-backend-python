import sqlite3

class ExecuteQuery:
    def __init__(self, query, params=None, db_name="users.db"):
        self.query = query
        self.params = params or ()
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()

    def __exit__(self, exc_type, exc_value, traceback):
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    param = (25,)

    with ExecuteQuery(query, param) as results:
        for row in results:
            print(row)
