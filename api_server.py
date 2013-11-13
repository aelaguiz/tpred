from flask import Flask
from flask import Response
from flask import redirect
import json
import tpred.reports.trending_posts as tp

app = Flask(__name__)


def htmlResponse(p_htmlText):
    r = app.make_response(p_htmlText)
    r.content_type = "text/html"
    return r


@app.route('/test')
def testHandler():
    return htmlResponse("test success")


@app.route('/report/<sn>/<mins>')
def generateReport(sn, mins):
#    screenname = sn
#    minutes = mins
    print "getting list"
    try:
        data = list(tp.run_report(mins, False))[:12]
    except Exception, e:
        print e
    print "got list"
#    if data == None:
#        return htmlResponse("None")
#    if len(data) > 0:
    return Response(json.dumps(data), mimetype='application/json')
#    else:
#        return htmlResponse("nothing")


app.run(host='0.0.0.0')
