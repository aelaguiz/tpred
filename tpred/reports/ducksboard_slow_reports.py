import tpred.reports.db_trending_topics as db_trending_topics
import tpred.ducksboard as ducksboard


if __name__ == '__main__':
    data = db_trending_topics.run_report(96 * 7)[:25]
    ducksboard.leaderboard(data, 238025)
