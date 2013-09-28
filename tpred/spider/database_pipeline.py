import datetime
import tpred.models as models
import tpred.db as db
import tpred.model_util as model_util


class DatabasePipeline(object):
    def __init__(self):
        print "Initializing database pipeline"

    def process_item(self, item, spider):
        print "Writing item", item
        sn = model_util.get_sn(item['site_id'], item['sn'])  # NOQA
        #post = model_util.get_post(item['site_id'], item['body'], datetime.datetime.now(), item['site_post_id'], sn)  # NOQA

        #moment = models.PostMomentModel(points=item['points'])

        #post.rel_moments.append(moment)

        #db.session.add(moment)
        #db.session.add(post)

        db.session.commit()

        return item
