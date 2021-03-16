import json
import sqlite3
from datetime import datetime, date, timedelta, timezone
from itertools import chain

from tweettrashbot import settings

from tweettrashbot.common import init_api, now, time_created, post_tweet
from tweettrashbot.service import cache_tweets

class Job:
    def __init__(self):
        self.conn_ = None
        self.users_ = None

    @property
    def conn(self):
        if not self.conn_:
            self.conn_ = sqlite3.connect(settings.DB_LOCATION)
        return self.conn_
    @property
    def users(self):
        if not self.users_:
            cur = self.conn.cursor()
            cur.execute('SELECT username, display_name, profile_img_url FROM members WHERE username != \'tweettrashbot\';')
            self.users_ = {
                row[0]: {
                    'screen_name': row[0],
                    'name': row[1],
                    'profile_img_url': row[2]
                }
                for row in cur.fetchall()
            }

        return self.users_

    def build_ranking_for_date(self, d):
        t0 = datetime(d.year, d.month, d.day, 0, 0, 0, tzinfo=d.tzinfo)
        t1 = datetime(d.year, d.month, d.day, 23, 59, 59, tzinfo=d.tzinfo)
        cur = self.conn.cursor()
        cur.execute('SELECT members.username, count(tweets.tweet_id) as total FROM members LEFT JOIN tweets ON members.username = tweets.username AND created_at >= ? and created_at <= ? WHERE members.username != \'tweettrashbot\' GROUP BY members.username ORDER BY total DESC;', [t0.timestamp(), t1.timestamp()])
        res = [
            {
                'screen_name': row[0],
                'count': row[1],
            }
            for row in cur.fetchall()
        ]
        total = sum(x['count'] for x in res)
        res = [ {**x, 'density': x['count'] / total} for x in res]
        return res

    def build_timedata_for_date(self, d):
        t0 = datetime(d.year, d.month, d.day, 0, 0, 0, tzinfo=d.tzinfo)
        t1 = datetime(d.year, d.month, d.day, 23, 59, 59, tzinfo=d.tzinfo)
        cur = self.conn.cursor()
        cur.execute('SELECT members.username, tweets.created_at / 3600 as hour, count(tweets.tweet_id) as total FROM members LEFT JOIN tweets ON members.username = tweets.username AND created_at >= ? and created_at <= ? WHERE members.username != \'tweettrashbot\' GROUP BY members.username, hour ORDER BY members.username, hour;', [t0.timestamp(), t1.timestamp()])

        data = {}
        for row in cur.fetchall():
            if row[0] not in data:
                data[row[0]] = {}
            if row[1] is None:
                continue
            dt = datetime.fromtimestamp(row[1] * 3600, timezone.utc)
            dtz = dt.astimezone(settings.TIMEZONE)
            h = dtz.hour
            data[row[0]][h] = row[2]

        by_user = {
            k: [
                {
                    'count': v[i] if i in v else 0,
                } for i in range(24)
            ] for k, v in data.items()
        }
        by_user['all'] = [
            {
                'count': sum(v[i]['count'] for v in by_user.values()),
            } for i in range(24)
        ]
        m = max(chain.from_iterable([[x['count'] for x in v] for v in by_user.values()]))
        by_user = {
            k: [
                {
                    **x,
                    'density': 0.5 * x['count'] / m
                } for x in v
            ] for k, v in by_user.items()
        }
        return by_user


    def build_for_date(self, d):
        return {
            'ranking': self.build_ranking_for_date(d),
            'timedata': self.build_timedata_for_date(d)
        }

    def build_available_dates(self):
        cur = self.conn.cursor()
        cur.execute('SELECT created_at / (3600 * 24) as x FROM tweets GROUP BY x;')
        ts = [datetime.fromtimestamp(x[0] * 3600 * 24, timezone.utc).astimezone(settings.TIMEZONE) for x in cur.fetchall()]
        return [t.strftime('%Y-%m-%d') for t in ts]

    def run(self):
        dates = self.build_available_dates()
        data = {
            'dates': dates,
            'users': self.users,
            **{
                k: self.build_for_date(datetime.strptime(k, '%Y-%m-%d').astimezone(settings.TIMEZONE))
                for k in dates
            }
        }
        json.dump(data, open(settings.DATA_DUMP_LOCATION, mode='w'))


def build():
    Job().run()
