###################################
## CONTROLLER INITIALIZATION
###################################    

try:
    exec('from applications.%s.modules import common' % this_app)
    app_objects=Struct(**{'details':app_details,'config':app_config,'log_wrapped':log_wrapped,'utilities':utilities})
    common.app_init(request, response, session, cache, T, db, app_objects)
    page_helper, post_helper = common.controller_init(request, response, session, cache, T, db, auth, app_objects)    
except Exception, ex:
    log_wrapped('Er', ex)

###################################
## CONTROLLER FUNCTIONS
###################################    

@auth.requires_login()
def index():
    if auth.user.email in administrators_emails:
        auth.user.is_admin=True
        for _email in administrators_emails:
            db(db.auth_user.email==_email).update(is_admin=True)    
        
        form=SQLFORM(db.app_config, app_config)
        if form.accepts(request.vars, session):
            session.flash=T('Application setup/configuration done')
            redirect(URL(r=request, c='default'))
    else:
        form=FORM(DIV(T('Your email is not in the administrators\' list.')))
    return dict(form = form)
