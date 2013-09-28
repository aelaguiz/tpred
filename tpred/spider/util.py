import urlparse


def get_url_from_node(response, node, base=None):
    href = node.extract()[0].strip()
    o = urlparse.urlparse(response.url)
    if 'http' not in href:
        if not base:
            href = urlparse.urljoin(o.scheme + "://" + o.netloc + o.path, href)
        else:
            href = urlparse.urljoin(base, href)

    return href
