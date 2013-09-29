import db
import models
import mputil
import gensim_util
import sites


def get_documents_initial(bodies):
    documents = []

    for b in bodies:
        body = b[1]

        words = gensim_util.get_words(body)
        documents.append(words)
        if not words:
            continue

        print words

    return documents

bodies = db.session.query(models.PostModel.id, models.PostBodyModel.body).join(models.PostBodyModel, models.PostModel.body_id == models.PostBodyModel.id).filter(models.PostModel.site_id == sites.HN).all()

print "Tokenizing documents"
documents = mputil.multiproc(bodies, 16, get_documents_initial)

#print "Removing single occurence words from documents"
#documents = mputil.multiproc(documents, 2, gensim_util.remove_singles)

#print "Saving corpus"
#dictionary, corpus = gensim_util.save_dict_corp(documents, 'corpus/gensim.dict', 'corpus/gensim.mm')

print "Loading corpus"
dictionary, corpus = gensim_util.load_dict_corp('corpus/gensim.dict', 'corpus/gensim.mm')

print "Extracting topics"
gensim_util.extract_topics(documents, dictionary, corpus, 10)
