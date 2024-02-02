import sqlite3 as sql
import sys

class db:
    def __init__(self):
        self.con = sql.connect('main.db', detect_types=sql.PARSE_DECLTYPES |
                                    sql.PARSE_COLNAMES)
        self.con.execute('PRAGMA foreign_keys = ON')
        self.con.commit()
        self.cur = self.con.cursor()
        self.cur.execute(
            '''CREATE TABLE artists(
            artist_ID INTEGER PRIMARY KEY,
            artist_forename TEXT NOT NULL,
            artist_surname TEXT NOT NULL,
            artist_vivace_url TEXT,
            artist_own_url TEXT,
            artist_total_sales INT,
            artist_total_streams INT,
            artist_apmusic_url TEXT,
            artist_spotify_url TEXT,
            artist_ammusic_url TEXT
            )'''
        )