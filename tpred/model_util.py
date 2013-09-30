import time
import db
import models
import settings


def get_sn(site_id, sn_str, **kwargs):
    m = db.session.query(models.SnModel).filter_by(site_id=site_id, sn=sn_str).first()

    if m:
        for k, v in kwargs.iteritems():
            setattr(m, k, v)

        db.session.add(m)

        return m

    #print "Getting sn exception", site_id, sn_str, e
    args = {
        'sn': sn_str,
        'site_id': site_id
    }

    args.update(kwargs)

    m = models.SnModel(**args)

    db.session.add(m)

    return m


def get_topic(topic_str):
    topic_str = topic_str.lower()

    m = db.session.query(models.TopicModel).filter_by(topic=topic_str).first()

    if m:
        return m

    m = models.TopicModel(
        topic=topic_str,
        num_words=topic_str.count(' ') + 1
    )
    db.session.add(m)

    return m


def did_run(key):
    moment = int(time.time() / settings.MOMENT_SECONDS)

    m = db.session.query(
        models.RunHistoryModel).filter(
            models.RunHistoryModel.moment == moment,
            models.RunHistoryModel.key == key).first()

    if m:
        return True

    return False


def set_ran(key):
    moment = int(time.time() / settings.MOMENT_SECONDS)

    m = db.session.query(
        models.RunHistoryModel).filter(
            models.RunHistoryModel.moment == moment,
            models.RunHistoryModel.key == key).first()

    if m:
        return

    m = models.RunHistoryModel(
        key=key,
        moment=moment)

    db.session.add(m)
    db.session.commit()


def did_site_run(site_id):
    moment = int(time.time() / settings.MOMENT_SECONDS)

    m = db.session.query(
        models.SiteRunHistoryModel).filter(
            models.SiteRunHistoryModel.moment == moment,
            models.SiteRunHistoryModel.site_id == site_id).first()

    if m:
        return True

    return False


def set_site_ran(site_id):
    moment = int(time.time() / settings.MOMENT_SECONDS)

    m = db.session.query(
        models.SiteRunHistoryModel).filter(
            models.SiteRunHistoryModel.moment == moment,
            models.SiteRunHistoryModel.site_id == site_id).first()

    if m:
        return

    m = models.SiteRunHistoryModel(
        site_id=site_id,
        moment=moment)

    db.session.add(m)
    db.session.commit()


def get_topic_moment(site_id, topic):
    moment = int(time.time() / settings.MOMENT_SECONDS)

    m = db.session.query(
        models.TopicMomentModel).filter(
            models.TopicMomentModel.moment == moment,
            models.TopicMomentModel.site_id == site_id,
            models.TopicMomentModel.topic_id == topic.id).first()
    if m:
        return m

    try:
        prev_value = db.session.query(models.TopicMomentModel.value).filter_by(moment == moment).order_by(models.TopicMomentModel.moment.desc()).limit(1).one()[0]
    except:
        prev_value = 0

    m = models.TopicMomentModel(
        site_id=site_id,
        moment=moment,
        value=prev_value
    )

    m.rel_topic = topic

    db.session.add(m)

    return m


def get_url(url_str):
    url_str = url_str.lower()

    m = db.session.query(models.UrlModel).filter_by(url=url_str).first()

    if m:
        return m

    m = models.UrlModel(url=url_str)
    db.session.add(m)

    return m


def get_hashtag(hashtag_str):
    hashtag_str = hashtag_str.lower()

    m = db.session.query(models.HashtagModel).filter_by(hashtag=hashtag_str).first()

    if m:
        return m

    m = models.HashtagModel(hashtag=hashtag_str)
    db.session.add(m)

    return m


def get_post(site_id, text, created_at, site_post_id, sn):
    site_post_id = str(site_post_id)

    m = db.session.query(models.PostModel).filter_by(site_id=site_id, site_post_id=site_post_id).first()

    if m:
        return m

    #print "Exception", e
    body = get_post_body(text)

    m = models.PostModel(
        sn_id=sn.id,
        site_id=site_id,
        site_post_id=site_post_id,
        created_at=created_at)
    m.rel_body = body
    db.session.add(m)

    return m


def get_post_body(text):
    m = db.session.query(models.PostBodyModel).filter_by(body=text).first()

    if m:
        return m

    #print "Exception", e
    m = models.PostBodyModel(
        body=text)
    db.session.add(m)

    return m
