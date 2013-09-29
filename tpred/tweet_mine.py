import t
import db
import models
import model_util
import dateutil.parser
import topic_util
import pprint
import sites

res = db.session.query(models.SnModel.site_sn_id).filter(
    models.SnModel.site_id == sites.TWITTER,
    models.SnModel.site_sn_id != None).order_by(models.SnModel.num_followers.desc()).limit(5000).all()

ids = [str(twid[0]) for twid in res]

it = t.stream.statuses.filter(follow=",".join(ids))

for tweet in it:
    #print "-----------------"
    #print ""
    #print ""
    #pprint.pprint(tweet)

    if 'delete' in tweet:
        continue

    if 'text' not in tweet:
        pprint.pprint(tweet)
        continue

    text = tweet['text']
    retweet = False
    if 'retweeted_status' in tweet:
        text = tweet['retweeted_status']['text']
        retweet = True

    user = tweet['user']

    sn = model_util.get_sn(
        sites.TWITTER,
        user['screen_name'],
        site_sn_id=user['id'],
        num_followers=user['followers_count'],
        num_posts=user['statuses_count'],
        num_friends=user['friends_count'],
        num_favorites=user['favourites_count'],
        verified=user['verified'])

    created_at = dateutil.parser.parse(tweet['created_at'])

    twm = model_util.get_post(sites.TWITTER, text, created_at, tweet['id'], sn)
    if retweet:
        twm.repost = True

    if 'user_mentions' in tweet['entities']:
        for mention in tweet['entities']['user_mentions']:
            msn = model_util.get_sn(sites.TWITTER, mention['screen_name'])

            twm.rel_mentions.append(msn)

    if 'hashtags' in tweet['entities']:
        for hashtag in tweet['entities']['hashtags']:
            ht = model_util.get_hashtag(hashtag['text'])

            twm.rel_hashtags.append(ht)

    if 'urls' in tweet['entities']:
        for url in tweet['entities']['urls']:
            urlm = model_util.get_url(url['expanded_url'])

            twm.rel_urls.append(urlm)

    #print sn.sn, text
    topic_util.update_topics(sites.TWITTER, twm.rel_body)

    print sn.sn, twm.rel_body.body
    db.session.commit()
