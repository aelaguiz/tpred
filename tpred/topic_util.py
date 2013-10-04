import nl_util
import db
import model_util


def update_topics(site_id, body, set_value=None):
    text = body.body

    words = [s.lower() for s in nl_util.prep(text)]

    common = list(nl_util.common_words(words, 1000))
    bigrams = list(nl_util.bigrams(words, 1000))
    trigrams = list(nl_util.trigrams(words, 1000))

    add_topics(site_id, body, common, set_value)
    add_topics(site_id, body, bigrams, set_value)
    add_topics(site_id, body, trigrams, set_value)


def add_topics(site_id, body, topics, set_value=None):
    for topic_word in topics:
        if isinstance(topic_word, tuple):
            topic_word = " ".join(topic_word)

        topic = get_topic(topic_word)

        body.rel_topics.append(topic)

        moment = model_util.get_topic_moment(site_id, topic)

        if set_value:
            moment.value = set_value
        else:
            moment.value += 1

        #print topic_word, moment.moment, moment.value

        db.session.add(moment)


def get_topic(topic_word):
    return model_util.get_topic(topic_word)
