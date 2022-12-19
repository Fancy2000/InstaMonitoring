import datetime
import psycopg


class Database:
    def __init__(self, dbname, user, host, password):
        self.conn = psycopg.connect(f"dbname={dbname} user={user} host={host} password={password}")

    def put_subscriptions(self, user_id, subscriptions):
        subscriptions_user = []
        for elem in subscriptions.values():
            user_name = str(elem.username)
            subscriptions_user.append(user_name)
        subscriptions = subscriptions_user
        print(user_id)
        print(subscriptions)
        with self.conn.cursor() as cur:
            user_exists = cur.execute(f"""
            SELECT 1 FROM subscriptions
            WHERE user_id = {user_id};""").fetchone()
            str_ids = ', '.join(subscriptions)
            if user_exists != None:

                cur.execute(f"""
                UPDATE subscriptions SET
                list_subs = array_cat((SELECT list_subs FROM subscriptions WHERE user_id = {user_id}), '{{ {str_ids} }}');
                """)
            else:
                cur.execute(f"""
                INSERT INTO subscriptions VALUES
                ({user_id}, '{{ {{ {str_ids} }} }}');
                """)
        self.conn.commit()

    def get_dynamic_subscribers(self, user_id, period):
        with self.conn.cursor() as cur:
            subscriptions = cur.execute(f"""
            SELECT list_subs[array_upper(list_subs, 1)-{period}:array_upper(list_subs, 1)] FROM subscriptions
            WHERE user_id = {user_id};
            """).fetchone()
            return subscriptions

    def close_connection(self):
        self.conn.close()