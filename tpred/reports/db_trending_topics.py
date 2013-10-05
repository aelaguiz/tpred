import pprint  # NOQA
import tpred.sites as sites
import tpred.db as db
import collections


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
        tm.moment IN ({}) and t.num_words >= 2
    GROUP BY
        tm.topic_id,
        t.id,
        tm.site_id""".format(",".join([str(m) for m in moments]))

    db.session.execute(q)
    db.session.commit()


def grouped(avgs):
    g1 = _grouped(avgs)

    g2 = _grouped(g1)

    for topic, _, site, val, avg in g2:
        yield (topic, site, val, avg)


def _grouped(avgs):
    ## Group things together
    grouped = collections.defaultdict(dict)

    for topic, words, site, val, avg in avgs:
        #topic = topic.encode("utf8")
        found = False

        for key, data in grouped[site].iteritems():
            if data['words'].issuperset(words) or \
                    words.issuperset(data['words']):
                group_avg = data['avg']

                # If the values are within 5%
                if (avg != 0 and (abs(group_avg - avg) / float(avg)) < 0.05) or \
                        (avg == group_avg):

                    #print "Grouping", topic, "with", data['topic'], "key", key

                    if words.issuperset(data['words']):
                        #print "\tReplacing", data['topic'], "with", topic, "key", key
                        grouped[site][key]['topic'] = topic
                        grouped[site][key]['words'] = words

                    found = True
                    break

        if not found:
            #print "Did not find", topic, "Adding"
            grouped[site][topic] = {
                'topic': topic,
                'words': words,
                'val': val,
                'avg': avg
            }
    
    for site, site_vals in grouped.iteritems():
        for key, data in site_vals.iteritems():
            yield (data['topic'], data['words'], site, data['val'], data['avg'])


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

        avgs.append((topics[topic_id], set(topics[topic_id].split(" ")), sites.site_map[site_id], diff, avg))

    avgs = sorted(avgs, key=lambda x: x[2], reverse=True)[:500]

    print "Grouping", len(avgs), "items"

    grouped_avgs = grouped(avgs)

    db.session.execute("DROP TABLE tr_mx;")

    grouped_avgs = sorted(grouped_avgs, key=lambda x: x[3], reverse=True)

    pprint.pprint(grouped_avgs[:200])

    return grouped_avgs
