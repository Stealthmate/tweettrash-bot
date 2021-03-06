import sys

from tweettrashbot import tasks

def main():
    p = sys.argv[1]
    if p == 'fetch_tweets':
        tasks.fetch_tweets()
    elif p == 'sync_members':
        tasks.sync_members()
    elif p == 'post_daily_report':
        tasks.post_daily_report()
    elif p == 'build_site':
        tasks.build_site()
    else:
        raise ValueError('Invalid command')

    print("Hello!")

if __name__ == '__main__':
    main()
