import tpred.db as db
import sqlalchemy as sqla
import sqlalchemy.sql as sql
import tpred.models as models
import tpred.sites as sites
import tpred.model_util as model_util  # NOQA

def update():
    moment = db.session.query(
        sqla.distinct(models.TopicMomentModel.moment)).order_by(
            models.TopicMomentModel.moment.desc()).limit(1).offset(1).scalar()

    query = """INSERT 
        INTO
            moment_topic_post_count
            (topic_id, body_id, moment, num_posts)  
        SELECT
                tm.topic_id as topic_id,
                b.id AS body_id,
                tm.moment as moment,
                COUNT(*) as num_posts
            FROM
                topic_moment tm
            JOIN
                body_topic_map btm
                    ON tm.topic_id=btm.topic_id
            JOIN
                post_body b
                    ON btm.body_id=b.id
            JOIN
                post p
                    ON p.body_id=b.id
            WHERE
                tm.moment={}
            GROUP BY
                tm.topic_id,
                b.id,
                tm.moment""".format(moment)

    print "Running query"
    db.session.execute(query)
    db.session.commit()

if not model_util.did_run("update_post_count"):
    model_util.set_ran("update_post_count")

    update()
