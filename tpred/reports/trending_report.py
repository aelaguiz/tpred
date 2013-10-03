import tpred.db as db
import tpred.sites as sites


def get_moments(n):
    q = """
    SELECT
        DISTINCT moment
    FROM
        topic_moment
    ORDER BY
        moment DESC LIMIT {}
    """.format(n)
    moments = [m[0] for m in db.session.execute(q)]

    return moments


def create_lookup_table(n):
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
        AND
        t.topic NOT LIKE '%forbes30%'
    GROUP BY
        tm.topic_id,
        t.id,
        tm.site_id""".format(n)

    db.session.execute(q)
    db.session.commit()


def run_report(n):
    moments = get_moments(n)
    midpoint = moments[len(moments) / 2]

    create_lookup_table(n)

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
    WHERE tm.moment={}
    """.format(midpoint)

    halfway_vals = db.session.execute(q)

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
            'halfway': start_val,
            'top_posts': []
        }

    for (site_id, topic_id, halfway_val) in halfway_vals:
        data[(site_id, topic_id)]['halfway'] = halfway_val

    avgs = []
    for (site_id, topic_id, end_val) in end_vals:
        start_val = data[(site_id, topic_id)]['start']
        halfway_val = data[(site_id, topic_id)]['halfway']

        data[(site_id, topic_id)]['end'] = end_val
        data[(site_id, topic_id)]['diff'] = end_val - start_val

        data[(site_id, topic_id)]['first_half'] = (halfway_val - start_val) / float(n)
        data[(site_id, topic_id)]['second_half'] = (end_val - halfway_val) / float(n)
        data[(site_id, topic_id)]['avg'] = (end_val - start_val) / float(n)

        if site_id == 1:
            avgs.append((site_id, topic_id, data[(site_id, topic_id)]['avg']))

    avgs = sorted(avgs, key=lambda x: x[2], reverse=True)[:200]

    topic_chart = {}
    for site_id in sites.site_array:
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
            p.site_id={} AND
            btm.topic_id IN ({})
        GROUP BY
            btm.topic_id,
            pb.id
        ORDER BY
            btm.topic_id,
            num_posts DESC
        """.format(site_id, ",".join([str(r[1]) for r in avgs]))

        posts = db.session.execute(q)

        top_posts = {}
        for topic_id, num_posts, body in posts:
            if topic_id not in top_posts:
                top_posts[topic_id] = (num_posts, body)

                if not (site_id, topic_id) in data:
                    data[(site_id, topic_id)] = {
                        'start': 0,
                        'end': 0,
                        'diff': 0,
                        'first_half': 0,
                        'second_half': 0,
                        'avg': 0,
                        'top_posts': []
                    }

                data[(site_id, topic_id)]['top_posts'].append((num_posts, body))

                if not topic_id in topic_chart:
                    topic_chart[topic_id] = {}

                topic_chart[topic_id][site_id] = (
                    data[(site_id, topic_id)]['avg'],
                    data[(site_id, topic_id)]['first_half'],
                    data[(site_id, topic_id)]['second_half'],
                    num_posts,
                    body)

    header = ["Topic"]

    for s in sites.site_names:
        header += [s + " " + o + " Momentum" for o in ["Overall", "Delta"]]

    header += [s + " Num Posts" for s in sites.site_names] + [s + " Post" for s in sites.site_names]
    output = []
    for topic_id, data in topic_chart.iteritems():
        vals = []
        num_posts = []
        bodies = []

        for site_id in sites.site_array:
            if site_id not in data:
                vals.append("0")
                vals.append("0")
                num_posts.append("0")
                bodies.append("")
            else:
                avg, first_half, second_half, num, body = data[site_id]
                vals.append(str(avg))
                vals.append(str(second_half - first_half))
                num_posts.append(str(num))
                bodies.append(body)

        output.append(
            [topics[topic_id]] + vals + num_posts + bodies)

    return header, output
