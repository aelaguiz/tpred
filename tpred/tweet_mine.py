import t
import db
import models
import pprint
import sites

res = db.session.query(models.SnModel.site_sn_id).filter(
    models.SnModel.site_id == sites.TWITTER,
    models.SnModel.site_sn_id != None).order_by(models.SnModel.num_followers.desc()).limit(5000).all()

ids = [str(twid[0]) for twid in res]

it = t.stream.statuses.filter(follow=",".join(ids))

for tweet in it:
    pprint.pprint(tweet)
