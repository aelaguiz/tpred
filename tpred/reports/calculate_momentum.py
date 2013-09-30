import sys
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


def calc_moment(topics):
    try:
        data = []

        session = db.Session()

        total = len(topics)

        for i, (topic_id, topic) in enumerate(topics):
            vec = np.zeros((len(sites.site_array), num_moments))

            for site_idx, site_id in enumerate(sites.site_array):
                res = session.query(
                    models.TopicMomentModel.moment, models.TopicMomentModel.value).filter(
                        models.TopicMomentModel.site_id == site_id,
                        models.TopicMomentModel.topic_id == topic_id,
                        models.TopicMomentModel.moment.in_(moments)).all()

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
                data.append((topic_id, topic, momentum))

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

    topics = list(db.session.query(models.TopicModel.id, models.TopicModel.topic).all())

    res = mputil.multiproc(topics, 16, calc_moment)

    print "Built data"
    f = open(out_file, "wb")
    pickle.dump(res, f)
    f.close()

if __name__ == '__main__':
    out_file = sys.argv[1]
    n = sys.argv[2]

    main(out_file, n)
