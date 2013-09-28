BOT_NAME = 'spider'

SPIDER_MODULES = ['tpred.spider.spiders']
USER_AGENT = 'tpred'

ITEM_PIPELINES = {
    'tpred.spider.database_pipeline.DatabasePipeline': 300
}
