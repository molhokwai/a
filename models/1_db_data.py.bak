# coding: utf8
db.define_table('json',
    SQLField('name', required=True),
    SQLField('data','text', required=True)
)
db.json.name.requires = IS_NOT_IN_DB(db, 'json.name', 'json.name')

db.define_table('entities',
    SQLField('group_name', required=True),
    SQLField('name', required=True),
    SQLField('data','text', required=True)
)
db.entities.name.requires = IS_NOT_IN_DB(db, 'entities.name', 'entities.name')

db.define_table('entities_blocks',
    SQLField('entity', db.entities, required=True),
    SQLField('block', required=True)
)
db.entities_blocks.entity.requires = IS_IN_DB(db, 'entities.id', 'entities.name')

json_labels = entities_labels = {
    'name' : T('name'),
    'data' : T('data')
}

entities_blocks_labels = {
    'entity' : T('entity'),
    'block' : T('block')
}
