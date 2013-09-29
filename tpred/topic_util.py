import nl_util
import db
import model_util


def update_topics(body):
    text = body.body

    words = [s.lower() for s in nl_util.prep(text)]

    common = list(nl_util.common_words(words, 1000))
    bigrams = list(nl_util.bigrams(words, 1000))
    trigrams = list(nl_util.trigrams(words, 1000))

    add_topics(body, common)
    add_topics(body, bigrams)
    add_topics(body, trigrams)


def add_topics(body, topics):
    for topic_word in topics:
        if isinstance(topic_word, tuple):
            topic_word = " ".join(topic_word)

        topic = get_topic(topic_word)

        body.rel_topics.append(topic)

        moment = model_util.get_topic_moment(topic)
        moment.value += 1

        print topic_word, moment.moment, moment.value

        db.session.add(moment)


def get_topic(topic_word):
    return model_util.get_topic(topic_word)
