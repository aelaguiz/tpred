import sqlalchemy as sqla
import sqlalchemy.orm as orm
import db


tweet_hashtag_map = sqla.Table(
    'tweet_hashtag_map', db.Base.metadata,
    sqla.Column('tweet_id', sqla.BigInteger, sqla.ForeignKey('tweet.id')),
    sqla.Column('hashtag_id', sqla.BigInteger, sqla.ForeignKey('hashtag.id'))
)


tweet_url_map = sqla.Table(
    'tweet_url_map', db.Base.metadata,
    sqla.Column('tweet_id', sqla.BigInteger, sqla.ForeignKey('tweet.id')),
    sqla.Column('url_id', sqla.BigInteger, sqla.ForeignKey('url.id'))
)


tweet_mention_map = sqla.Table(
    'tweet_mention_map', db.Base.metadata,
    sqla.Column('tweet_id', sqla.BigInteger, sqla.ForeignKey('tweet.id')),
    sqla.Column('sn_id', sqla.BigInteger, sqla.ForeignKey('sn.id'))
)


class SnModel(db.Base):
    __tablename__ = "sn"

    id = sqla.Column(sqla.BigInteger, primary_key=True, nullable=False)
    sn = sqla.Column(sqla.String, nullable=False)


class UrlModel(db.Base):
    __tablename__ = "url"

    id = sqla.Column(sqla.BigInteger, primary_key=True, nullable=False)
    url = sqla.Column(sqla.String, nullable=False)


class HashtagModel(db.Base):
    __tablename__ = "hashtag"

    id = sqla.Column(sqla.BigInteger, primary_key=True, nullable=False)
    hashtag = sqla.Column(sqla.String, nullable=False)


class TweetModel(db.Base):
    __tablename__ = "tweet"

    id = sqla.Column(sqla.BigInteger, primary_key=True, nullable=False)
    sn_id = sqla.Column(sqla.BigInteger, sqla.ForeignKey(SnModel.id), nullable=False)
    twitter_id = sqla.Column(sqla.BigInteger, nullable=False)
    created_at = sqla.Column(sqla.DateTime, nullable=False)
    text = sqla.Column(sqla.String, nullable=False)

    rel_mentions = orm.relationship(SnModel, secondary=tweet_mention_map)
    rel_hashtags = orm.relationship(HashtagModel, secondary=tweet_hashtag_map)
    rel_urls = orm.relationship(UrlModel, secondary=tweet_url_map)
