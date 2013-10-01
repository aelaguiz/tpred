SELECT * FROM (
SELECT id, topic, twval, hnval, redditval FROM (
	SELECT twitter.id, twitter.topic, twitter.val as twval, hn.val as hnval, reddit.val as redditval FROM (
		SELECT AVG(value) as val, t.id, t.topic 
		FROM topic_moment_deriv tmd 
		JOIN topic t on tmd.topic_id=t.id 
		WHERE moment_to IN (
			SELECT DISTINCT moment FROM topic_moment ORDER BY moment DESC LIMIT 8 OFFSET 1) AND 
			site_id=1 
		GROUP BY t.id 
		ORDER BY avg(value) desc) as twitter
	LEFT JOIN
		(SELECT AVG(value) as val, t.topic 
		FROM topic_moment_deriv tmd 
		JOIN topic t on tmd.topic_id=t.id 
		WHERE moment_to IN (
			SELECT DISTINCT moment FROM topic_moment ORDER BY moment DESC LIMIT 8 OFFSET 1) AND 
			site_id=2
		GROUP BY t.topic 
		ORDER BY avg(value) desc) as hn
	ON twitter.topic=hn.topic

	LEFT JOIN
		(SELECT AVG(value) as val, t.topic 
		FROM topic_moment_deriv tmd 
		JOIN topic t on tmd.topic_id=t.id 
		WHERE moment_to IN (
			SELECT DISTINCT moment FROM topic_moment ORDER BY moment DESC LIMIT 8 OFFSET 1) AND 
			site_id=3
		GROUP BY t.topic 
		ORDER BY avg(value) desc) as reddit
	ON twitter.topic=reddit.topic) as cur

	WHERE cur.id NOT in 
	(SELECT twitter.id FROM (
		SELECT AVG(value) as val, t.id, t.topic 
		FROM topic_moment_deriv tmd 
		JOIN topic t on tmd.topic_id=t.id 
		WHERE moment_to IN (
			SELECT DISTINCT moment FROM topic_moment ORDER BY moment DESC LIMIT 8 OFFSET 2) AND 
			site_id=1 
		GROUP BY t.id 
		ORDER BY avg(value) desc) as twitter
	LEFT JOIN
		(SELECT AVG(value) as val, t.topic 
		FROM topic_moment_deriv tmd 
		JOIN topic t on tmd.topic_id=t.id 
		WHERE moment_to IN (
			SELECT DISTINCT moment FROM topic_moment ORDER BY moment DESC LIMIT 8 OFFSET 2) AND 
			site_id=2
		GROUP BY t.topic 
		ORDER BY avg(value) desc) as hn
	ON twitter.topic=hn.topic

	LEFT JOIN
		(SELECT AVG(value) as val, t.topic 
		FROM topic_moment_deriv tmd 
		JOIN topic t on tmd.topic_id=t.id 
		WHERE moment_to IN (
			SELECT DISTINCT moment FROM topic_moment ORDER BY moment DESC LIMIT 8 OFFSET 2) AND 
			site_id=3
		GROUP BY t.topic 
		ORDER BY avg(value) desc) as reddit
	ON twitter.topic=reddit.topic) 
) as a
JOIN

(SELECT COUNT(*), body, topic_id FROM post p JOIN post_body b ON p.body_id=b.id JOIN body_topic_map btm ON b.id=btm.body_id GROUP BY topic_id, body ORDER BY COUNT(*) desc) as tweets

ON a.id=tweets.topic_id

ORDER BY a.twval DESC;
