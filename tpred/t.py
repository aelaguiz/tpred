import twitter
import db
import model_util

api = twitter.Api(
    consumer_key='nlH3pUB6J6dRB31YOqVlyQ',
    consumer_secret='ozh7DyDEZql2w2NW4Qt76UgB9oXpHKOABg24jT3c',
    access_token_key='18362611-BIh0HMnGSFQ3wkDtp8lKu4lxPn60zSPppGIUUL5I6',
    access_token_secret='YW5bzat9hFb3eLxL5DZ5MSR0Z6qpnOe8wWQIeRIGUs')

print api.VerifyCredentials()
