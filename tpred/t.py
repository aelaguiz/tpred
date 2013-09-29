import twitter
import db
import model_util

twitter.twitter_globals.POST_ACTIONS.append('filter')

oauth = twitter.OAuth(
    '18362611-BIh0HMnGSFQ3wkDtp8lKu4lxPn60zSPppGIUUL5I6',
    'YW5bzat9hFb3eLxL5DZ5MSR0Z6qpnOe8wWQIeRIGUs',
    'nlH3pUB6J6dRB31YOqVlyQ',
    'ozh7DyDEZql2w2NW4Qt76UgB9oXpHKOABg24jT3c'
)

api = twitter.Twitter(
    auth=oauth
)

stream = twitter.TwitterStream(auth=oauth)
