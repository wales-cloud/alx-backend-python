import time
import sqlite3
import functools

# ✅ Global cache dictionary
query_cache = {}

# ✅ with_db_connection decorator
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# ✅ cache_query decorator
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query):
        if query in query_cache:
            print("Using cached result")
            return query_cache[query]
        print("Query not cached, executing...")
        result = func(conn, query)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# ✅ Example usage
if __name__ == "__main__":
    # First call will execute and cache
    users = fetch_users_with_cache(query="SELECT * FROM users")

    # Second call will use cache
    users_again = fetch_users_with_cache(query="SELECT * FROM users")

    print(users_again)
