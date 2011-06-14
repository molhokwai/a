# coding: utf8

def index():
    import urllib, base64
    exec('from applications.%s.modules import urllib2' % this_app)
    import gluon.contrib.simplejson as sj

    url=request.vars.url
    params = []
    for k in request.vars:
        if k=='json_p_n':
            json_p_n=request.vars.json_p_n
            json_o = eval('request.vars.%s'%json_p_n)
            params.append((json_p_n, json_o))
        else:
            params.append((k, request.vars[k]))

    args= urllib.urlencode(params)
    headers={}

    rq = urllib2.Request(url, args, headers)
    return response.json(sj.loads(urllib2.urlopen(rq).read()))
