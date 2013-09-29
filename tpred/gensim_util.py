import gensim  # NOQA
import gensim.corpora as corpora
from nltk.corpus import stopwords

sw = stopwords.words()
print len(sw)


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
