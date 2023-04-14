import random
import sqlite3
import datetime

import requests


def get_random_header() -> dict | None:
    from settings import SCRAPEOPS_API_KEY

    url = 'http://headers.scrapeops.io/v1/browser-headers?api_key=' + SCRAPEOPS_API_KEY
    response = requests.get(url)
    json_response = response.json()
    header_list = json_response.get('result', None)

    return random.choice(header_list) if header_list else None


class RequestHistory:
    def __init__(self):
        self.con = sqlite3.connect("database.db")
        self.init_db()

    def init_db(self):
        self.con.execute(
            '''
            CREATE TABLE IF NOT EXISTS request_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                offer_id TEXT NOT NULL,
                timestamp timestamp NOT NULL
                )
        ''')

    def is_application_already_submitted(self, email: str, offer_id: str) -> bool:
        cursor = self.con.cursor()
        cursor.execute(
            'select timestamp from request_history where email=? and offer_id=?', (email, offer_id)
        )
        rows = cursor.fetchall()
        cursor.close()
        is_submitted = len(rows) > 0
        if is_submitted:
            print(f'Application of {offer_id} was already submitted on {rows[0][0]}')
        return is_submitted

    def add_application(self, email: str, offer_id: str):
        timestamp = datetime.datetime.now()
        cursor = self.con.cursor()
        cursor.execute(
            'insert into request_history (email, offer_id, timestamp) values (?,?,?)',
            (email, offer_id, timestamp)
        )
        self.con.commit()
        cursor.close()
