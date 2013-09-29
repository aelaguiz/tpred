import t
import twitter
import sys
import db
import models
import pprint  # NOQA
import model_util
import sites
import json

for sn in db.session.query(models.SnModel).filter(
        models.SnModel.site_id == sites.TWITTER, models.SnModel.deleted == False).all():
    if sn.num_friends is None or sn.site_sn_id is None:
        print "Loading friends for", sn.sn

        try:
            twmention = t.api.users.show(screen_name=sn.sn)

            sn = model_util.get_sn(
                sites.TWITTER,
                twmention['screen_name'],
                site_sn_id=twmention['id'],
                num_followers=twmention['followers_count'],
                num_posts=twmention['statuses_count'],
                num_friends=twmention['friends_count'],
                num_favorites=twmention['favourites_count'],
                verified=twmention['verified'])
        except twitter.api.TwitterHTTPError as e:
            try:
                data = json.loads(e.response_data)
                code = data['errors'][0]['code']
                if code == 88:
                    print "Rate limited"
                    sys.exit(1)
                elif code == 34 or code == 63:
                    sn.deleted = True
                    print "User deleted", sn.sn
            except Exception as e:
                print e
                pass

            print "Failed getting info for", sn.sn, e

        db.session.commit()

    #try:
    #except:
        #print "Failed adding post"
        #print post.id, post.created_at, post.text, post.urls, post.user_mentions, post.hashtags, post.user.screen_name
        #db.session.rollback()
