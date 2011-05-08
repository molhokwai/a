# coding: utf8
from types import *

#########################################################################
## PAGE SITE BLOCKS
#########################################################################

try:
    exec('from applications.%s.modules.page_site_blocks.BlockBase import BlockBase' % this_app)
    exec('from applications.%s.modules.page_site_blocks.Entity import Entity' % this_app)
    exec('from applications.%s.modules.page_site_blocks.EntityBlock import EntityBlock' % this_app)
    exec('from applications.%s.modules.page_site_blocks.EntityMapping import EntityMapping' % this_app)
    exec('from applications.%s.modules.page_site_blocks.LayoutMapping import LayoutMapping' % this_app)
    exec('from applications.%s.modules.page_site_blocks.Template import Template' % this_app)
except Exception, ex:
    log_wrapped('Error (%s/models/modules.py)' % this_app, ex)

class StandardBlock(BlockBase):
    entityMappings = None
    layoutMapping = None

    def __init__(self, entityMappings=None, layoutMapping=None):
        if entityMappings:
            self.entityMappings = entityMappings
        else:
            self.entityMappings = [EntityMapping(type(db.posts))]
            
        if layoutMapping:
            self.layoutMapping = layoutMapping
        else:
            self.layoutMapping = LayoutMapping()
            self.layoutMapping.container = "%(content)s"
            self.layoutMapping.title = DIV(("%(text)s ", SPAN("%(name)s")), _class='title')
            self.layoutMapping.summary = P("%s", _class="blue")
            self.layoutMapping.text = P((IMG(_src="%(imageUrl)s", _class="left_img"), "%(text)s"))
            self.layoutMapping.links = DIV(A("%(text)s", _href="%(url)s"), _class="read_more")
            self.layoutMapping.listOrder = ['title','summary','text','links']

        BlockBase.__init__(self, entityMappings=entityMappings, layoutMapping=layoutMapping)

class PageBase(Template):

    """
     

    :version:
    :author:
    """

    """ ATTRIBUTES

    blocks  (protected)
        Implementation of the Parent's (Template) abstract attribute, 
        for a global site default Base Page
    entityBlocks  (protected)
        Implementation of the Parent's (Template) abstract attribute, 
        for a global site default Base Page
    """
    entityBlocks = [[EntityBlock(block=StandardBlock(), query=db(db.posts.id==64))]]


    def __init__(self, entityBlocks=None):
        """
         The construction method of the page passes the  page's implemented entityBlocks
         attribute to the Template base class construction , or the optional entityBlocks 
        Parameter.

        @return  :
        @author
        """
        if entityBlocks:
            self.entityBlocks = entityBlocks
        Template.__init__(self, self.entityBlocks)


class HomePage(PageBase):

    """
     

    :version:
    :author:
    """

    """ ATTRIBUTES

    blocks  (protected)
        Optional Implementation of the Parent's (Template) abstract attribute
    entityBlocks  (protected)
        Optional Implementation of the Parent's (Template) abstract attribute
    """
    
    """
    blocks = None
    entityBlocks = None
    """
