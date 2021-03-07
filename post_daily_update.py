import common
import pandas as pd
from datetime import date, timedelta

def run():
    api = common.init_api()
    statuses = common.get_prev_day_statuses(api=api)
    day = common.today() - timedelta(days=1)

    df = pd.DataFrame([
        {
            'time': common.time_created(s),
            'user': s.user.name,
            'userid': s.user.screen_name,
            'text': s.text
        } for s in statuses
    ])

    total = df.shape[0]
    by_user = df.groupby(['user', 'userid'])['text'].count()
    mvp = by_user.idxmax()
    mvp_c = by_user.max()
    mvpbad = by_user.idxmin()
    mvpbad_c = by_user.min()
    members = len(by_user)

    post = f'''昨日 ({day.year}-{day.month:02}-{day.day:02}) の活動まとめ：
総ツイート数: {total} ツイート
活動者数　　: {members}
ツイ廃王者　: @{mvp[1]} ({mvp_c} ツイート，全体の {100 * mvp_c / total:.2f}%)
ビリ廃　　　: @{mvpbad[1]} ({mvpbad_c} ツイート，全体の {100 * mvpbad_c / total:.2f}%)
'''
    print(post)
    print("Posting ...")
    # common.post_tweet(post, api=api)
    print("OK!")

if __name__ == '__main__':
    run()
