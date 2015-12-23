BOT_NAME = 'spider'

SPIDER_MODULES = ['tpred.spider.spiders']
USER_AGENT = 'tpred2'

ITEM_PIPELINES = {
    #'tpred.spider.database_pipeline.DatabasePipeline': 300
    'tpred.spider.csv_pipeline.CSVPipeline': 300
}

DOWNLOAD_DELAY = 0.5

OUTPUT_DIRECTORY = 'spider_data'
