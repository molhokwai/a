# coding: utf8
# try something like

def index():
    import urllib, urlib2, base64
    import gluon.contrib.simplejson as sj
    
    json_p_n=request.vars.json_p_n
    url=request.vars.url
    exec('json_o = sj.loads(request.vars.%s)'%json_p_n)
    
    args= urllib.urlencode([
            (json_p_n,json_o),
            ('output',request.vars.output)
    ])
    headers={}

    rq = urllib2.Request(url, args, headers)
    return sj.loads(urllib2.urlopen(rq).read())
