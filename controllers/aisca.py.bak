###################################
## CONTROLLER INITIALIZATION
###################################

try:
    exec('from applications.%s.modules import common' % this_app)
    page_helper, post_helper = common.controller_init(request, response, session, cache, T, db, auth, app_objects)
except Exception, ex:
    log_wrapped('Error (%s/controllers/default.py:9)' % this_app, ex)
    
###################################
## CONTROLLER FUNCTIONS
###################################

def index():
    ## Layout mappings and query for entities that have attributes 
    ## matching the layout
    
    ## Main block
    ## ----------
    mainBlockLayoutMapping = LayoutMapping(
        container = DIV("%(content)s"),
        title = DIV(("%(text)s ", SPAN("%(name)s")), _class='title'),
        summary = P("%s", _class="blue"),
        text = P((IMG(_src="%(imageUrl)s", _class="left_img"), "%(text)s")),
        links = DIV(A("%(text)s", _href="%(url)s"), _class="read_more"),
        listOrder = ['title','summary','text','links']
    )
    mainBlockQuery=db(db.posts.post_title=='home_main_block_layout_entities')

    ## System block
    ## ----------
    systemBlockLayoutMapping = LayoutMapping(
        container = DIV((DIV(("The ", SPAN("system")), _class='title'), 
                        "%(content)s")),
        text = DIV(IMG(_src="%(imageUrl)s", _class="icon"), BR(), 
                   P((SPAN("%(title)s", _class="blue"), BR(), "%(text)s"), _class="services"),
                     _class="services_box"),
        listOrder = ['text']
    )
    systemBlockQuery=db(db.posts.post_title=='system_block_layout_entities')
    
    
    ## The page construction
    homePage = Page(
        entityBlocks = [
                         [
                           EntityBlock(
                            block=Block(layoutMapping=mainBlockLayoutMapping), 
                            query=mainBlockQuery
                           ),
                           EntityBlock(
                            block=Block(layoutMapping=systemBlockLayoutMapping), 
                            query=systemBlockQuery
                           )
                         ]
                       ],
    )
    homePage.populateEntityBlocks()

    ## The attributes for view output    
    return dict(entityBlocks = homePage.entityBlocks, blocks = homePage.blocks)
