import datetime
import psycopg

class Database:
    def __init__(self, dbname, user, host, password):
        self.conn = psycopg.connect(f"dbname={dbname} user={user} host={host} password={password}")
    
    def get_dynamic_subscribers(self, login, period):
        time_period = datetime.datetime.now().date() - datetime.timedelta(days=period)
        with self.conn.cursor() as cur:
            subscriptions = cur.execute(f"""
            SELECT action, subscription, timestamp FROM subscriptions
            WHERE login = '{login}' AND timestamp >= '{time_period}';
            """).fetchall()

            subscribers = cur.execute(f"""
            SELECT action, subscriber, timestamp FROM subscribers
            WHERE login = '{login}' AND timestamp >= '{time_period}';
            """).fetchall()
            return subscriptions, subscribers
    
    def close_connection(self):
        self.conn.close()