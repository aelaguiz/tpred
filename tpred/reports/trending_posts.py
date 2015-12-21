import tpred.db as db


def run_report(minutes, filter_links=False):
    print "Runing tweet report for", minutes, "minutes with link filter:", filter_links

    q = """
    SELECT original.site_id, original.body_id, COUNT(*) as num_reposts, original.site_post_id, original.body, original.sn, MAX(original.diff), original.url, original.pic_url
    FROM (
            SELECT p.site_id, pb.id as body_id, pb.body,sn.sn, p.site_post_id, CURRENT_TIMESTAMP-created_at as diff, url, sn.pic_url FROM post p JOIN post_body pb on p.body_id=pb.id
            JOIN sn ON p.sn_id=sn.id
            LEFT JOIN post_url_map pum ON p.id=pum.post_id
                LEFT JOIN url ON pum.url_id=url.id
            WHERE repost=false AND created_at > (CURRENT_TIMESTAMP - INTERVAL '{} minute')
            {}
            ) original

    JOIN

    post p ON p.site_id=original.site_id AND original.body_id=p.body_id

    WHERE p.repost=true

    GROUP BY original.body_id, original.site_id, original.body, original.sn, original.site_post_id, original.url, original.pic_url

    ORDER BY num_reposts DESC;""".format(
        minutes, "AND body NOT LIKE '%http%'" if filter_links else "")

    res = db.session.execute(q)
    db.session.commit()

    used = set()
    for site_id, body_id, num_reposts, site_post_id, body, sn, diff, url, pic_url in res:
        if '#forbes30' in body.lower():
            continue

        if body_id in used:
            continue
        if num_reposts <= 1:
            continue

        used.add(body_id)

        if url is None:
            url = ""

        if site_id == 1:
            url = 'https://twitter.com/' + sn + '/status/' + site_post_id

        row = {
            u'title': u"{} - {} - {} - {}".format(sn, num_reposts, diff, site_id),
            u'image': pic_url,
            u'link': url,
            u'content': body
        }

        print row

        yield row
        #yield "{}\n{}".format(title, body)
