import numpy as np
import tpred.db as db
import sqlalchemy as sqla
import tpred.models as models
import tpred.sites as sites

moment_res = db.session.query(
    sqla.distinct(models.TopicMomentModel.moment)).order_by(
        models.TopicMomentModel.moment.desc()).all()
moments = [m[0] for m in moment_res]

site_array = [sites.TWITTER, sites.HN, sites.REDDIT]
topic_idx = {}
moment_idx = {m: i for i, m in enumerate(moments)}
num_moments = len(moments)


#data = [topic_id][site][moment]
data = []

#order_by(models.TopicModel.id.desc()).
for topic_id, topic in db.session.query(models.TopicModel.id, models.TopicModel.topic).all():
    vec = np.zeros((len(site_array), num_moments))

    for site_idx, site_id in enumerate(site_array):
        res = db.session.query(
            models.TopicMomentModel.moment, models.TopicMomentModel.value).filter(
                models.TopicMomentModel.site_id == site_id,
                models.TopicMomentModel.topic_id == topic_id).all()

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

    new_idx = len(data)
    topic_idx[topic_id] = new_idx
    data.append(momentum)

print "Built data"


#for moment in moments:
    #for site_id in [sites.TWITTER, sites.HN, sites.REDDIT]:
        #res = db.session.query(
            #models.TopicMomentModel, models.TopicModel).join(
                #models.TopicModel).filter(
                    #models.TopicMomentModel.site_id == site_id,
                    #models.TopicMomentModel.moment == moment).all()

        #for topic_moment, topic in res:
            #print topic.topic, topic_moment.value

            #topic_idx[topic.topic]
