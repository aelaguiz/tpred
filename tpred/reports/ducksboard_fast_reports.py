import tpred.reports.trending_posts as trending_posts
import tpred.ducksboard as ducksboard


if __name__ == '__main__':
    data = list(trending_posts.run_report(15, False))[:12]
    print data
    ducksboard.timeline(data, 237985)

    data = list(trending_posts.run_report(60, False))[:12]
    ducksboard.timeline(data, 238075)

    data = list(trending_posts.run_report(24 * 60, False))[:12]
    ducksboard.timeline(data, 238078)

    data = list(trending_posts.run_report(15, True))[:12]
    ducksboard.timeline(data, 238079)

    data = list(trending_posts.run_report(60, True))[:12]
    ducksboard.timeline(data, 238008)

    data = list(trending_posts.run_report(24 * 60, True))[:12]
    ducksboard.timeline(data, 238080)
