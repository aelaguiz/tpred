import gensim  # NOQA
import gensim.corpora as corpora
import gensim.models as models
from nltk.corpus import stopwords

sw = stopwords.words()


def prep(document):
    return document.lower().split()


def get_words(document):
    return [word for word in prep(document) if word not in sw]


def remove_singles(documents):
    all_tokens = sum(documents, [])
    tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)

    documents = [
        [word for word in text if word not in tokens_once]
        for text in documents]

    return documents


def save_dict_corp(documents, dict_path, corp_path):
    dictionary = corpora.Dictionary(documents)

    dictionary.save(dict_path)

    corpus = [dictionary.doc2bow(text) for text in documents]
    corpora.MmCorpus.serialize(corp_path, corpus)


def load_dict_corp(dict_path, corp_path):
    dictionary = corpora.Dictionary.load(dict_path)
    corpus = corpora.MmCorpus(corp_path)

    return dictionary, corpus


def extract_topics(documents, dictionary, corpus, num_topics):
    tfidf = models.TfidfModel(corpus)
    vec_space = [dictionary.doc2bow(doc) for doc in documents]

    documents_tfidf = tfidf[vec_space]

    lsi = models.LsiModel(documents_tfidf, id2word=dictionary, num_topics=num_topics)
    documents_lsi = lsi[documents_tfidf]

    for topic in enumerate(lsi.show_topics(num_topics)):
        print topic

    #for doc in documents_lsi:
        #print doc
