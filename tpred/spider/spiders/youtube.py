import logging
import scrapy
import scrapy.http as http
import scrapy.spider as spider
import tpred.spider.util as util
import tpred.sites as sites  # NOQA
import tpred.spider.items as items  # NOQA
import re
import tpred.model_util as model_util  # NOQA

log = logging.getLogger(u"tpred")

views_re = re.compile("([,0-9]+) views?")


class YoutubeSpider(spider.BaseSpider):
    name = "youtube"
    allowed_domains = ["youtube.com"]

    def start_requests(self):
        yield http.Request("https://www.youtube.com/feed/trending", meta={'type': 'page', 'num': 1})

    def parse(self, response):
        response_type = response.meta['type']

        if response_type == 'page':
            for res in self.parse_page(response):
                yield res

    def parse_page(self, response):
        hxs = scrapy.Selector(response)
        log.debug(hxs)

        entries = hxs.xpath('//li[contains(@class,"expanded-shelf-content-item-wrapper")]')
        log.debug(entries)
        for thing in entries:
            log.debug(thing)
            item_node = thing.xpath('./div[contains(@class, "expanded-shelf-content-item")]')

            post_id = item_node.xpath('./div[contains(@class, "yt-lockup-video")]/@data-context-item-id').extract()[0].strip()

            title_link = item_node.xpath('.//div[contains(@class, "yt-lockup-content")]/h3[contains(@class, "yt-lockup-title")]/a')

            title = title_link.xpath('./text()').extract()[0].strip()

            href = util.get_url_from_node(response, title_link.xpath('./@href'))

            body = " ".join(item_node.xpath('.//div[contains(@class, "yt-lockup-content")]/div[contains(@class, "yt-lockup-description")]//text()').extract()).strip()

            author = item_node.xpath('.//div[contains(@class, "yt-lockup-content")]/div[contains(@class, "yt-lockup-byline")]/a/text()').extract()[0].strip()

            views = 0
            try:
                views_str = item_node.xpath('.//div[contains(@class, "yt-lockup-content")]//ul[contains(@class, "yt-lockup-meta-info")]/li/text()').extract()[1].strip()
                matches = views_re.match(views_str)
                views = int(matches.group(1).replace(",", ""))
            except:
                log.exception(u"Exception parsing {}".format(thing))

            yield items.PostItem(
                site_id=sites.YOUTUBE,
                points=views,
                site_post_id=post_id,
                body=body,
                sn=author,
                url=href)
