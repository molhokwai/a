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


#########################################################################
## SAMPLE LAYOUT MAPPING & BLOCK CONSTRUCTION
#########################################################################
## standardLayoutMapping =  LayoutMapping(
##    container = "%(content)s",
##    title = DIV(("%(text)s ", SPAN("%(name)s")), _class='title'),
##    summary = P("%s", _class="blue"),
##    text = P((IMG(_src="%(imageUrl)s", _class="left_img"), "%(text)s")),
##    links = DIV(A("%(text)s", _href="%(url)s"), _class="read_more"),
##    listOrder = ['title','summary','text','links']
##)
##
## block = BlockBase(layoutMapping=standardLayoutMapping)
    
class Page(Template):

    """
     

    :version:
    :author:
    """

    """ ATTRIBUTES

    entityBlocks  (protected)
        Optional Implementation of the Parent's (Template) abstract attribute, 
        for a global site default Base Page
        Like:
            entityBlocks = [[EntityBlock(block=Block(), query=db(db.entities.group_name=="home_main_entity"))]]
    """
    entityBlocks = []


    def __init__(self, entityBlocks):
        """
         The construction method of the page passes the  page's implemented entityBlocks
         attribute to the Template base class construction , or the optional entityBlocks 
        Parameter.

        @return  :
        @author
        """
        Template.__init__(self, entityBlocks)


###################################
## Blocks layout mapping definitions
###################################

blocks_layout_mapping = {
    'entry': LayoutMapping(
            container = DIV("%(content)s"),
            title = DIV(("%(text)s ", SPAN("%(name)s")), _class='title'),
            summary = P("#:#display#:#truncate#:#%s#:#200", _class="blue display"),
            text = P((IMG(_src="%(imageUrl)s", _class="left_img"), "%(text)s")),
            listOrder = ['title','summary','text']
        ),
    'entry_summary': LayoutMapping(
            container = DIV("%(content)s"),
            title = DIV(("%(text)s ", SPAN("%(name)s")), _class='title'),
            summary = P("#:#display#:#truncate#:#%s#:#200", _class="blue display"),
            text = P((IMG(_src="%(imageUrl)s", _class="left_img"), 
                        "#:#display#:#truncate#:#%(text)s#:#350#:#['hide','.read_more']"),
                        _class="display"),
            links = DIV(A("%(text)s", _href="/a/aisca/read/%(name)s"), _class="read_more"),
            listOrder = ['title','summary','text','links']
        ),
     'entry_list_summary': LayoutMapping(
            container = DIV(DIV(("The ", SPAN("system")), _class='title'), 
                            "%(content)s"),
            text = DIV(IMG(_src="%(imageUrl)s", _class="icon"), BR(), 
                       P((SPAN("%(title)s", _class="blue"), BR(), 
                       "#:#display#:#truncate#:#%(text)s#:#290#:#['hide','.read_more']"), 
                       _class="services display"),
                 _class="services_box"),
            links = DIV(A("%(text)s", _href="/a/aisca/read/%(name)s"), _class="read_more"),
            listOrder = ['text', 'links']
        ),
     'icon_list': LayoutMapping(
            container = DIV(DIV(("Main ", SPAN("links")), _class='title'), 
                            DIV("%(content)s", _class="latest_projects")),
            image = A(IMG(_src="%(imageUrl)s", _class="img_border"), _href="%(url)s"),
            listOrder = ['image']
        ),
     'feed_list_summary': LayoutMapping(
            container = DIV(DIV(("News & ", SPAN("updates")), _class='title'), 
                            "%(content)s"),
            text = P("#:#display#:#truncate#:#%s#:#210#:#['hide', '.read_more']", 
                    _class="news display"),
            links = DIV(A("%(text)s", _href="/a/aisca/read/%(name)s"), _class="read_more"),
            listOrder = ['text', 'links']
        ) 
}
def get_block_layout_mapping(name):
    return blocks_layout_mapping[name]
db.entities_blocks.block.requires = IS_IN_SET(map(lambda x: '%s(%s)' % (x[0],','.join(x[1].__dict__.keys())),
                                        [(_name,blocks_layout_mapping[_name]) for _name in blocks_layout_mapping]))
