from cache import Cache
from typing import Dict
from sqlite3 import Connection

import base64
import json
import sqlite3 as sql


class SqliteCache(Cache):
    TABLE_NAME: str = "words"
    _connection: Connection

    def _encode_key(self, key: str) -> str:
        return self._to_b64(key)

    def __init__(self, database_file_path: str):
        self._connection = sql.connect(database_file_path)
        self._connection.cursor().execute(
            f"""CREATE TABLE IF NOT EXISTS {self.TABLE_NAME} (key TEXT PRIMARY KEY UNIQUE, json TEXT)"""
        )
        self._connection.commit()

    def read(self, key: str):
        result = (
            self._connection.cursor()
            .execute(
                f"""SELECT json FROM {self.TABLE_NAME} WHERE key = '{self._encode_key(key)}'"""
            )
            .fetchall()
        )

        if not result:
            raise Exception(f"Could not find '{key}'")

        return json.loads(self._from_b64(result[0][0]))

    def write(self, key: str, data: Dict):
        json_data = json.dumps(data, ensure_ascii=False)
        self._connection.cursor().execute(
            f"""
            INSERT INTO {self.TABLE_NAME} 
            VALUES ('{self._encode_key(key)}', '{self._to_b64(json_data)}')
            """
        )
        self._connection.commit()

    def is_present(self, key: str) -> bool:
        result = (
            self._connection.cursor()
            .execute(
                f"""SELECT COUNT(key) FROM {self.TABLE_NAME} WHERE key = '{self._encode_key(key)}'"""
            )
            .fetchall()
        )
        return result[0][0] != 0

    def _to_b64(self, text: str) -> str:
        bytes = text.encode("utf-8")
        return base64.b64encode(bytes).decode("ascii")

    def _from_b64(self, text: str) -> str:
        bytes = text.encode("ascii")
        return base64.b64decode(bytes).decode("utf-8")
