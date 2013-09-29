import db
import models
import mputil
import sites
import nl_util


def prep_bodies(bodies):
    documents = []

    for b in bodies:
        body = b[1]

        documents.append([s.lower() for s in nl_util.prep(body)])

    return documents

bodies = db.session.query(models.PostModel.id, models.PostBodyModel.body).join(models.PostBodyModel, models.PostModel.body_id == models.PostBodyModel.id).filter(models.PostModel.site_id == sites.HN).all()

print "Tokenizing documents"

docs = mputil.multiproc(bodies, 1, prep_bodies)
words = [item for sublist in docs for item in sublist]

print words

common = list(nl_util.common_words(words, 1000))
bigrams = list(nl_util.bigrams(words, 1000))
trigrams = list(nl_util.trigrams(words, 1000))


##print "Removing single occurence words from documents"
##documents = mputil.multiproc(documents, 2, gensim_util.remove_singles)

##print "Saving corpus"
##dictionary, corpus = gensim_util.save_dict_corp(documents, 'corpus/gensim.dict', 'corpus/gensim.mm')

#print "Loading corpus"
#dictionary, corpus = gensim_util.load_dict_corp('corpus/gensim.dict', 'corpus/gensim.mm')

#print "Extracting topics"
#gensim_util.extract_topics(documents, dictionary, corpus, 10)
