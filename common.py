import twitter
from time import sleep
from datetime import datetime, date, timedelta
import json
import os
import pytz

LIST_ID = os.environ['TWEETTRASH_LIST_ID']
CONSUMER_KEY = os.environ['TWEETTRASH_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['TWEETTRASH_CONSUMER_SECRET']
ACCESS_TOKEN_KEY = os.environ['TWEETTRASH_ACCESS_TOKEN_KEY']
ACCESS_TOKEN_SECRET = os.environ['TWEETTRASH_ACCESS_TOKEN_SECRET']
DATETIME_FORMAT = '%a %b %d %H:%M:%S %z %Y'
OUTPUT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S %z'

TZ = pytz.timezone('Asia/Tokyo')

def today():
    return datetime.today().astimezone(tz=TZ).date()

def init_api():
    return twitter.Api(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token_key=ACCESS_TOKEN_KEY,
        access_token_secret=ACCESS_TOKEN_SECRET
    )

def time_created(status):
    return datetime.strptime(status.created_at, DATETIME_FORMAT).astimezone(tz=TZ)

def get_prev_day_statuses(api=None):
    if api is None:
        api = init_api()

    today_ = today()
    target = today_ - timedelta(days=1)
    since = target - timedelta(days=1)

    theresults = []
    kwargs = {
        'list_id': LIST_ID,
        'include_rts': False,
        'count': 200
    }
    results = api.GetListTimeline(**kwargs)
    maxid = -1
    total = 0
    while len(results) > 1 and time_created(results[0]).date() > since:
        theresults.extend(results)
        maxid = results[-1].id
        results = api.GetListTimeline(max_id=maxid, **kwargs)
        print(f"Got {len(results)} tweets!")
        sleep(1)
    results = [x for x in theresults if time_created(x).date() == target]
    return [x for x in results if x.user.screen_name != 'tweettrashbot']

def post_tweet(txt, api=None):
    if not api:
        api = init_api()
    api.PostUpdate(txt)


def statuses_to_json(xs, f):
    open(f, mode='w').write(
        json.dumps([
            {
                'text': x.text,
                'created': time_created(x).strftime(OUTPUT_DATETIME_FORMAT),
                'user': x.user.name
            } for x in xs
        ], ensure_ascii=False))
