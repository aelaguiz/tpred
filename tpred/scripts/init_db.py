import tpred.model_util as model_util  # NOQA
import tpred.db as db

db.Base.metadata.create_all(db.engine)
