import logging
import StringIO
import os
import time
import tpred.unicode_csv as unicode_csv

log = logging.getLogger(u"tpred")


class CSVPipeline(object):
    def __init__(self):
        self.files = {}

    def get_file(self, spider):
        if spider.name in self.files:
            return self.files[spider.name]

        filename = os.path.join(spider.settings['OUTPUT_DIRECTORY'], time.strftime("{}-%H%M%S-%h%d%Y.csv".format(spider.name)))

        log.debug(u"Opening output file {}".format(filename))

        self.files[spider.name] = open(filename, "wb")

        return self.files[spider.name]

    def process_item(self, item, spider):
        try:
            f = self.get_file(spider)

            of = StringIO.StringIO()
            writer = unicode_csv.UnicodeWriter(of)
            writer.writerow([unicode(a) for a in [int(time.time()), item['site_id'], item['points'], item['body'], item['url'], item['site_post_id'], item['sn']]])

            data = of.getvalue()

            f.write(data)
        except:
            log.exception(u"Failed")

        return item
