import json
import urllib2
import base64

DUCKSBOARD_API_KEY = "BHXaRwl3qEBVQAgHWFgQ1woxlcOPa9feJ4PbV9cs1WTkW2EO87"


def send_to_ducksboard(id, msg):
    """
    Send image to ducksboard custom image widget.
    """
    endpoint = "https://push.ducksboard.com/v/{}".format(id)

    #log.debug("Sending to ducksboard {} {}".format(id, msg))
    print endpoint, msg

    request = urllib2.Request(endpoint)
    auth = base64.encodestring('%s:x' % DUCKSBOARD_API_KEY)
    auth = auth.replace('\n', '')
    request.add_header('Authorization', 'Basic %s' % auth)
    urllib2.urlopen(request, json.dumps(msg))


def leaderboard(rows, chart_id):
    upload = []

    for row in rows:
        data = {}

        data['name'] = row[0]
        data['values'] = list(row[1:])

        upload.append(data)

    send_to_ducksboard(chart_id, {'value': {'board': upload}})


def timeline(rows, chart_id):
    for row in reversed(rows):
        send_to_ducksboard(chart_id, {'value': row})
