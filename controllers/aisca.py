###################################
## CONTROLLER INITIALIZATION
###################################
 
"""try:"""
if True:
    app_objects.__dict__.update({'menu_order':['a_home', 'the_system-entry', 'the_technology-entry', 'the_options-entry', 'demo request', 'contact us']})
    exec('from applications.%s.modules import common' % this_app)
    page_helper, post_helper = common.controller_init(request, response, session, cache, T, db, auth, app_objects)

    app_objects.__dict__.update({
        'page_helper' : page_helper,
        'post_helper' : post_helper,
        'home_page_link'   : common.home_page_link,
        'help_page_link'   : common.help_page_link
    })
    exec('from applications.%s.modules import aisca as m_aisca' % this_app)
    page_helper, post_helper = m_aisca.controller_init(request, response, session, cache, T, db, auth, app_objects)

"""except Exception, ex:
    log_wrapped('Error (%s/controllers/default.py:9)' % this_app, ex)
"""    
###################################
## CONTROLLER FUNCTIONS
###################################

def index():
    ## Main block
    mainBlockLayoutMapping = get_block_layout_mapping('entry_summary')
    mainBlockQuery = db(db.entities.name == 'presenting')

    ## Summaries block
    summariesBlockLayoutMapping = get_block_layout_mapping('entry_list_summary')
    summariesBlockQuery = db(db.entities.group_name == 'main_the-system')

    ## Icons block
    iconsBlockLayoutMapping = get_block_layout_mapping('icon_list')
    iconsBlockQuery = db(db.entities.group_name == 'main_icons')

    ## Main block
    newsBlockLayoutMapping = get_block_layout_mapping('feed_list_summary')
    newsBlockQuery = db(db.entities.group_name == 'main_news-updates')

    page = Page(
        [
            [
                EntityBlock(block=BlockBase(layoutMapping=mainBlockLayoutMapping), query=mainBlockQuery),
                EntityBlock(block=BlockBase(layoutMapping=summariesBlockLayoutMapping), query=summariesBlockQuery),
            ]
            ,
            [
                EntityBlock(block=BlockBase(layoutMapping=iconsBlockLayoutMapping), query=iconsBlockQuery),
                EntityBlock(block=BlockBase(layoutMapping=newsBlockLayoutMapping), query=newsBlockQuery),
            ]
        ]
    )
    page.populateEntityBlocks()
    
    return dict(entityBlocks = page.entityBlocks, blocks = page.blocks)


def read():
    ## Main block
    mainBlockLayoutMapping = get_block_layout_mapping('entry')
    mainBlockQuery = db(db.entities.name == request.args[0])

    ## Icons block
    iconsBlockLayoutMapping = get_block_layout_mapping('icon_list')
    iconsBlockQuery = db(db.entities.group_name == 'main_icons')

    ## Main block
    newsBlockLayoutMapping = get_block_layout_mapping('feed_list_summary')
    newsBlockQuery = db(db.entities.group_name == 'main_news-updates')

    page = Page(
        [
            [
                EntityBlock(block=BlockBase(layoutMapping=mainBlockLayoutMapping), query=mainBlockQuery),
            ]
            ,
            [
                EntityBlock(block=BlockBase(layoutMapping=iconsBlockLayoutMapping), query=iconsBlockQuery),
                EntityBlock(block=BlockBase(layoutMapping=newsBlockLayoutMapping), query=newsBlockQuery),
            ]
        ]
    )
    page.populateEntityBlocks()
    
    return dict(entityBlocks = page.entityBlocks, blocks = page.blocks)


def contact():
    ## Main block
    ## mainBlockLayoutMapping = get_block_layout_mapping('entry')
    ## mainBlockQuery = db(db.entities.name == request.args[0])

    ## Form block
    formBlockLayoutMapping = get_block_layout_mapping('form')
    formBlockQuery = db(db.entities.name == 'contact_form-entry')

    ## Main block
    newsBlockLayoutMapping = get_block_layout_mapping('feed_list_summary')
    newsBlockQuery = db(db.entities.group_name == 'main_news-updates')

    page = Page(
        [
            [
                ## EntityBlock(block=BlockBase(layoutMapping=mainBlockLayoutMapping), query=mainBlockQuery),
            ]
            ,
            [
                EntityBlock(block=BlockBase(layoutMapping=formBlockLayoutMapping), query=formBlockQuery),
                EntityBlock(block=BlockBase(layoutMapping=newsBlockLayoutMapping), query=newsBlockQuery),
            ]
        ]
    )
    page.populateEntityBlocks()
    
    return dict(entityBlocks = page.entityBlocks, blocks = page.blocks)
