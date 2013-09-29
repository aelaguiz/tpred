import t
import tweet_mine

it = t.stream.statuses.sample()
tweet_mine.mine(it)
