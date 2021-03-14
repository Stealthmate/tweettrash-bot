from itertools import chain

import sqlite3

from tweettrashbot.common import time_created
from tweettrashbot.settings import DB_LOCATION

def cache_tweets(statuses):
    conn = sqlite3.connect(DB_LOCATION)
    cur = conn.cursor()
    cur.execute('SELECT tweet_id FROM tweets;')
    existing = set(int(x[0]) for x in cur.fetchall())
    statuses = [x for x in statuses if x.id not in existing]
    seen = set()
    statuses_ = []
    for s in statuses:
        if s.id in seen:
            continue
        statuses_.append(s)
        seen.add(s.id)
    statuses = statuses_

    if statuses:
        tpl = ','.join('(?, ?, ?)' for _ in statuses)
        q = f'INSERT INTO tweets(tweet_id, created_at, username) VALUES {tpl};'
        phs = list(chain.from_iterable(
            [x.id, time_created(x).timestamp(), x.user.screen_name] for x in statuses
        ))

        cur.execute(q, phs)

    conn.commit()
