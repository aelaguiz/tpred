import tpred.reports.db_trending_topics as db_trending_topics
import tpred.reports.trending_posts as trending_posts
import tpred.ducksboard as ducksboard


if __name__ == '__main__':
    data = db_trending_topics.run_report(4, 25)
    ducksboard.leaderboard(data, 237838)

    data = db_trending_topics.run_report(96, 25)
    ducksboard.leaderboard(data, 237980)

    data = list(trending_posts.run_report(15, False))
    ducksboard.timeline(data, 237985)
