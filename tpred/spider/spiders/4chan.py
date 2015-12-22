import logging
import scrapy
import HTMLParser
import json
import scrapy.http as http
import scrapy.spider as spider
import tpred.sites as sites  # NOQA
import tpred.spider.items as items  # NOQA
import re
import tpred.model_util as model_util  # NOQA
import tpred.html_util as html_util

log = logging.getLogger(u"tpred")

views_re = re.compile("([,0-9]+) views?")

js_re = re.compile("\s*PostList\.set\('(\w+)', ({.*})\);$")

parser = HTMLParser.HTMLParser()


class FourchanSpider(spider.BaseSpider):
    name = "4chan"
    allowed_domains = ["4chan.org"]

    def start_requests(self):
        yield http.Request("http://www.4chan.org", meta={'type': 'page', 'num': 1})

    def parse(self, response):
        response_type = response.meta['type']

        if response_type == 'page':
            for res in self.parse_page(response):
                yield res

    def parse_page(self, response):
        hxs = scrapy.Selector(response)
        log.debug(hxs)

        scripts = hxs.xpath('//script[@type="text/javascript"]')
        for script in scripts:
            js = " ".join(script.xpath('./text()').extract())

            matches = js_re.match(js)

            if matches:
                json_data = json.loads(matches.group(2))

                for post_id, post_data in json_data.iteritems():
                    body = re.sub(
                        ">>\d+",
                        "",
                        html_util.strip_tags(
                            parser.unescape(
                                post_data['com']
                            )
                        )
                    )
                    #log.debug(post_data)

                    if 'resto' in post_data and int(post_data['resto']) != 0:
                        url = u"http://boards.4chan.org/{}/thread/{}#p{}".format(post_data['board'], post_data['resto'], post_data['no'])
                    else:
                        url = u"http://boards.4chan.org/{}/thread/{}".format(post_data['board'], post_data['no'])

                    yield items.PostItem(
                        site_id=sites.FOURCHAN,
                        points=int(post_data['replies']) if post_data['replies'] else 0,
                        site_post_id=post_id,
                        body=body,
                        sn=post_data['name'],
                        url=url
                    )
