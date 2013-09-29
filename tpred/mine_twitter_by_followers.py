import t
import tweet_mine

res = t.api.friends.ids(screen_name='amirpc')['ids']

ids = [str(twid) for twid in res]

it = t.stream.statuses.filter(follow=",".join(ids))
tweet_mine.mine(it)
