import db
import models


def get_sn(site_id, sn_str, **kwargs):
    try:
        m = db.session.query(models.SnModel).filter_by(site_id=site_id, sn=sn_str).one()

        for k, v in kwargs.iteritems():
            setattr(m, k, v)

        db.session.add(m)

        return m
    except Exception as e:
        print "Exception", e
        args = {
            'sn': sn_str,
            'site_id': site_id
        }

        args.update(kwargs)

        m = models.SnModel(**args)

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


def get_post(site_id, text, created_at, site_post_id, sn):
    try:
        return db.session.query(models.PostModel).filter_by(site_id=site_id, site_post_id=site_post_id).one()
    except Exception as e:
        print "Exception", e
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
    try:
        return db.session.query(models.PostBodyModel).filter_by(body=text).one()
    except Exception as e:
        print "Exception", e
        m = models.PostBodyModel(
            body=text)
        db.session.add(m)

        return m
