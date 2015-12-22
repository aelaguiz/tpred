import logging
import scrapy
import scrapy.http as http
import scrapy.spider as spider
import tpred.spider.util as util
import tpred.sites as sites  # NOQA
import tpred.spider.items as items  # NOQA
import tpred.model_util as model_util  # NOQA

log = logging.getLogger(u"tpred")


class MediumSpider(spider.BaseSpider):
    name = "medium"
    allowed_domains = ["medium.com"]

    def start_requests(self):
        yield http.Request("https://medium.com/top-stories", meta={'type': 'page', 'num': 1})

    def parse(self, response):
        response_type = response.meta['type']

        if response_type == 'page':
            for res in self.parse_page(response):
                yield res

    def parse_page(self, response):
        hxs = scrapy.Selector(response)

        entries = hxs.xpath('//div[contains(@class,"postItem")]')
        for thing in entries:
            post_id = thing.xpath('./@data-post-id').extract()[0].strip()

            entry = thing.xpath('.//div[contains(@class, "postArticle-content")]')

            title_node = entry.xpath('.//h3')

            title = " ".join(title_node.xpath('.//text()').extract()).strip()

            href = util.get_url_from_node(response, thing.xpath('.//article[contains(@class, "postArticle")]/a/@href'))

            body_node = entry.xpath('.//div[contains(@class, "section-inner")]/p')
            body = title

            if body_node:
                body = " ".join(body_node.xpath('.//text()').extract()).strip()

            header = thing.xpath('.//div[contains(@class, "postMeta-previewHeader")]')
            author = header.xpath('.//a[@data-action="show-user-card"]/text()').extract()[0].strip()

            votes = 0
            try:
                votes_str = thing.xpath('.//button[@data-action="show-recommends"]/text()').extract()[0].strip().replace(",", "")
                votes = int(votes_str)
            except:
                log.exception(u"Exception parsing {}".format(thing))

            yield items.PostItem(
                site_id=sites.MEDIUM,
                points=votes,
                site_post_id=post_id,
                body=body,
                sn=author,
                url=href)
