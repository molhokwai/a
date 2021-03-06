/* html form */
/*      <cli_web class="left margt2pc  width100pc">
        <form action="/lcs/cli_web/_do" method="post" onsubmit="return on_cli_web_submit();">
            <input type="text" id="_cmd" name="_cmd" class="width30pc"/>
            <font id="_cmd_msg" class="flash small">
                {{if session.cli_web_flash:}}{{=session.cli_web_flash}}{{ session.cli_web_flash=False }}{{pass}}
                {{if session.flash:}}{{=session.flash}}{{pass}}
            </font>
            <input type="hidden" id="_cmd_history_cur" value="-1"/>
        </form>
      </cli_web>
*/

/* configuration & settings */
settings={
       markItUp:{
            onShiftEnter:   {keepDefault:false, replaceWith:'<br />\n'},
            onCtrlEnter:    {keepDefault:false, openWith:'\n<p>', closeWith:'</p>'},
            onTab:          {keepDefault:false, replaceWith:'    '},
            markupSet:  [   
                {name:'Bold', key:'B', openWith:'(!(<strong>|!|<b>)!)', closeWith:'(!(</strong>|!|</b>)!)' },
                {name:'Italic', key:'I', openWith:'(!(<em>|!|<i>)!)', closeWith:'(!(</em>|!|</i>)!)'  },
                {name:'Stroke through', key:'S', openWith:'<del>', closeWith:'</del>' },
                {separator:'---------------' },
                {name:'Picture', key:'P', replaceWith:'<img src="[![Source:!:http://]!]" alt="[![Alternative text]!]" />' },
                {name:'Link', key:'L', openWith:'<a href="[![Link:!:http://]!]"(!( title="[![Title]!]")!)>', closeWith:'</a>', placeHolder:'Your text to link...' },
                {separator:'---------------' },
                {name:'Clean', className:'clean', replaceWith:function(markitup) { return markitup.selection.replace(/<(.*?)>/g, "") } },       
                {name:'Preview', className:'preview',  call:'preview'}
            ]
       },
       google: {
           search : {
               load : false,
               loaded : false
           }
       }
};

/* brake them, change them, until there are none anymore */
rules={
    page : {
        current : {
            id : {
                get : 
                    /* rule: to find the id in the url */
                    function(){
                        var args=window.location.split('/');
                        args.pop(0), args.pop(1), args.pop(2);
                        if (args.length>1)
                            if (args[0]=='page'){
                            }
                        /* to be continued somewhen, or never, this code into javascript
                            ------------------------------------------------------------
                            <code>    
                                if len(request.args)>2:
                                    if (request.args[0]=='edit' 
                                        and (request.args[1]=='page' or request.args[1]=='post')):
                                        return int(request.args[2])
                                if len(request.args)>1:
                                    if request.args[0]=='page':
                                        return int(request.args[1])
                                return -1
                            </code>              
                        */
                    }
            }
        }
    }
}

/* ... */
var markup_textareas=function(){
    $('textarea').markItUp(settings.markItUp);
};


/*************
  context : page.cli_web
**************/

/* double press ctrl key command vars & config */
var ctrl_timeout=null;
var ctrl_max_interval=150;

/* to focus on the 1st form element */
var focus=function(cmd){
    var rv=false;
    params=null;
    if (cmd.split(':').length>1)
        params=cmd.split(':')[1].split(',');
        cmd=cmd.split(':')[0].replace(' ','').toLowerCase();
        
    switch(cmd){
        case 'form':
            if ($('form:visible:last')){
                if ($($('form:visible:last')).formFirstField) {
                    $($('form:visible:last')).formFirstField().focus();
                }
                else {
                    document.getElementById('_cmd').focus();                    
                }
                rv=true;
            }
            break;
        default:
            break;
    }
    
    return rv;
};

/* to attempt finding and triggering the page element given in the command */
var click=function(cmd){
    var rv=false;

    params=null;
    if (cmd.split(':').length>1)
        params=cmd.split(':')[1].split(',');
        cmd=cmd.split(':')[0].toLowerCase();
        
    switch(cmd){
        default:
            /* 'a', 'button', 'link', 'go', 'goto', 'click' */
            if (params==null){
                params=new Array();
                params[0]=cmd;
            }
            var fd=false;
            var el=null;
            
            if (cmd!='button'){
                $.each($('a'), function() {
                  if (!fd && this.innerHTML.toLowerCase()
                          .indexOf(params[0].toLowerCase())>=0){
                      fd=true;
                      el=this;
                      rv=true;
                  }
                });
                /******
                -- Nope! not possible to search in external iframes
                --    cross domain js, cross domain js...
                if (el==null){
                    $.each($('iframe'), function() {
                      $.each($('#'+this.id).contents().find('.signin'), function() {
                        if (!fd && this.innerHTML.toLowerCase()
                                .indexOf(params[0].toLowerCase())>=0){
                            fd=true;
                            el=this;
                            rv=true;
                        }
                      });
                    });
                }
                *****/
            }
            
            if (el!=null){
                /* why this not working: $(el).trigger('click'); ? */
                if (el.href.indexOf('javascript:')==0){
                    eval(el.href.substring('javascript:'.length));
                }
                else {
                    /* _no history_ alternative: window.location.replace(el.href); */
                    window.location=el.href;
                }
                return true
            }
            else{
                $(':button').each(function() {
                  if (!fd && $(this).val().toLowerCase()
                          .indexOf(params[0].toLowerCase())>=0){
                      fd=true;
                      el=this;
                      rv=true;
                  }
                });
                if (el!=null){
                    $(el).trigger('click');
                }
                else {
                    $(':submit').each(function() {
                      if (!fd && $(this).val().toLowerCase()
                              .indexOf(params[0].toLowerCase())>=0){
                          fd=true;
                          el=this;
                          rv=true;
                      }
                    });
                }

                if (el!=null){
                    $(el).trigger('click');
                }
                else {
                    /****** These: 
                        <code language="javascript">
                            $.each([':checkbox', ':radio'], function() ...
                        </code>
                        
                        <code language="javascript">
                            $('#cmd_flash').exists()
                        </code>

                        ...crashes on ubuntu 9.10 - chrome (incognito window).
                        Report it, if you will help some-one.
                    ******/
                    $(':checkbox').each(function() {
                        if (!fd && ($(this).attr('name').toLowerCase().indexOf(params[0].toLowerCase())>=0
                          || $(this).attr('id').toLowerCase().indexOf(params[0].toLowerCase())>=0
                          || $(this).attr('value').toLowerCase().indexOf(params[0].toLowerCase()))>=0){
                            fd=true;
                            el=this;
                            rv=true;
                        }
                    });

                    if (el!=null){
                        $(el).trigger('click');
                    }
                    else {
                        $(':radio').each(function() {
                            if (!fd && ($(this).attr('name').toLowerCase().indexOf(params[0].toLowerCase())>=0
                              || $(this).attr('id').toLowerCase().indexOf(params[0].toLowerCase())>=0
                              || $(this).attr('value').toLowerCase().indexOf(params[0].toLowerCase()))>=0){
                                fd=true;
                                el=this;
                                rv=true;
                            }
                        });
    
                        if (el!=null){
                            $(el).trigger('click');
                        }
                        else if (el==null){
                                if ($(':'+params[0]+':visible:last')){
                                fd=true;
                                el=$(':'+params[0]+':visible:last');
                                rv=true;
                            }
                        }
                    }
                }
            }
            break;
    }
    
    return rv;
};

/* on document ready... */
$(document).ready(function(){
    /* cli web dbl ctrl shortcut... */
    $('body').keyup(function(event){
      if (event.keyCode==17){
          if (ctrl_timeout!=null){
              $('#_cmd').focus();
          }
          ctrl_timeout=setTimeout('clearTimeout(ctrl_timeout); ctrl_timeout=null;', ctrl_max_interval);
      }
    });
    
    if ($.browser.mozilla){
        $('#_cmd').bind('keyup', function(e){
            if((e.keyCode ? e.keyCode : e.which) == 13) {
                if (on_cli_web_submit()){
                    $('#_cmd').parents('form:first').submit();
                }
            }
        });
    }
    
    focus('form');

    if (settings.google.search.load){
        settings.google.search.loaded=google_search_load();
    }    
});

/* caught eval to more or less brutally evaluate the given command,
    catch any (probable) exception, and continue
*/
var cec_rv='boom, crashshsh...';
var caught_eval=function(value){
    try{
        return eval(value);
    }
    catch(e){
        return cec_rv;
    }
};

/* on_cli web submit event handler */
var on_cli_web_submit=function(){
    /* >(command) for direct server call */
    if ($('#_cmd').val().substring(0,1)=='>'){
        return true;
    }
    
    /* quick fix */
    if ($('#_cmd').val()=='home'){ $('#_cmd').val('root');}
    
    try {
        /* raw eval */
        var rv=caught_eval($('#_cmd').val());
        
        /* added 'punctuation' eval */
        if (rv==cec_rv){
            rv=caught_eval($('#_cmd').val().replace(' ', '.'));
        }

        /* added 'punctuation' & method last eval */
        if (rv==cec_rv){
            rv=caught_eval($('#_cmd').val().replace(' ', '.')+'()');
        }

        /* last chance function... */
        try{ 
            var _fct=null;
            if ('function'==typeof rv && eval(rv)==rv) _fct=rv;
        }
        catch(e){
        }
        
        /* assumptions eval */
        if (rv==cec_rv || eval(rv)==rv){
            /* assumption: element focus */
            rv=focus($('#_cmd').val());
            
            if (!rv){
                rv=click($('#_cmd').val());
            }
        }
        
        /* last chance... */
        try{ 
            if (_fct){
                _fct=_fct;
                _fct();
                rv=true;
            } 
        }
        catch(e){
        }
        
        if (rv) {
            $('#_cmd_msg').append('done ('+(parseInt($('#_cmd_msg')).html()+1)+')');
        }
        else {
            $('#_cmd_msg').html('falling back to google search...');
            if (settings.google.search.loaded){
                molhokwai.google.search.response.get(cmd.toString());
            }
        }
        
        return false;
    }
    catch(e)
    {
        if ($('#_cmd_msg').length>0) {
            $('#_cmd_msg').html(e);
        }
        if (settings.google.search.loaded){
            molhokwai.google.search.response.get(cmd.toString());
        }
        return false;
    }
};


/*************
  context : browser
  utilities
**************/

/* convenience (for cli_web also) methods */
var back=b=function(){
  history.go(-1);
}
var forward=fwd=f=function(){
  history.go(+1);
}
