# coding: utf8

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
