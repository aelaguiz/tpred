import scrapy.http as http
import scrapy.spider as spider
import scrapy.selector as selector
import tpred.spider.util as util
import tpred.sites as sites  # NOQA
import tpred.spider.items as items  # NOQA
import re
import tpred.model_util as model_util  # NOQA


points_re = re.compile("(\d+) points?")
post_id_re = re.compile("item\?id=(\d+)")


class RedditSpider(spider.BaseSpider):
    name = "reddit"
    allowed_domains = ["www.reddit.com"]

    def start_requests(self):
        if not model_util.did_site_run(sites.REDDIT):
            model_util.set_site_ran(sites.REDDIT)

            yield http.Request("http://www.reddit.com/new", meta={'type': 'page', 'num': 1})

    def parse(self, response):
        response_type = response.meta['type']

        if response_type == 'page':
            for res in self.parse_page(response):
                yield res

    def parse_page(self, response):
        num = response.meta['num']

        hxs = selector.HtmlXPathSelector(response)

        entries = hxs.select('//div[contains(@class,"thing")]')
        for thing in entries:
            post_id = thing.select('./@data-fullname').extract()[0].strip()
            entry = thing.select('./div[@class="entry unvoted"]')

            href = util.get_url_from_node(response, entry.select('./p[@class="title"]/a/@href'))
            title = entry.select('./p[@class="title"]/a/text()').extract()[0].strip()

            author = entry.select('./p[@class="tagline"]/a/text()').extract()[0].strip()
            votes = 0
            try:
                votes_str = thing.select('./div[@class="midcol unvoted"]/div[@class="score unvoted"]/text()').extract()[0].strip()
                votes = int(votes_str)
            except:
                pass

            yield items.PostItem(
                site_id=sites.REDDIT,
                points=votes,
                site_post_id=post_id,
                body=title,
                sn=author,
                url=href)

        if num < 10:
            next_link = hxs.select('//a[@rel="nofollow next"]/@href')
            if next_link:
                yield http.Request(util.get_url_from_node(response, next_link), meta={'type': 'page', 'num': num + 1})
