import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('sleep.db', check_same_thread=False)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS sleep (
            user_id INTEGER,
            bedtime TEXT,
            waketime TEXT,
            duration REAL
        )
    ''')
    conn.commit()
    return conn

def add_sleep(conn, user_id, bedtime, waketime):
    bed = datetime.strptime(bedtime, '%H:%M')
    wake = datetime.strptime(waketime, '%H:%M')
    if wake < bed:
        wake = wake.replace(day=wake.day + 1)
    duration = (wake - bed).total_seconds() / 3600
    
    conn.execute('INSERT INTO sleep VALUES (?, ?, ?, ?)', 
                (user_id, bedtime, waketime, duration))
    conn.commit()
    return duration

def get_stats(conn, user_id):
    cursor = conn.execute('SELECT duration FROM sleep WHERE user_id = ?', (user_id,))
    records = cursor.fetchall()
    return records