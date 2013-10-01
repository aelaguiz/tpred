SELECT * FROM (
SELECT twitter.id, twitter.topic, twitter.val as twval, hn.val, reddit.val FROM (
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
		site_id=3s
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

ORDER BY cur.twval DESC;