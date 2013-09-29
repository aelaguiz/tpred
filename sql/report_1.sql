SELECT twitter.moment, twitter.topic, twitter.value as twitter_value, hn.value as hn_value, twitter.value::float / hn.value::float as ratio FROM
	(SELECT * FROM topic JOIN topic_moment tm ON topic.id=tm.topic_id WHERE site_id=1 ORDER BY value DESC) as twitter
JOIN
	(SELECT * FROM topic JOIN topic_moment tm ON topic.id=tm.topic_id WHERE site_id=2 ORDER BY value DESC) as hn
ON twitter.topic_id=hn.topic_id WHERE twitter.num_words=2 AND twitter.moment=hn.moment ORDER BY ratio DESC;