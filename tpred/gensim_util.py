import string
import corpus_util
import gensim  # NOQA
import gensim.corpora as corpora
import gensim.models as models
from nltk.corpus import stopwords

sw = stopwords.words()
sw2 = set(corpus_util.load_words("corpus/stopwords.txt"))


def prep(document):
    document = document.lower().split()

    document = ["".join(l for l in word if l not in string.punctuation) for word in document]

    return document


def get_words(document):
    return [word for word in prep(document) if word and word not in sw and word not in sw2]


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

    return dictionary, corpus


def load_dict_corp(dict_path, corp_path):
    dictionary = corpora.Dictionary.load(dict_path)
    corpus = corpora.MmCorpus(corp_path)

    return dictionary, corpus


def extract_topics(documents, dictionary, corpus, num_topics):
    tfidf = models.TfidfModel(corpus)
    vec_space = [dictionary.doc2bow(doc) for doc in documents]

    documents_tfidf = tfidf[vec_space]

    lsi = models.LsiModel(documents_tfidf, id2word=dictionary, num_topics=num_topics)
    documents_lsi = lsi[documents_tfidf]  # NOQA

    for topic in enumerate(lsi.show_topics(num_topics)):
        print topic
    
    topics = dict(enumerate(lsi.show_topics(num_topics)))

    for index, ranks in enumerate(documents_lsi):
        srank = sorted(ranks, key=lambda x: abs(x[1]), reverse=True)

        if srank:
            print documents[index], topics[srank[0][0]]
