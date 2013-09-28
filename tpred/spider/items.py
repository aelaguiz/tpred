import scrapy.item as item

class PostItem(item.Item):
    site_id = item.Field()
    points = item.Field()
    body = item.Field()
    url = item.Field()
    site_post_id = item.Field()
    sn = item.Field()
