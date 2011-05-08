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

    indexPage = Page(
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
    indexPage.populateEntityBlocks()
    
    return dict(entityBlocks = indexPage.entityBlocks, blocks = indexPage.blocks)


def read():
    ## Main block
    mainBlockLayoutMapping = get_block_layout_mapping('entry')
    mainBlockQuery = db(db.entities.name == 'presenting')

    ## Icons block
    iconsBlockLayoutMapping = get_block_layout_mapping('icon_list')
    iconsBlockQuery = db(db.entities.group_name == 'main_icons')

    ## Main block
    newsBlockLayoutMapping = get_block_layout_mapping('feed_list_summary')
    newsBlockQuery = db(db.entities.group_name == 'main_news-updates')

    indexPage = Page(
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
    indexPage.populateEntityBlocks()
    
    return dict(entityBlocks = indexPage.entityBlocks, blocks = indexPage.blocks)
