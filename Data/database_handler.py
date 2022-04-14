import os
import sqlite3
import dotenv
from sqlite3.dbapi2 import connect

dotenv.load_dotenv()

class DataBaseHandler():
    def __init__(self):
        self.con = sqlite3.connect(f"{os.path.dirname(os.path.abspath(__file__))}/{os.getenv('DATABASE_NAME')}")
        self.con.row_factory = sqlite3.Row

    def channel_exist(self, guild_id:int):
        cursor = self.con.cursor()
        query = "SELECT * FROM channels WHERE guild_id = ?;"
        cursor.execute(query, (guild_id,))
        result = cursor.fetchone()
        cursor.close()
        if result is None:
            return False
        return True  

    def edit_channel(self, guild_id: int, channel_id: int, message_id: int):
        cursor = self.con.cursor()
        query = "UPDATE channels SET channel_id = ?, message_id = ? WHERE guild_id = ?;"
        cursor.execute(query, (channel_id, message_id, guild_id))
        self.con.commit() 
        cursor.close()  

    def add_channel(self, guild_id: int, channel_id: int, message_id: int):
        cursor = self.con.cursor()
        query = "INSERT INTO channels VALUES (?, ?, ?);"
        cursor.execute(query, (guild_id, channel_id, message_id))
        self.con.commit() 
        cursor.close()   

    def get_channel(self, guild_id: int):
        cursor = self.con.cursor()
        query = "SELECT * FROM channels WHERE guild_id = ?;"
        cursor.execute(query, (guild_id,))
        result = cursor.fetchone()
        cursor.close()
        r = {}
        for i in result.keys():
            r[i] = result[i]
        return r

    def remove_channel(self, guild_id: int):
        cursor = self.con.cursor()
        query = "DELETE FROM channels WHERE guild_id = ?;"
        cursor.execute(query, (guild_id,))
        self.con.commit() 
        cursor.close()

    def add_instruction(self, guild_id: int, instruction: str):
        cursor = self.con.cursor()
        query = "INSERT INTO instruction(guild_id, instruction) VALUES (?, ?);"
        cursor.execute(query, (guild_id, instruction))
        self.con.commit() 
        cursor.close()

    def get_all_instructions(self, guild_id: int):
        cursor = self.con.cursor()
        query = "SELECT * FROM instruction WHERE guild_id = ? ORDER BY priority;"
        cursor.execute(query, (guild_id,))
        result = cursor.fetchall()
        cursor.close()
        r = []
        for i in result:
            r.append(i["instruction"])
        return r

    def remove_instruction(self, guild_id: int, id: int):
        cursor = self.con.cursor()
        query = "DELETE FROM instruction WHERE guild_id = ? and ID = ?;"
        cursor.execute(query, (guild_id, id))
        self.con.commit() 
        cursor.close()

    def remove_all_instructions(self, guild_id: int):
        cursor = self.con.cursor()
        query = "DELETE FROM instruction WHERE guild_id = ?;"
        cursor.execute(query, (guild_id,))
        self.con.commit() 
        cursor.close()