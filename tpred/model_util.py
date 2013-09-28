import db
import models


def get_sn(sn_str):
    try:
        return db.session.query(models.SnModel).filter_by(sn=sn_str).one()
    except:
        m = models.SnModel(sn=sn_str)
        db.session.add(m)

        return m

#def get_domain(domain_str):
    #try:
        #return db.session.query(models.DomainModel).filter_by(domain=domain_str).one()
    #except:
        #m = models.DomainModel(domain=domain_str)
        #db.session.add(m)

        #return m


def get_url(url_str):
    url_str = url_str.lower()

    try:
        return db.session.query(models.UrlModel).filter_by(url=url_str).one()
    except:
        m = models.UrlModel(url=url_str)
        db.session.add(m)

        return m


def get_hashtag(hashtag_str):
    hashtag_str = hashtag_str.lower()

    try:
        return db.session.query(models.HashtagModel).filter_by(hashtag=hashtag_str).one()
    except:
        m = models.HashtagModel(hashtag=hashtag_str)
        db.session.add(m)

        return m


def get_tweet(text, created_at, twitter_id, sn):
    try:
        return db.session.query(models.TweetModel).filter_by(twitter_id=twitter_id).one()
    except:
        m = models.TweetModel(
            sn_id=sn.id,
            twitter_id=twitter_id,
            created_at=created_at,
            text=text)
        db.session.add(m)

        return m
