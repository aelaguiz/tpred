import pprint  # NOQA
import tpred.sites as sites
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


def run_report(n):
    print "Running report for", n, "Periods"
    moments = get_moments(n)

    create_lookup_table(moments)

    q = """
    SELECT
        tm.site_id,
        tm.topic_id,
        tm.value,
        tr_mx.topic,
        tr_mx.min_moment
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
        tm.value,
        tr_mx.max_moment
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
    for (site_id, topic_id, start_val, topic, min_moment) in start_vals:
        topics[topic_id] = topic

        data[(site_id, topic_id)] = {
            'start': start_val,
            'min_moment': min_moment
        }

    avgs = []
    for (site_id, topic_id, end_val, max_moment) in end_vals:
        start_val = data[(site_id, topic_id)]['start']
        min_moment = data[(site_id, topic_id)]['min_moment']

        min_idx = moments.index(min_moment)
        max_idx = moments.index(max_moment)

        diff = end_val - start_val

        num_moments = (min_idx - max_idx) + 1
        avg = (diff) / float(num_moments)

        #print topics[topic_id], "Start val", start_val, "End Val", end_val, "Max moment", max_moment, "Min Moment", min_moment, "Max idx", max_idx, "Min idx", min_idx, "Num moments", num_moments, "Diff", diff, "Avg", avg

        avgs.append((topics[topic_id], sites.site_map[site_id], diff, avg))

    avgs = sorted(avgs, key=lambda x: x[2], reverse=True)

    ## Group things together
    grouped_avgs = []

    group_topic = None
    group_site = None
    group_val = None
    group_avg = None

    for topic, site, val, avg in avgs:
        found = False

        if site == group_site:
            if group_val == val and group_avg == avg:
                if group_topic in topic:
                    group_topic = topic

                found = True

        if not found:
            group_topic = topic
            group_site = site
            group_val = val
            group_avg = avg

            grouped_avgs.append((topic, site, val, avg))

    db.session.execute("DROP TABLE tr_mx;")

    #pprint.pprint(avgs)

    return grouped_avgs
