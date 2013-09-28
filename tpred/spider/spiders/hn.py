import scrapy.spider as spider


class HnSpider(spider.BaseSpider):
    name = "hn"
    allowed_domains = "news.ycombinator.com"

    def start_requests(self):
        print "Starting requests"
        return []
