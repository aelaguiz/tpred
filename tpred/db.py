import os
import logging
import sqlalchemy as sqla
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as decl

log = logging.getLogger(u"tpred")

db_str = os.getenv('DATABASE')

log.debug(u"Database {}".format(db_str))

engine = sqla.create_engine(db_str)
#engine = sqla.create_engine(db_str, echo=True)
Session = orm.sessionmaker(bind=engine)
session = Session()
Base = decl.declarative_base()
