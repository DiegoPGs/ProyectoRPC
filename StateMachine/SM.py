import sqlite3
import logging
import asyncio

class StateMachine:
    def __init__(self):
        self.data = {}

    # public methods
    def get(self, key):
        """
        Getter for data dictionary

        Args:
            key (dictionary key): for data dictionary

        Returns:
            _type_: value of data[key]
        """
        return self.data.get(key)

    def set(self, key, value):
        """
        Setter for data dictionary

        Args:
            key (dictionary key): position to modify
            value (_type_): value to be set
        """
        self.data[key] = value

    def add(self, key, value):
        if key in self.data:
            self.data[key] += value
        else:
            self.data[key] = value

    def mult(self, key, value):
        if key in self.data:
            self.data[key] *= value
        else:
            self.data[key] = 0

    # remote methods
    def read(self, key):
        return self.data.get(key)

    def update(self, key, value, operation):
        actions = {
            'set': self.set,
            'add': self.add,
            'mult': self.mult
        }
        action = actions.get(operation)

        if action:
            action(key, value)
            return True
        else:
            return False

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def read(self, key):
        self.cursor.execute("SELECT value FROM data WHERE key=?", (key,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None

    def update(self, key, value):
        self.cursor.execute("UPDATE data SET value=? WHERE key=?", (value, key))
        self.conn.commit()
        return True
