SELECT a.topic, b.twitter_value - a.twitter_value as twitter_delta, b.hn_value - a.hn_value as hn_delta, b.reddit_value - a.reddit_value as reddit_delta, (b.twitter_value - a.twitter_value)+(b.hn_value - a.hn_value)+(b.reddit_value - a.reddit_value) FROM
	(SELECT twitter.moment, twitter.topic, twitter.value as twitter_value, hn.value as hn_value, reddit.value as reddit_value, twitter.value::float / hn.value::float as ratio, twitter.value::float / reddit.value::float as ratio
	FROM
		(SELECT * FROM topic JOIN topic_moment tm ON topic.id=tm.topic_id AND value > 1 WHERE site_id=1 ORDER BY value DESC) as twitter
	LEFT JOIN
		(SELECT * FROM topic JOIN topic_moment tm ON topic.id=tm.topic_id WHERE site_id=2 ORDER BY value DESC) as hn
	ON twitter.topic_id=hn.topic_id AND twitter.moment=hn.moment
	LEFT JOIN
		(SELECT * FROM topic JOIN topic_moment tm ON topic.id=tm.topic_id WHERE site_id=3 ORDER BY value DESC) as reddit
	ON twitter.topic_id=reddit.topic_id AND twitter.moment=reddit.moment

	WHERE twitter.num_words>1 

	AND twitter.moment = (
		SELECT MAX(moment) FROM topic_moment)
	
	ORDER BY twitter_value DESC) as a
JOIN
	(SELECT twitter.moment, twitter.topic, twitter.value as twitter_value, hn.value as hn_value, reddit.value as reddit_value, twitter.value::float / hn.value::float as ratio, twitter.value::float / reddit.value::float as ratio
	FROM
		(SELECT * FROM topic JOIN topic_moment tm ON topic.id=tm.topic_id AND value > 1 WHERE site_id=1 ORDER BY value DESC) as twitter
	LEFT JOIN
		(SELECT * FROM topic JOIN topic_moment tm ON topic.id=tm.topic_id WHERE site_id=2 ORDER BY value DESC) as hn
	ON twitter.topic_id=hn.topic_id AND twitter.moment=hn.moment
	LEFT JOIN
		(SELECT * FROM topic JOIN topic_moment tm ON topic.id=tm.topic_id WHERE site_id=3 ORDER BY value DESC) as reddit
	ON twitter.topic_id=reddit.topic_id AND twitter.moment=reddit.moment

	WHERE twitter.num_words>1 

	AND twitter.moment = (
		SELECT MAX(moment)-1 FROM topic_moment)
	
	ORDER BY twitter_value DESC) as b

ON a.topic=b.topic ORDER BY (b.twitter_value - a.twitter_value)+(b.hn_value - a.hn_value)+(b.reddit_value - a.reddit_value) DESC;