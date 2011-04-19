###################################
## CONTROLLER INITIALIZATION
###################################    

try:
    exec('from applications.%s.modules import common' % this_app)
    common.app_init(request, response, session, cache, T, db, app_objects)
    page_helper, post_helper = common.controller_init(request, response, session, cache, T, db, auth, app_objects)    
except Exception, ex:
    log_wrapped('Er (%s/controllers/setup.py:9' % this_app, ex)

###################################
## CONTROLLER FUNCTIONS
###################################    

@auth.requires_login()
def index():
    if auth.user.email in administrators_emails:
        auth.user.is_admin=True
        for _email in administrators_emails:
            db(db.auth_user.email==_email).update(is_admin=True)    

        form=SQLFORM(db.app_config)
        form1=FORM(
            SPAN(T('save/load from json data file upload')),
            INPUT(_type='file', _name='file', _value='(upload json data file)'),
            INPUT(_type='submit', _value=T('upload, save/load')),
            _class='margb2pc'
        )

        ace = db(db.app_config.id>0)
        if form1.accepts(request.vars, session):
            ac=Struct(**eval(request.vars.file.file.getvalue()))
            if ace.select():
                ace.update(
                    APP_CURRENT_LANGUAGES=ac.APP_CURRENT_LANGUAGES,
                    APP_DETAILS=ac.APP_DETAILS,
                    APP_METAS=ac.APP_METAS,
                    APP_THEMES=ac.APP_THEMES,
                    BLOGGER_API=ac.BLOGGER_API,
                    BLOGGER_BLOGS_LANGUAGES=ac.BLOGGER_BLOGS_LANGUAGES,
                    BLOGGER_BLOGS_THEMES=ac.BLOGGER_BLOGS_THEMES,
                    MAIL_SETTINGS=ac.MAIL_SETTINGS,
                    PICASA_API=ac.PICASA_API,
                    RPX_API=ac.RPX_API,
                    TWITTER_API=ac.TWITTER_API
                )
                ace = ace.select()[0]
            else:
                ace=db.app_config.insert(
                    APP_CURRENT_LANGUAGES=ac.APP_CURRENT_LANGUAGES,
                    APP_DETAILS=ac.APP_DETAILS,
                    APP_METAS=ac.APP_METAS,
                    APP_THEMES=ac.APP_THEMES,
                    BLOGGER_API=ac.BLOGGER_API,
                    BLOGGER_BLOGS_LANGUAGES=ac.BLOGGER_BLOGS_LANGUAGES,
                    BLOGGER_BLOGS_THEMES=ac.BLOGGER_BLOGS_THEMES,
                    MAIL_SETTINGS=ac.MAIL_SETTINGS,
                    PICASA_API=ac.PICASA_API,
                    RPX_API=ac.RPX_API,
                    TWITTER_API=ac.TWITTER_API
                )
            session.flash=T('Default values saved and loaded')
            redirect(URL(r=request, c='setup'))

        elif ace.select():
            ace = ace.select()[0]
            form=SQLFORM(db.app_config, ace)           

        if form.accepts(request.vars, session):
            session.flash=T('Application setup/configuration done')
            redirect(URL(r=request, c='default'))
    else:
        form=FORM(DIV(T('Your email is not in the administrators\' list.')))
    return dict(form = form, form1 = form1)
