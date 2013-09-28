import t
import db
import models
import model_util
import sites

for sn in db.session.query(models.SnModel).all():
    if sn.num_friends is None:
        twmention = t.api.GetUser(screen_name=sn.sn)
        sn = model_util.get_sn(
            sites.TWITTER,
            twmention.screen_name,
            num_followers=twmention.followers_count,
            num_tweets=twmention.statuses_count,
            num_friends=twmention.friends_count,
            num_favorites=twmention.favourites_count,
            verified=twmention.verified)

    #try:
    db.session.commit()
    #except:
        #print "Failed adding tweet"
        #print tweet.id, tweet.created_at, tweet.text, tweet.urls, tweet.user_mentions, tweet.hashtags, tweet.user.screen_name
        #db.session.rollback()
