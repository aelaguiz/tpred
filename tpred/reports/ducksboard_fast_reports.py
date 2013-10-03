import tpred.reports.trending_posts as trending_posts
import tpred.ducksboard as ducksboard


if __name__ == '__main__':
    data = list(trending_posts.run_report(15, False))
    ducksboard.timeline(data, 237985)

    data = list(trending_posts.run_report(60, True))
    ducksboard.timeline(data, 238008)
