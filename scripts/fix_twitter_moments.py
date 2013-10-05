import tpred.db as db
import tpred.models as models
import tpred.mputil as mputil


def fix_topics(topic_ids):
    session = db.Session()
    for topic_id in topic_ids:
        print "Fixing topic", topic_id

        moments = list(session.query(models.TopicMomentModel).order_by(models.TopicMomentModel.moment.asc()).filter_by(topic_id=topic_id, site_id=1).all())

        last_val = 0
        for moment in moments:
            if not moment.fixed:
                moment.value += last_val
                moment.fixed = True
                session.add(moment)

            last_val = moment.value

        session.commit()

    return []

topics = [t[0] for t in db.session.query(models.TopicModel.id).limit(8).all()]

mputil.multiproc(topics, 8, fix_topics)
