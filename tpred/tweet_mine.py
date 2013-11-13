import db
import model_util
import dateutil.parser
import topic_util
import pprint
import sites


def mine(it):
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
            verified=user['verified'],
            pic_url=user['profile_image_url'])

        created_at = dateutil.parser.parse(tweet['created_at'])

        twm = model_util.get_post(sites.TWITTER, text, created_at, tweet['id'], sn)
        if retweet:
            twm.repost = True

        stopwords = []
        if 'user_mentions' in tweet['entities']:
            for mention in tweet['entities']['user_mentions']:
                msn = model_util.get_sn(sites.TWITTER, mention['screen_name'])
                stopwords.append(mention['screen_name'])

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
        topic_util.update_topics(sites.TWITTER, twm.rel_body, stopwords=stopwords)

        #print sn.sn, twm.rel_body.body
        db.session.commit()
