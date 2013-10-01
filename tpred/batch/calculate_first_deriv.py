import tpred.db as db
import sqlalchemy as sqla
import tpred.models as models
import tpred.sites as sites
import tpred.model_util as model_util
import sys

if model_util.did_run("calculate_first_deriv"):
    sys.exit(1)

model_util.set_ran("calculate_first_deriv")

n = 100

moment_res = db.session.query(
    sqla.distinct(models.TopicMomentModel.moment)).order_by(
        models.TopicMomentModel.moment.desc()).limit(n).all()

# Skip the current moment because it is presumably incomplete
moment_res = moment_res[1:]

for i in reversed(range(len(moment_res))):
    if i == 0:
        break

    moment_from = moment_res[i][0]
    moment_to = moment_res[i - 1][0]

    print moment_from, moment_to

    for site_id in sites.site_array:
        res = db.session.query(models.TopicMomentDerivModel).filter_by(
            site_id=site_id,
            moment_from=moment_from,
            moment_to=moment_to).first()

        if res:
            print "Skipping", site_id, moment_from, moment_to
            continue

        from_vals = db.session.query(models.TopicMomentModel.topic_id, models.TopicMomentModel.moment, models.TopicMomentModel.value).filter(
            models.TopicMomentModel.site_id == site_id,
            models.TopicMomentModel.moment == moment_from).all()

        to_vals = db.session.query(models.TopicMomentModel.topic_id, models.TopicMomentModel.moment, models.TopicMomentModel.value).filter(
            models.TopicMomentModel.site_id == site_id,
            models.TopicMomentModel.moment == moment_to).all()

        from_dict = {r[0]: r[2] for r in from_vals}
        to_dict = {r[0]: r[2] for r in to_vals}

        for topic_id in to_dict.keys():
            if topic_id not in from_dict:
                from_dict[topic_id] = 0

            value = to_dict[topic_id] - from_dict[topic_id]

            m = models.TopicMomentDerivModel(
                topic_id=topic_id,
                site_id=site_id,
                moment_from=moment_from,
                moment_to=moment_to,
                value=value)

            db.session.add(m)

        db.session.commit()
