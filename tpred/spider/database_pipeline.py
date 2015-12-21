import datetime
import pprint
import logging
import tpred.models as models
import tpred.db as db
import tpred.model_util as model_util
import tpred.topic_util as topic_util
import sys

log = logging.getLogger(u"tpred")


class DatabasePipeline(object):
    def process_item(self, item, spider):
        sn = model_util.get_sn(item['site_id'], item['sn'])  # NOQA
        post = model_util.get_post(item['site_id'], item['body'], datetime.datetime.now(), item['site_post_id'], sn)  # NOQA
        url = model_util.get_url(item['url'])

        log.debug(pprint.pformat(item))

        moment = models.PostMomentModel(points=item['points'])

        post.rel_moments.append(moment)
        post.rel_urls.append(url)

        topic_util.update_topics(item['site_id'], post.rel_body, set_value=item['points'], stopwords=['reddit'])

        db.session.add(moment)
        db.session.add(post)

        try:
            db.session.commit()
        except Exception:
            log.exception(u"Failed to commit")
            sys.exit(1)

        return item
