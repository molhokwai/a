# coding: utf8
def index():
    area = request.args[0]
    return dict(form=crud(), edit_title=area)
    

@auth.requires_login()
def create():
    try:
        _id = db.json.insert(
            name = request.vars.name,
            data = request.vars.data
        )
        return dict(_id = _id)
    except Exception, ex:
        return str(ex)
            

@auth.requires_login()
def read():
    try:
        _json = db(db.json.name == request.vars.name).select()[0].data
        return dict(_json = _json)
    except Exception, ex:
        return str(ex)

def fetch():
    from gluon.tools import fetch
    return fetch(request.vars.url, headers = {'Cache-Control' : request.vars.cache_control, 'Pragma' : request.vars.pragma})
