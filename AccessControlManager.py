import sqlite3

class AccessControlManager:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name,check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS access_control (
                user TEXT,
                resource TEXT,
                action TEXT,
                PRIMARY KEY (user, resource, action)
            );
        ''')
        self.conn.commit()

    def grant_permission(self, user, resource, action):
        self.cursor.execute('''
            INSERT INTO access_control (user, resource, action)
            VALUES (?, ?, ?);
        ''', (user, resource, action))
        self.conn.commit()

    def check_permission(self, user, resource, action):
        self.cursor.execute('''
            SELECT * FROM access_control
            WHERE user = ? AND resource = ? AND action = ?;
        ''', (user, resource, action))
        return self.cursor.fetchone() is not None

    def revoke_permission(self, user, resource, action):
        self.cursor.execute('''
            DELETE FROM access_control
            WHERE user = ? AND resource = ? AND action = ?;
        ''', (user, resource, action))
        self.conn.commit()
    def get_access_control_rules(self):
        self.cursor.execute('SELECT * FROM access_control;')
        rules = self.cursor.fetchall()
        access_control_rules = []
        for rule in rules:
            access_control_rules.append({
                'user': rule[0],
                'resource': rule[1],
                'action': rule[2]
            })
        return access_control_rules

    def close_connection(self):
        self.conn.close()
