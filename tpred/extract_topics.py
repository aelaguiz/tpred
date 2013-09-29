import db
import models
import mputil
import gensim_util


def get_documents_initial(bodies):
    documents = []

    for b in bodies:
        body = b[0]

        words = gensim_util.get_words(body)
        documents.append(words)

    return documents

bodies = db.session.query(models.PostBodyModel.body).all()

print "Tokenizing documents"
documents = mputil.multiproc(bodies, 16, get_documents_initial)

print "Removing single occurence words from documents"
documents = mputil.multiproc(documents, 2, gensim_util.remove_singles)

#print "Saving corpus"
#gensim_util.save_dict_corp(documents, 'corpus/gensim.dict', 'corpus/gensim.mm')

print "Loading corpus"
dictionary, corpus = gensim_util.load_dict_corp('corpus/gensim.dict', 'corpus/gensim.mm')

print "Extracting topics"
gensim_util.extract_topics(documents, dictionary, corpus, 50)
