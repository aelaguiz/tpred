import tpred.db as db
import sqlalchemy as sqla
import sqlalchemy.sql as sql
import tpred.models as models
import tpred.sites as sites
import tpred.model_util as model_util  # NOQA

#if model_util.did_run("calculate_first_deriv"):
    #sys.exit(1)

#model_util.set_ran("calculate_first_deriv")


def calc_report(period, period_moments):
    n = 2

    moment_res = db.session.query(
        sqla.distinct(models.TopicMomentModel.moment)).order_by(
            models.TopicMomentModel.moment.desc()).limit(n).all()

    # Skip the current moment because it is presumably incomplete
    moment_res = moment_res[1:]

    for m_row in moment_res:
        moment = m_row[0]

        # Get all of the moments leading up to this moment
        moment_res = db.session.query(
            sqla.distinct(models.TopicMomentModel.moment)).order_by(
                models.TopicMomentModel.moment.desc()).filter(
                    models.TopicMomentModel.moment <= moment).limit(period_moments).all()
        moments = [m[0] for m in moment_res]

        for site_id in sites.site_array:
            print "Calculating", site_id, moment, period
            res = db.session.query(models.AvgMomentumPeriodReportModel).filter_by(
                site_id=site_id,
                period=period,
                moment=moment).first()
            if res:
                print "Skipping", site_id, moment, period

            res = db.session.query(models.TopicMomentDerivModel.topic_id, sql.func.avg(models.TopicMomentDerivModel.value)).filter(
                models.TopicMomentDerivModel.site_id == site_id,
                models.TopicMomentDerivModel.moment_to.in_(moments)).group_by(
                    models.TopicMomentDerivModel.topic_id).all()

            print "Got results", len(res)

            for topic_id, avg_val in res:
                m = models.AvgMomentumPeriodReportModel(
                    site_id=site_id,
                    period=period,
                    moment=moment,
                    topic_id=topic_id,
                    value=avg_val
                )

                db.session.add(m)

            print "Committing"
            db.session.commit()


calc_report(1, 4 * 24)
calc_report(2, 4 * 12)
calc_report(3, 4 * 4)
calc_report(4, 4 * 1)
