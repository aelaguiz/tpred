import logging
import scrapy.http as http
import scrapy.spider as spider
import scrapy.selector as selector
import tpred.spider.util as util
import tpred.sites as sites
import tpred.spider.items as items
import re
import tpred.model_util as model_util

log = logging.getLogger(u"tpred")

points_re = re.compile("(\d+) points?")
post_id_re = re.compile("item\?id=(\d+)")


class HnSpider(spider.BaseSpider):
    name = "hn"
    allowed_domains = ["news.ycombinator.com"]

    def start_requests(self):
        if not model_util.did_site_run(sites.HN):
            model_util.set_site_ran(sites.HN)

            yield http.Request("https://news.ycombinator.com/newest", meta={'type': 'page', 'num': 1})
        else:
            log.debug(u"Not running HN, too soon")

    def parse(self, response):
        response_type = response.meta['type']

        if response_type == 'page':
            for res in self.parse_page(response):
                yield res

    def parse_page(self, response):
        num = response.meta['num']

        hxs = selector.HtmlXPathSelector(response)

        links = hxs.xpath('//td[@class="title"]/a')
        subtext = hxs.xpath('//td[@class="subtext"]')

        for link, td in zip(links, subtext)[:-1]:
            sn = td.xpath('./a/text()')[0].extract()

            points_text = td.xpath('./span/text()')[0].extract()
            items_href = td.xpath('./a/@href')[1].extract()
            m = points_re.match(points_text)
            points = int(m.group(1))

            m = post_id_re.match(items_href)
            post_id = int(m.group(1))

            post = link.xpath('./text()')[0].extract()
            content_link = util.get_url_from_node(response, link.xpath('./@href'))

            yield items.PostItem(
                site_id=sites.HN,
                points=points,
                site_post_id=post_id,
                body=post,
                sn=sn,
                url=content_link)

        if num < 5:
            more_link = links[-1]
            more_url = util.get_url_from_node(response, more_link.xpath('./@href'))

            yield http.Request(more_url, meta={'type': 'page', 'num': num + 1})
