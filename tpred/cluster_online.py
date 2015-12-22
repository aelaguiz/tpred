import logging
import db
import sqlalchemy as sqla
import pprint  # NOQA
import models
import nltk
import nltk.stem
import sklearn.cluster as cluster
import sklearn.feature_extraction.text as text

log = logging.getLogger(u"tpred")

stemmer_func = nltk.stem.snowball.EnglishStemmer().stem
stopwords = set(nltk.corpus.stopwords.words('english'))


def save_clusters(clusters):
    session = db.Session()

    for _, topic_ids in clusters.iteritems():
        topics = session.query(models.TopicModel).filter(models.TopicModel.id.in_(topic_ids)).all()
        topic_cluster = models.TopicClusterModel()
        topic_cluster.rel_topics += topics

        session.add(topic_cluster)

        stmt = sqla.update(models.TopicModel.__table__).where(models.TopicModel.id.in_(topic_ids)).values(clustered=True)
        session.execute(stmt)

    session.commit()


def go_cluster(vectorizer, model, topic_rows):
    log.debug(u"Vectorizing...")
    X = vectorizer.transform([t.topic for t in topic_rows])

    log.debug(X)

    log.debug(u"Clustering...")

    model.fit(X)

    log.debug(u"Gathering")
    clusters = {}
    output_clusters = {}

    for (t, tid), cluster_id in zip(topic_rows, model.labels_):
        if cluster_id == -1:
            continue

        if cluster_id not in output_clusters:
            output_clusters[cluster_id] = []
            clusters[cluster_id] = []

        output_clusters[cluster_id].append(t)
        clusters[cluster_id].append(tid)

    pprint.pprint(clusters)

    log.debug(u"Saving")
    save_clusters(output_clusters)


def cluster_topics():
    #model = cluster.Birch(
        #branching_factor=2,
        #threshold=0.002 # Lower = more clusters, higher = fewer clusters
    #)

    #model = cluster.KMeans(
        #branching_factor=10,
        #threshold=0.1 # Lower = more clusters, higher = fewer clusters
    #)

    model = cluster.DBSCAN(
        min_samples=2,
        eps=0.2
    )

    #model = cluster.AffinityPropagation(
    #)

    vectorizer = text.HashingVectorizer(
        analyzer='char_wb',         # The feature is made of words not characters
        norm='l2',               # Normalize the words
        lowercase=True,          # Converts everything to lowercase
        stop_words=stopwords
    )

    num_samples = 40000
    offset = 0

    while True:
        log.debug(u"Loading topics...")
        topic_rows = db.session.query(models.TopicModel.id, models.TopicModel.topic).filter_by(clustered=False).order_by(models.TopicModel.id.asc()).limit(num_samples).offset(offset).all()
        log.debug(u"Loaded {} topics".format(len(topic_rows)))

        offset += num_samples

        go_cluster(vectorizer, model, topic_rows)


if __name__ == '__main__':
    db.session.execute(models.topic_cluster_map.delete())
    db.session.commit()
    db.session.query(models.TopicClusterModel).delete()
    db.session.commit()

    try:
        cluster_topics()
    except:
        log.exception(u"Failed")
