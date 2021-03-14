import sqlite3
from time import sleep
from datetime import datetime, date, timedelta
from itertools import chain

from tweettrashbot import settings

from tweettrashbot.common import init_api, now, time_created
from tweettrashbot.service import cache_tweets

def fetch_tweets(since=None):
    if since is None:
        since = now() - timedelta(minutes=10)
    elif not isinstance(since, datetime):
        raise ValueError("Must be datetime instance")

    api = init_api()
    kwargs = {
        'list_id': settings.LIST_ID,
        'include_rts': False,
        'count': 50
    }

    maxid = -1
    total = 0

    results = api.GetListTimeline(**kwargs)
    theresults = []
    while len(results) > 1 and time_created(results[0]) > since:
        theresults.extend(results)
        maxid = results[-1].id
        results = api.GetListTimeline(max_id=maxid, **kwargs)
        print(f"Got {len(results)} tweets!")
        sleep(1)
    results = [x for x in theresults if time_created(x) > since and x.user.screen_name != 'tweettrashbot']

    cache_tweets(results)

def sync_members():
    api = init_api()
    members = api.GetListMembers(list_id=settings.LIST_ID)
    conn = sqlite3.connect(settings.DB_LOCATION)
    with conn:
        cur = conn.cursor()
        cur.execute('DELETE FROM members;')
        tpl = ','.join('(?, ?, ?)' for _ in members)
        phs = list(chain.from_iterable(
            [x.screen_name, x.name, x.profile_image_url] for x in members
        ))
        cur.execute(f'INSERT INTO members(username, display_name, profile_img_url) VALUES {tpl}', phs)
    conn.close()

def post_daily_report():
    sync_members()
    conn = sqlite3.connect(settings.DB_LOCATION)
    cur = conn.cursor()
    t = datetime.now().astimezone(settings.TIMEZONE)
    phs = [datetime(t.year, t.month, t.day - 1, 0, 0, 0).astimezone(settings.TIMEZONE), datetime(t.year, t.month, t.day - 1, 23, 59, 59).astimezone(settings.TIMEZONE)]
    phs = [p.timestamp() for p in phs]
    cur.execute('SELECT members.username, count(tweets.tweet_id) FROM members LEFT JOIN tweets ON members.username = tweets.username AND created_at >= ? AND created_at <= ? WHERE members.username != \'tweettrashbot\' GROUP BY members.username', phs)
    stats = cur.fetchall()
    stats = sorted(stats, key=lambda x: x[1], reverse=True)
    top = stats[0]
    bot = stats[-1]
    total = sum(x[1] for x in stats)

    post = f'''昨日 ({t.year}-{t.month:02}-{t.day - 1:02}) の活動まとめ：
総ツイート数: {total} ツイート
活動者数　　: {len(stats)}
ツイ廃王者　: @{top[0]} ({top[1]} ツイート，全体の {100 * top[1] / total:.2f}%)
ビリ廃　　　: @{bot[0]} ({bot[1]} ツイート，全体の {100 * bot[1] / total:.2f}%)
'''
    print(post)
