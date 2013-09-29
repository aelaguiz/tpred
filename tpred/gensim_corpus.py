import db
import models
import mputil
#import nl_util
import gensim_util
#import model_util
#import sites


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

print "Saving corpus"
gensim_util.save_dict_corp(documents, 'corpus/gensim.dict', 'corpus/gensim.mm')




#gensim_util.build_corpus(documents)

#for post in db.session.query(models.PostModel).all():
    #text = post.rel_body.body

    #sents = nl_util.sentences(text + ".  ")

    #for sent in sents:
        #pos = nl_util.pos_tag(sents)
        #print nl_util.get_pos_subject(pos)
    ##if sn.num_friends is None:
        ##twmention = t.api.GetUser(screen_name=sn.sn)
        ##sn = model_util.get_sn(
            ##sites.TWITTER,
            ##twmention.screen_name,
            ##num_followers=twmention.followers_count,
            ##num_tweets=twmention.statuses_count,
            ##num_friends=twmention.friends_count,
            ##num_favorites=twmention.favourites_count,
            ##verified=twmention.verified)

    ###try:
    ##db.session.commit()
    ###except:
        ###print "Failed adding tweet"
        ###print tweet.id, tweet.created_at, tweet.text, tweet.urls, tweet.user_mentions, tweet.hashtags, tweet.user.screen_name
        ###db.session.rollback()
