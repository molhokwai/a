#!/usr/bin/env python 
# coding: utf8 
from types import *
from gluon.html import *
from gluon.http import *
from gluon.validators import *
from gluon.sqlhtml import *
# request, response, session, cache, T, db(s) 
# must be passed and cannot be imported!

#########################################################################
## CLASSES :
##    BlockBase
##    Entity
##    EntityBlock
##    EntityMapping
##    LayoutMapping
##    Template
##
#########################################################################


class BlockBase:

    """


    :version:
    :author:
    """

    """ ATTRIBUTES

    entityMappings  (public)
        EntityMapping.mapping object (dictionary) required if Entity attributes does not
        directy map to LayoutMapping placehoders
            [1,0] -right top, [1,1] -right bottom )
    layoutMapping  (public)
    """
    entityMappings = None
    layoutMapping = None


    def __init__(self, entityMappings=None, layoutMapping=None):
        if entityMappings:
            self.entityMappings = entityMappings
        if layoutMapping:
            self.layoutMapping = layoutMapping


    _layoutOutput = None
    def layoutOutput(self):
        """
         Generic method:
            - Using reflection to match Entity relevant attributes to corresponding block
              layoutMapping placeholders
            - Executing replacements (looping through entities) and returning output

        @return string :
        @author
        """
        if not self._layoutOutput:
            self._layoutOutput = self.layoutMapping.listOrder
            for i in range(len(self.entityMappings)):
                entity = self.entityMappings[i].entity                
                for key in entity.__dict__:
                    e_attr = entity.__dict__.get(key)
                    l_attr = self.layoutMapping.__dict__.get(key)
                    
                    if l_attr:
                        l_attr_v = ''   
                        if type(e_attr) == ListType:
                            for i in range(len(e_attr)):
                                l_attr_v += l_attr.xml() % {key : e_attr[i]}

                        elif type(e_attr) == DictType:
                            l_attr_v += l_attr.xml() % e_attr

                        else:
                            l_attr_v += l_attr.xml() % e_attr

                        self.layoutMapping.__dict__.update({key:l_attr_v})
                        self._layoutOutput[self._layoutOutput.index(key)]= l_attr_v
                        
            self._layoutOutput = self.layoutMapping.container % dict(content='\n'.join(self._layoutOutput))
        return self._layoutOutput
        

class Entity():

    """
     

    :version:
    :author:
    """

    """ ATTRIBUTES

    _**attr  (public)

    """
    @staticmethod
    def fetch(query):
        """
        - Executes the query object
        - Returns a List of Entity objects with attributes populated from fetched entities         

        @param type _type : 
        @param object _key : 
        @return Entity :
        @author
        """
        from gluon.contrib import simplejson
        e_dicts = map(lambda x: simplejson.loads(x.post_attributes_json)["entity"], query.select())
        entities = []
        for i in range(len(e_dicts)):
            e = Entity()
            e.__dict__.update(e_dicts[i])
            entities.append(e)
        return entities


class EntityBlock(object):

    """
     Dynamic Entity assignment to Block

    :version:
    :author:
    """

    """ ATTRIBUTES

    entities  (public)
    block  (public)
    query  (public)
        (Sql string | Else)

    """
    entities = None
    block = None
    query = None

    def __init__(self, **kwargs):
        if kwargs:
            self.__dict__.update(kwargs)


class EntityMapping():

    """
     

    :version:
    :author:
    """

    """ ATTRIBUTES
    entity  (public)
    content  (public)
    optional_url  (public)
    optional_imageUrl  (public)
    opt_mapping  (public)
        Object (dictionary) required if Entity mapping does not match LayoutMapping
        key : the LayoutMapping attribute, value: the entity corresponding attribute

    """
    entity = None
    content = None
    url = None
    imageUrl = None
    mapping = None

    def setContent(self, value):
        self.content = value
    def setUrl(self, value):
        self.url = value
    def setImageUrl(self, value):
        self.imageUrl = value

    def __init__(self, entity, mapping=None):
        """
        If mapping object provided, attributes are appended to object accordingly         

        @return  :
        @author
        """
        self.entity = entity
        if mapping:
            self.mapping = mapping
            for attr in mapping:
                value = self.entity.__dict__.get(mapping[attr])
                self.__dict__.update({attr:value})


class LayoutMapping():

    """
     Attributes title & string:
         - String (xml/html...) with placeholders for entity mapping

    :version:
    :author:
    """

    """ ATTRIBUTES

    container (public)
    title  (public)
    summary (public)
    content  (public)

    """

    container = None
    title = None
    summary = None
    content = None
    _list = {'container' : '', 'content' : ''}



class Template(object):

    """
     

    :version:
    :author:
    """

    """ ATTRIBUTES

    menu  (public) (documentation only)
    footer  (public) (documentation only)
    container  (public) (documentation only)
    entityBlocks  (private)
        Abstract attribute to be implemented in child Page

    Mapping by type:
        - Entity type (Post, NewsUpdate, Service...)
        - Block by coordinates :
            ([0,0] -left top,   [0,1]  -left borrom,
              [1,0] -right top, [1,1] -right bottom )
    """
    entityBlocks = None 

    _blocks = None
    @property
    def blocks(self):
        """
        Property, returning the blocks from the entityBlocks Attribute, keeping the x,y list coordinates.

        @return  :
        @author
        """
        if not self._blocks:
            self._blocks = []
            for x in range(len(self.entityBlocks)):
                self._blocks.append([])
                for y in range(len(self.entityBlocks[x])):
                    self._blocks[x].append(self.entityBlocks[x][y].block)
        return self._blocks
                

    def __init__(self, entityBlocks):
        """
        @param EntityBlock entityBlocks : 
        @return  :
        @author
        """
        self.entityBlocks = entityBlocks

                    
    def populateEntityBlocks(self, entityBlocks=None):
        """
        Method used to get and assign the entities for each entityBlock. 

        @param EntityBlock opt_entityBlocks : Uses the class's entityBlocks attribute unless optional entityBlocks parameter given
        @return Entity :
        @author
        """
        if not entityBlocks:
            entityBlocks = self.entityBlocks
        for x in range(len(entityBlocks)):
            for y in range(len(entityBlocks[x])):
                entityBlock = entityBlocks[x][y]
                entityBlock.entities = Entity.fetch(entityBlock.query)
                entityMapping = entityBlock.block.entityMappings[0]
                for i in range(len(entityBlock.entities)):
                    if i<len(entityBlock.block.entityMappings):
                        entityBlock.block.entityMappings[i].entity = entityBlock.entities[i]
                    else:
                        e = None
                        e = entityMapping
                        e.entity = entityBlock.entities[i]
                        entityBlock.block.entityMappings.append(e)
