import db
import sqlalchemy as sqla
import pprint  # NOQA
import numpy as np
import models
import model_util
import nltk
import nltk.stem
import nltk.cluster as cluster
import nltk.cluster.util as cutil
import mputil

stemmer_func = nltk.stem.snowball.EnglishStemmer().stem
stopwords = set(nltk.corpus.stopwords.words('english'))


@nltk.decorators.memoize
def normalize_word(word):
    return stemmer_func(word.lower())


def get_words(titles):
    words = set()
    for title in titles:
        for word in title.split():
            words.add(normalize_word(word))
    return list(words)
 

def vectorspaced(title, words):
    title_components = [normalize_word(word) for word in title.split()]
    return np.array([
        word in title_components and not word in stopwords
        for word in words], np.short)


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


def go_cluster(topic_rows):
    print "Clustering", len(topic_rows), "Topics"
    topics = [t[1] for t in topic_rows]

    print "Getting topic words"
    words = get_words(topics)

    print "Vectorizing topics"
    vectorized = [vectorspaced(topic, words) for topic in topics]

    k = len(topics) / 3

    c = cluster.KMeansClusterer(k, cutil.euclidean_distance, avoid_empty_clusters=True)

    print "Clustering into", k
    res = c.cluster(vectorized, assign_clusters=True, trace=False)
    #print res

    print "Clustering done, gathering"
    clusters = {}
    output_clusters = {}

    for (t, tid), cluster_id in zip(topic_rows, res):
        if cluster_id not in output_clusters:
            output_clusters[cluster_id] = []
            clusters[cluster_id] = []

        output_clusters[cluster_id].append(t)
        clusters[cluster_id].append(tid)

    #pprint.pprint(clusters)

    print "Saving clusters"
    save_clusters(output_clusters)

    return []


def cluster_topics():
    num_procs = 1
    per_proc = 1000
    pool = mputil.get_pool(num_procs)

    while True:
        topic_rows = db.session.query(models.TopicModel.id, models.TopicModel.topic).filter_by(clustered=False).order_by(models.TopicModel.id.asc()).limit(num_procs * per_proc).all()

        if len(topic_rows) < per_proc:
            go_cluster(topic_rows)
            break
        else:
            mputil.multiproc(topic_rows, num_procs, go_cluster, pool=pool)


if __name__ == '__main__':
    if not model_util.did_run("alias"):
        model_util.set_ran("alias")
        cluster_topics()
