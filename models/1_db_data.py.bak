# coding: utf8
db.define_table('json',
    SQLField('name', required=True),
    SQLField('data','text', required=True)
)
db.json.name.requires = IS_NOT_IN_DB(db, 'json.name', 'json.name')

json_labels = {
    'name' : T('name'),
    'data' : T('data')
}
