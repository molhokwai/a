# coding: utf8
###################################
## CONTROLLER INITIALIZATION
###################################
from types import *
from gluon.contrib import simplejson

try:
    exec('from applications.%s.modules import common' % this_app)
    page_helper, post_helper = common.controller_init(request, response, session, cache, T, db, auth, app_objects)
except Exception, ex:
    log_wrapped('Error (%s/controllers/data.py:~9)' % this_app, ex)
    
###################################
## CONTROLLER FUNCTIONS
###################################

default_entity_data = """{"meta":{"groupName":"meta.groupName","name":"meta.name","key":"meta.key"},"entity":{"text":{"text":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur, dolore eu fugiat nulla pariatur","imageUrl":"/a/static/css/themes/aisca/images/pic1.gif"},"summary":"Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip","links":{"text":"read more","name":"home_main_welcome"},"title":{"text":"Welcome to","name":"aisca"}}}"""
@auth.requires_login()
def index():
    def get_parse_data(form_vars):
        data = form_vars.data
        metas = ['name', 'groupName', 'key']
        for i in range(len(metas)):
            r = 'meta.%s'%metas[i]
            v = str({
                    'meta.groupName' : form_vars.group_name,
                    'meta.name' : form_vars.name,
                    'meta.key' : form_vars.id
            }[r])
            data = data.replace(r, v)
                    
        data = simplejson.loads(data)
        return data
    
    area = 'add'
    if len(request.args)>0:
        area = request.args[0]
    html = None
        
    form = None
    form2 = None
    form2_title = H2(T('Assign blocks'))
    form2_list = []
    form2_list_title = H2(T('Blocks'))
    form3_list = []
    form3_list_title = H2(T('Entities'))
    _id = -1

    entities = db(db.entities.id > 0).select()
    i=0
    for entity in entities:
        """ Eventually
        if area == 'add' and i==0:
            db.entities.data.default = entity.data
            i+=1
        """
        sql_form = SQLFORM(db.entities, entity, fields = ['group_name', 'name'],
                    labels = entities_labels, readonly=True, formstyle="divs")
        sql_form.append(A(T('edit'), _href=URL(r=request,args=['edit', entity.id])))
        form3_list.append(sql_form)
    if area == 'add' and i==0:
        db.entities.data.default = default_entity_data

    form = SQLFORM(db.entities, labels = entities_labels, _class='edit')
    if area == 'edit':
        _id = int(request.args[1])
        record = db(db.entities.id == _id).select()[0]
        form = SQLFORM(db.entities, record, 
                        labels = entities_labels, deletable=True, _class='edit')
        html = P(INPUT(_type="button", _onclick="window.location='%s';"%URL(r=request, args=['add']), 
                _value=T('add another'), _class = 'submit'), _class='text-alignr')
                
        db.entities_blocks.entity.default = record
        form2 = SQLFORM(db.entities_blocks, fields = ['block'], 
                        labels = entities_blocks_labels, formstyle="divs")
                        
        entity_blocks = db(db.entities_blocks.entity == _id).select()
        for entity_block in entity_blocks:
            form2_list.append(SQLFORM(db.entities_blocks, entity_block, 
                        fields = ['block'], labels = entities_blocks_labels, 
                        deletable=True, formstyle="divs", showid=False))
        
    if form.accepts(request.vars, session):
        flash = T('Entity data: %(area)sed ', dict(area=area))
        if area == 'add':
            data = get_parse_data(form.vars)
            data['meta']['key'] = form.vars.id
            db(db.entities.id == form.vars.id).update(data = simplejson.dumps(data))
            
            session.flash = flash
            redirect(URL(r = request, args=['edit', form.vars.id]))
        else:
            data = get_parse_data(form.vars)
            query = db(db.entities.id == form.vars.id)
            if query.select():
                query.update(data = simplejson.dumps(data))
            session.flash = flash
            redirect(URL(r = request, args=['edit', form.vars.id]))

    i=-1
    while i<len(form2_list):
        if i == -1:
            f = form2
        else:
            f = form2_list[i]
        if f and f.accepts(request.vars, session):
            flash = T('Entity blocks: %(area)sed ', dict(area=area))
            session.flash = flash
            redirect(URL(r = request, args=['edit', _id]))
        i+=1
    return dict(form=form, edit_title=T('Json data: %(area)s ', dict(area=area)), 
                html=html, form2_list_title=form2_list_title, form2_list=form2_list, 
                form2_title=form2_title, form2=form2,
                form3_list=form3_list, form3_list_title=form3_list_title)

def entity():
    area = 'save'
    if len(request.args)>0:
        area = request.args[0]

    if area in ['create', 'create.json']:
        key = int(request.vars.key)
        record = db(db.entities.id == key).select()[0]
        
        from gluon.contrib import simplejson
        data = simplejson.loads(record.data)
        if record.group_name == 'client_contact':
            data['entity']['text']['value'] = request.vars.message
            name = None
            for i in range(len(data['entity']['string'])):
                data['entity']['string'][i]['value'] = request.vars[data['entity']['string'][i]['name']]
                if data['entity']['string'][i]['name'] == 'name':
                    name = data['entity']['string'][i]['value']
        _id = db.entities.insert(
            name = '%s:%s'%(record.name,name),
            group_name = record.group_name,
            data = simplejson.dumps(data)
        )

        return response.json({
            'status' : 1,
            'message' : 'done',
            'result' : data
        })
        
    elif area in ['search', 'search.json', 'search.html']:
        entities = db().select(db.entities.ALL)
        results = filter(lambda x:(
                    x.searchable_through 
                    and 'site' in x.searchable_through 
                    and x.data and x.data.lower().find(request.vars.partialStr.lower())>0), entities
        )

        if area in ['search.html']:
            ## Page/Site Entity 'machine' for Html output
            mainBlockLayoutMapping = get_block_layout_mapping('entry_summary')
            _ids = map(lambda x:x.id, results)
            results = []
            for _id in _ids:
                mainBlockQuery = db(db.entities.id==_id)
                page = Page(
                    [
                        [
                            EntityBlock(block=BlockBase(layoutMapping=mainBlockLayoutMapping), query=mainBlockQuery),
                        ]
                    ]
                )
                page.populateEntityBlocks()
                results.append('<div id="#id">%s</div>' % page.blocks[0][0].layoutOutput())
        else:
            results = map(lambda x:x.data, results)
        return response.json({
            'status' : 1,
            'message' : 'done',
            'result' : results
        })
        


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
def save():
    try:
        q = db(db.json.name == request.vars.name)
        if len(q.select()):
            _id = q.update(
                name = request.vars.name,
                data = request.vars.data
            )
            return response.json({
                            'status' : 1,
                            'message' : 'update done',
                            'result' : _id
            })
        else:
            _id = db.json.insert(
                name = request.vars.name,
                data = request.vars.data
            )
            return response.json({
                            'status' : 1,
                            'message' : 'insert done',
                            'result' : _id
            })
    except Exception, ex:
        return response.json({
                            'status' : 0,
                            'message' : 'error',
                            'result' : str(ex)
        })


@auth.requires_login()
def read():
    try:
        _json = db(db.json.name == request.vars.name).select()[0].data
        return response.json({
                        'status' : 1,
                        'message' : 'read done',
                        'result' : simplejson.loads(_json)
        })
    except Exception, ex:
        return response.json({
                        'status' : 0,
                        'message' : 'error',
                        'result' : str(ex)
        })
    except Exception, ex:
        return str(ex)

def fetch():
    from gluon.tools import fetch
    return fetch(request.vars.url, headers = {'Cache-Control' : request.vars.cache_control, 'Pragma' : request.vars.pragma})
