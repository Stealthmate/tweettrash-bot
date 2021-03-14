import common
import pandas as pd
from datetime import date, timedelta
import json

class Job:
    def __init__(self, statuses):
        self.statuses = statuses
        self.users = None
        self.ranking = None

    def build_users(self):
        if self.users:
            return self.users

        self.users = {}
        for i, s in enumerate(self.statuses):
            if s.user.screen_name not in self.users:
                self.users[s.user.screen_name] = {
                    'name': s.user.name,
                    'screen_name': s.user.screen_name,
                    'profile_image_url': s.user.profile_image_url
                }
        return self.users

    def build_ranking(self):
        if self.ranking:
            return self.ranking

        self.ranking = {}

        for s in self.statuses:
            sn = s.user.screen_name
            if sn not in self.ranking:
                self.ranking[sn] = 0
            self.ranking[sn] += 1

        self.ranking = sorted([
            {
                'screen_name': k,
                'count': v,
                'density': v / len(self.statuses)
            }
            for k, v in self.ranking.items()
        ], key=lambda x: x['count'], reverse=True)

        return self.ranking

    def build_by_time(self):

        df = pd.DataFrame([
            {
                'time': common.time_created(s),
                'screen_name': s.user.screen_name
            } for s in self.statuses
        ])
        df['time'] = pd.to_datetime(df['time']).dt.hour
        df['dummy'] = 1
        g = df.groupby(['screen_name', 'time'])['dummy'].sum()

        self.by_time = {}
        for u in self.users.keys():
            self.by_time[u] = []
            for i in range(24):
                c = 0
                try:
                    c = int(g.loc[(u, i)])
                except KeyError:
                    pass
                self.by_time[u].append({
                    'count': c,
                    'density': c / len(self.statuses)
                })
        self.by_time['all'] = []
        for i in range(24):
            c = sum(v[i]['count'] for k, v in self.by_time.items() if k != 'all')
            self.by_time['all'].append({
                'count': c,
                'density': c / len(statuses)
            })
        return self.by_time

    def run(self):

        jsdata = {
            'day': (common.today() - timedelta(days=1)).strftime('%Y-%m-%d'),
            'users': self.build_users(),
            'ranking': self.build_ranking(),
            'by_time': self.build_by_time()
        }

        with open('site/public/site-data.json', mode='w') as f:
            json.dump(jsdata, f)

if __name__ == '__main__':
    api = common.init_api()
    statuses = common.get_prev_day_statuses(api=api)
    Job(statuses).run()
