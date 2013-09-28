import sqlalchemy as sqla
import sqlalchemy.orm as orm
import datetime
import db


post_hashtag_map = sqla.Table(
    'post_hashtag_map', db.Base.metadata,
    sqla.Column('post_id', sqla.BigInteger, sqla.ForeignKey('post.id')),
    sqla.Column('hashtag_id', sqla.BigInteger, sqla.ForeignKey('hashtag.id'))
)


post_url_map = sqla.Table(
    'post_url_map', db.Base.metadata,
    sqla.Column('post_id', sqla.BigInteger, sqla.ForeignKey('post.id')),
    sqla.Column('url_id', sqla.BigInteger, sqla.ForeignKey('url.id'))
)


post_mention_map = sqla.Table(
    'post_mention_map', db.Base.metadata,
    sqla.Column('post_id', sqla.BigInteger, sqla.ForeignKey('post.id')),
    sqla.Column('sn_id', sqla.BigInteger, sqla.ForeignKey('sn.id'))
)


class SnModel(db.Base):
    __tablename__ = "sn"

    id = sqla.Column(sqla.BigInteger, primary_key=True, nullable=False)
    sn = sqla.Column(sqla.String, nullable=False)
    num_followers = sqla.Column(sqla.Integer)
    num_friends = sqla.Column(sqla.Integer)
    num_favorites = sqla.Column(sqla.Integer)
    num_posts = sqla.Column(sqla.Integer)
    verified = sqla.Column(sqla.Boolean)
    last_check = sqla.Column(sqla.DateTime)

    @property
    def needs_check(self):
        if self.num_followers < 100000:
            return False

        # If the sn has never been checked
        if self.last_check is None:
            return True
        # Or it has been longer than 15 minutes
        else:
            diff = datetime.datetime.now() - self.last_check
            if diff.total_seconds() > 900:
                return True

        return False


class UrlModel(db.Base):
    __tablename__ = "url"

    id = sqla.Column(sqla.BigInteger, primary_key=True, nullable=False)
    url = sqla.Column(sqla.String, nullable=False)


class HashtagModel(db.Base):
    __tablename__ = "hashtag"

    id = sqla.Column(sqla.BigInteger, primary_key=True, nullable=False)
    hashtag = sqla.Column(sqla.String, nullable=False)


class PostModel(db.Base):
    __tablename__ = "post"

    id = sqla.Column(sqla.BigInteger, primary_key=True, nullable=False)
    sn_id = sqla.Column(sqla.BigInteger, sqla.ForeignKey(SnModel.id), nullable=False)
    site_post_id = sqla.Column(sqla.BigInteger, nullable=False)
    created_at = sqla.Column(sqla.DateTime, nullable=False)
    text = sqla.Column(sqla.String, nullable=False)

    rel_mentions = orm.relationship(SnModel, secondary=post_mention_map)
    rel_hashtags = orm.relationship(HashtagModel, secondary=post_hashtag_map)
    rel_urls = orm.relationship(UrlModel, secondary=post_url_map)
