from sqlalchemy import sessionmaker
from __future__ import print_function
import Pyro5
import asyncio
from configurations import database_url

@Pyro5.api.expose
@Pyro5.api.behavior(instance_mode="single")
class StateMachine(object):
    def __init__(self):
        self.data = {}

    # public methods
    def get(self, key):
        return self.data.get(key)
    
    def set(self, key, value):
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
    async def read(self, key):
        # connecto to db and read value with a sql query
        sql = f"SELECT value FROM data WHERE key = {key}"
        
        # return value

    async def update(self, key, value, operation):
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