import twitter
import db
import model_util

api = twitter.Api(
    consumer_key='nlH3pUB6J6dRB31YOqVlyQ',
    consumer_secret='ozh7DyDEZql2w2NW4Qt76UgB9oXpHKOABg24jT3c',
    access_token_key='18362611-BIh0HMnGSFQ3wkDtp8lKu4lxPn60zSPppGIUUL5I6',
    access_token_secret='YW5bzat9hFb3eLxL5DZ5MSR0Z6qpnOe8wWQIeRIGUs')

print api.VerifyCredentials()


user = 'jason'
statuses = api.GetUserTimeline(screen_name=user, count=200)

for tweet in statuses:
    sn = model_util.get_sn(tweet.user.screen_name)
    twm = model_util.get_tweet(tweet.text, tweet.created_at, tweet.id, sn)

    for mention in tweet.user_mentions:
        msn = model_util.get_sn(mention.screen_name)

        twm.rel_mentions.append(msn)

    for url in tweet.urls:
        urlm = model_util.get_url(url.expanded_url)

        twm.rel_urls.append(urlm)

    for hashtag in tweet.hashtags:
        ht = model_util.get_hashtag(hashtag.text)

        twm.rel_hashtags.append(ht)

    #try:
    db.session.commit()
    #except:
        #print "Failed adding tweet"
        #print tweet.id, tweet.created_at, tweet.text, tweet.urls, tweet.user_mentions, tweet.hashtags, tweet.user.screen_name
        #db.session.rollback()
