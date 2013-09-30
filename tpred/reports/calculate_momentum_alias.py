import sys
import sqlalchemy.sql as sql
import numpy as np
import tpred.db as db
import sqlalchemy as sqla
import tpred.models as models
import tpred.sites as sites
import tpred.mputil as mputil
import cPickle as pickle


global moments
moments = []

global moment_idx
moment_idx = {}

global num_moments
num_moments = 0


def calc_moment(clusters):
    try:
        data = []

        session = db.Session()

        total = len(clusters)

        for i, cluster_id in enumerate(clusters):
            vec = np.zeros((len(sites.site_array), num_moments))

            cluster = session.query(models.TopicClusterModel).filter_by(id=cluster_id).one()
            topics = cluster.rel_topics

            topic_ids = [t.id for t in topics]
            topic_topics = ",".join([t.topic for t in topics])

            for site_idx, site_id in enumerate(sites.site_array):
                res = session.query(
                    models.TopicMomentModel.moment, sql.func.sum(models.TopicMomentModel.value)).filter(
                        models.TopicMomentModel.site_id == site_id,
                        models.TopicMomentModel.topic_id.in_(topic_ids),
                        models.TopicMomentModel.moment.in_(moments)).group_by(
                            models.TopicMomentModel.moment).all()

                for moment, value in res:
                    idx = moment_idx[moment]
                    vec[site_idx][idx] = value

                #print vec[site_idx]

                norm = vec[site_idx]
                old = np.roll(vec[site_idx], 1)
                old[0] = 0

                #print norm
                #print old

                # Set the vector = to the change
                vec[site_idx] = norm - old
                #print vec[site_idx]

            momentum = np.average(vec, axis=1)

            if not np.all(momentum == 0):
                print "Got momentum", cluster_id, topic_topics, momentum
                data.append((cluster_id, topic_topics, momentum))

            if i % 100 == 0:
                print "Done", i, "of", total, "-", str(round(i / float(total) * 100.0, 2)) + "%"

        return data
    except:
        import traceback
        traceback.print_exc()
        return []


def main(out_file, n):
    global num_moments
    global moments
    global moment_idx

    moment_res = db.session.query(
        sqla.distinct(models.TopicMomentModel.moment)).order_by(
            models.TopicMomentModel.moment.desc()).limit(n).all()
    moments = [m[0] for m in moment_res]

    moment_idx = {m: i for i, m in enumerate(moments)}
    num_moments = len(moments)

    clusters = list(db.session.query(models.TopicClusterModel.id).all())
    print "Got", len(clusters), "clusters"

    res = mputil.multiproc(clusters, 4, calc_moment)

    print "Built data"
    f = open(out_file, "wb")
    pickle.dump(res, f)
    f.close()

if __name__ == '__main__':
    out_file = sys.argv[1]
    n = sys.argv[2]

    main(out_file, n)
