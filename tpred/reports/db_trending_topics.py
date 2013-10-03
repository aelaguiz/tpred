import pprint  # NOQA
import tpred.db as db


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


def create_lookup_table(moments):
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
        tm.moment IN ({})
    GROUP BY
        tm.topic_id,
        t.id,
        tm.site_id""".format(",".join([str(m) for m in moments]))

    db.session.execute(q)
    db.session.commit()


def run_report(n, top_n):
    print "Running report for", n, "Periods"
    moments = get_moments(n)

    create_lookup_table(moments)

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
            'start': start_val
        }

    avgs = []
    for (site_id, topic_id, end_val) in end_vals:
        start_val = data[(site_id, topic_id)]['start']

        diff = end_val - start_val

        avg = (diff) / float(n)

        avgs.append((topics[topic_id], site_id, diff, avg))

    avgs = sorted(avgs, key=lambda x: x[2], reverse=True)[:top_n]

    db.session.execute("DROP TABLE tr_mx;")

    return avgs