import logging
import scrapy
import HTMLParser
import json
import scrapy.http as http
import scrapy.spider as spider
import tpred.sites as sites  # NOQA
import tpred.spider.items as items  # NOQA
import tpred.spider.util as util
import tpred.model_util as model_util  # NOQA

log = logging.getLogger(u"tpred")

parser = HTMLParser.HTMLParser()


class TumblrSpider(spider.BaseSpider):
    name = "tumblr"
    allowed_domains = ["tumblr.com"]

    def start_requests(self):
        #yield http.Request("http://www.4chan.org", meta={'type': 'page', 'num': 1})

        for i in range(1):
            yield http.Request(
                "https://www.tumblr.com/svc/discover/posts?offset={}&askingForPage={}&limit={}&type=trending&with_form_key=true".format(
                    i * 20, i + 1, 20),
                headers={
                    "x-requested-with": "XMLHttpRequest"
                },
                meta={'type': 'page', 'num': 1}
            )

    def parse(self, response):
        response_type = response.meta['type']

        if response_type == 'page':
            for res in self.parse_page(response):
                yield res

    def parse_page(self, response):
        try:
            data = json.loads(response.body)

            discovery_posts = data['response']['DiscoveryPosts']
            posts = discovery_posts['posts']

            for post in posts:
                hxs = scrapy.Selector(text=post)

                entry = hxs.xpath('//article')

                post_id = entry.xpath('./@data-id').extract()[0].strip()
                #log.debug(post_id)
                author = entry.xpath('./@data-tumblelog-name').extract()[0].strip()
                #log.debug(author)

                header = entry.xpath('.//header')
                href = util.get_url_from_node(response, header.xpath('./div/a/@href'))
                #log.debug(href)

                tags = entry.xpath('.//section[@class="post_tags"]/div/a[@class="post_tag"]/@data-tag').extract()
                #log.debug(tags)

                body = entry.xpath('.//div[@class="post_body"]//text()').extract()
                #log.debug(body)

                body += tags

                body_text = " ".join(parser.unescape(body))
                #log.debug(body_text)

                votes = int(entry.xpath('.//div[@class="post_notes_inner"]//span[@class="note_link_current"]/@data-count').extract()[0].strip())
                #log.debug(votes)

                yield items.PostItem(
                    site_id=sites.TUMBLR,
                    points=votes,
                    site_post_id=post_id,
                    body=body_text,
                    sn=author,
                    url=href
                )
        except:
            log.exception(u"Failed")
