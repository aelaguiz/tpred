import t
import datetime
import db
import models
import model_util
import sites


for sn in db.session.query(models.SnModel).all():
    if not sn.needs_check:
        continue

    statuses = t.api.GetUserTimeline(screen_name=sn.sn, count=200)

    for tweet in statuses:
        sn = model_util.get_sn(sites.TWITTER, tweet.user.screen_name)
        twm = model_util.get_post(sites.TWITTER, tweet.text, tweet.created_at, tweet.id, sn)

        for mention in tweet.user_mentions:
            msn = model_util.get_sn(sites.TWITTER, mention.screen_name)

            twm.rel_mentions.append(msn)

        for url in tweet.urls:
            urlm = model_util.get_url(url.expanded_url)

            twm.rel_urls.append(urlm)

        for hashtag in tweet.hashtags:
            ht = model_util.get_hashtag(hashtag.text)

            twm.rel_hashtags.append(ht)

        db.session.commit()

    sn.last_check = datetime.datetime.now()

    db.session.add(sn)
    db.session.commit()
