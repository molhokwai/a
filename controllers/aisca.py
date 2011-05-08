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
    homePage = HomePage()
    homePage.populateEntityBlocks()
    
    return dict(entityBlocks = homePage.entityBlocks, blocks = homePage.blocks)
