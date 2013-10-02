import sys
import csv
import tpred.db as db
import tpred.sites as sites


def run_report(n, out_path):
    q = """CREATE TEMPORARY TABLE tr_mx AS SELECT
        tm.site_id,
        tm.topic_id,
        t.topic,
        MIN(tm.moment) AS min_moment,
        MAX(tm.moment) as max_moment
        
    FROM
        topic_moment tm
    JOIN topic t ON tm.topic_id=t.id
    WHERE
        tm.moment IN (
            SELECT
                DISTINCT moment
            FROM
                topic_moment
            ORDER BY
                moment DESC LIMIT {}
        )
    GROUP BY
        tm.topic_id,
        t.id,
        tm.site_id""".format(n)

    db.session.execute(q)
    db.session.commit()

    q = """
    SELECT
        tm.site_id,
        tm.topic_id,
        tm.value,
        tr_mx.topic
    FROM
        topic_moment tm
    JOIN tr_mx ON
        tr_mx.site_id=tm.site_id AND
        tr_mx.topic_id=tm.topic_id AND
        tr_mx.min_moment=tm.moment
    """

    start_vals = db.session.execute(q)

    q = """
    SELECT
        tm.site_id,
        tm.topic_id,
        tm.value
    FROM
        topic_moment tm
    JOIN tr_mx ON
        tr_mx.site_id=tm.site_id AND
        tr_mx.topic_id=tm.topic_id AND
        tr_mx.max_moment=tm.moment
    """

    end_vals = db.session.execute(q)

    topics = {}
    data = {}
    for (site_id, topic_id, start_val, topic) in start_vals:
        topics[topic_id] = topic

        data[(site_id, topic_id)] = {
            'start': start_val,
            'top_posts': []
        }

    site_avgs = {}
    for (site_id, topic_id, end_val) in end_vals:
        start_val = data[(site_id, topic_id)]['start']

        data[(site_id, topic_id)]['end'] = end_val
        data[(site_id, topic_id)]['diff'] = end_val - start_val
        data[(site_id, topic_id)]['avg'] = (end_val - start_val) / float(n)

        if not site_id in site_avgs:
            site_avgs[site_id] = []

        site_avgs[site_id].append((site_id, topic_id, data[(site_id, topic_id)]['avg']))

    topic_chart = {}
    for site_id, avgs in site_avgs.iteritems():
        avgs = sorted(avgs, key=lambda x: x[2], reverse=True)[:10]

        q = """
        SELECT
            btm.topic_id,
            COUNT(*) as num_posts,
            pb.body
        FROM
            body_topic_map btm
            
            JOIN
                post_body pb
            ON
                btm.body_id=pb.id
                
            JOIN
                post p
            ON
                p.body_id=pb.id
        WHERE
            btm.topic_id IN ({})
        GROUP BY
            btm.topic_id,
            pb.id
        ORDER BY
            btm.topic_id,
            num_posts DESC
        """.format(",".join([str(r[1]) for r in avgs]))

        posts = db.session.execute(q)

        top_posts = {}
        for topic_id, num_posts, body in posts:
            if topic_id not in top_posts:
                print topic_id, topics[topic_id], num_posts, body
                top_posts[topic_id] = (num_posts, body)
                data[(site_id, topic_id)]['top_posts'].append((num_posts, body))

                if not topic_id in topic_chart:
                    topic_chart[topic_id] = {}

                topic_chart[topic_id][site_id] = (
                    data[(site_id, topic_id)]['avg'],
                    num_posts,
                    body)

    import pprint
    pprint.pprint(topic_chart)

    header = ["Topic"] + [s + " Momentum" for s in sites.site_names] + [s + " Num Posts" for s in sites.site_names] + [s + " Post" for s in sites.site_names]
    output = []
    for topic_id, data in topic_chart.iteritems():
        vals = []
        num_posts = []
        bodies = []

        for site_id in sites.site_array:
            if site_id not in data:
                vals.append(0)
                num_posts.append(0)
                bodies.append("")
            else:
                avg, num, body = data[site_id]
                vals.append(avg)
                num_posts.append(num)
                bodies.append(body.encode("utf8"))

        output.append(
            [topics[topic_id]] + vals + num_posts + bodies)

    f = open(out_path, "wb")
    w = csv.writer(f)

    w.writerow(header)
    for row in output:
        w.writerow(row)

    f.close()


if __name__ == '__main__':
    n = int(sys.argv[1])
    out_file = sys.argv[2]

    run_report(n, out_file)
