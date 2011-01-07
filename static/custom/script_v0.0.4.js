/* html form */
/*      <form onsubmit="return false;">
            <input type="text" id="_cmd" name="_cmd" class="width30pc"/>
            <font id="_cmd_msg" class="flash small">
                {{if session.cli_web_flash:}}{{=session.cli_web_flash}}{{ session.cli_web_flash=False }}{{pass}}
                {{if session.flash:}}{{=session.flash}}{{pass}}
            </font>
            <input type="hidden" id="_cmd_history_cur" value="-1"/>
        </form>
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
    if (cmd.split(':').length>1){
        params=cmd.split(':')[1].split(',');
        cmd=cmd.split(':')[0].replace(' ','').toLowerCase();
    }
        
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

var select_elements=function(selector, params){
    var _function=function(){return false};
    switch(selector){
      case 'a':
          _function=function() {
              return (this.innerHTML.toLowerCase().indexOf(params[0].toLowerCase())>=0)
          };
          break;
      case ':button':
      case ':submit':
          _function=function() {
              return ($(this).val().toLowerCase().indexOf(params[0].toLowerCase())>=0)
          };
          break;
      case ':checkbox':
      case ':radio':
          _function=function() {
              return (($(this).attr('name') && $(this).attr('name').toLowerCase().indexOf(params[0].toLowerCase())>=0)
                      || ($(this).attr('id') && $(this).attr('id').toLowerCase().indexOf(params[0].toLowerCase())>=0)
                      || ($(this).attr('value') && $(this).attr('value').toLowerCase().indexOf(params[0].toLowerCase())>=0))
          };
          break;
      case ':text':
      case 'textarea':
      case 'select':
      case 'input':
          _function=function() {
              return (($(this).attr('name') && $(this).attr('name').toLowerCase().indexOf(params[0].toLowerCase())>=0)
                      || ($(this).attr('id') && $(this).attr('id').toLowerCase().indexOf(params[0].toLowerCase())>=0))
          };
          break;
    }
    
    return $(selector).filter(_function);
};


var trigger_click=function(el, selector){
    switch(selector){
        case 'a':
            /* why this not working: $(el).trigger('click'); ? */
            if ($(el)[0].href.indexOf('javascript:')==0){
                eval($(el)[0].href.substring('javascript:'.length));
            }
            else {
                /* _no history_ alternative: window.location.replace(el.href); */
                window.location=$(el)[0].href;
            }
            return true;
            break;
        case ':button':
        case ':submit':
        case ':checkbox':
        case ':radio':
            $(el).trigger('click'); //return {'_fct' : $(el)[0].trigger, 'args' : ['click']};
            return true;
            break;
        case ':text':
        case 'textarea':
        case 'select':
        case 'input':
            $(el)[0].focus(); //return {'_fct' : $(el)[0].focus, 'args' : []};
            return true;
            break;
    }
};

/* to attempt finding and triggering the page element given in the command */
var click=function(cmd){
    params=null;
    if (cmd.split(':').length>1)
        params=cmd.split(':')[1].split(',');
        cmd=cmd.split(':')[0].toLowerCase();
        
    switch(cmd){
        default:  {
            /* 'a', 'button', 'link', 'go', 'goto', 'click' */
            if (params==null){
                params=new Array();
                params[0]=cmd;
            }
            var el=null;
            
            var selectors=['a', ':button', ':submit', ':checkbox', ':radio', 'select', ':text', 'textarea', 'input'];
            var i=0;
            while((el==null || $(el).length==0) && i<selectors.length){
              var selector=selectors[i];
              if ($(selectors[i]).length>0){
                el=select_elements(selectors[i], params);
              }
              
              if ($(el).length>0){
                  return trigger_click(el, selector);
              }
              i++;
            }
            break;
        }
    }
};

var _cmd_history=[];
var set_cmd_history=function(val){
    if (val && val!=''){
      var do_set=true;
      var h_cur=parseInt($('#_cmd_history_cur').val());
      
      /* check adjacent history values */
      for(var i=h_cur-1;i<=h_cur+1;i++){
        if (i>=0 && i<_cmd_history.length && val==_cmd_history[i]){
            do_set=false;
            $('#_cmd_history_cur').val(i);
            break;
        }
      }
      
      if (do_set){
          /* insert in 
              to do: javascript array insertAt instead...
          */
          if (h_cur>=0 && h_cur<_cmd_history.length-1){
              var _c_h=_cmd_history;
              _cmd_history=[];
              for(var i=0;i<_c_h.length;i++){
                  if (i==h_cur+1){
                      _cmd_history.push(val);
                      h_cur++;
                      i--;
                  }
                  else {
                      _cmd_history.push(_c_h[i])
                  }
              }
          }
          else {
              _cmd_history.push(val);
              h_cur=parseInt($('#_cmd_history_cur').val())+1;
          }
          $('#_cmd_history_cur').val(h_cur);
      }
    }
};

var walk_cmd_history=function(walk){
    var cur=parseInt($('#_cmd_history_cur').val());
    if (cur+walk>=0 && cur+walk<_cmd_history.length){
      var h_val=_cmd_history[cur+walk];
      if (h_val) {
          $('#_cmd').val(_cmd_history[cur+walk]);
          $('#_cmd_history_cur').val(cur+walk);
      }
    }
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
    
    $('#_cmd').bind('keyup', function(e){
        /* mozilla fix */
        if ($.browser.mozilla){
            if((e.keyCode ? e.keyCode : e.which) == 13) {
                on_cli_web_submit();
            }
        }
        
        /* history */
        var e_k_c=(e.keyCode ? e.keyCode : e.which);
        switch(e_k_c){
            case 38: walk_cmd_history(-1); break;
            case 40: walk_cmd_history(+1); break;
        }
    });

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
    /* history */
    set_cmd_history($('#_cmd').val());

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
        
        /* assumptions */
        if (rv==cec_rv || eval(rv)==rv){
            /* assumption: element focus */
            rv=focus($('#_cmd').val());
            
            if (!rv){
                /* assumption: element click */
                rv=click($('#_cmd').val());
            }
        }
        
        /* last chance... */
        /* last chance function... */
        try{ 
            if (!rv){
              var _fct=null;
              if ('function'==typeof rv && eval(rv)==rv) _fct=rv;
              if (_fct){
                  _fct=_fct;
                  _fct();
                  rv=true;
              } 
            } 
        }
        catch(e){
        }
        
        if (rv) {
            if ($('#_cmd_msg').html().indexOf('done')>=0){
            
                var regexS = "[\(]\d*[^\)]";
                var regex = new RegExp( regexS );
                var results = regex.exec($('#_cmd_msg').html());
              
                var n=parseInt(results[0].replace('(',''));
                var h=$('#_cmd_msg').html();
                $('#_cmd_msg').html(  h.replace('('+n+')','('+(n+1)+')')   );
            }
            else {
                $('#_cmd_msg').html('done (1)');
            }
        }
        else {
            $('#_cmd_msg').html('no command...');
            if (settings.google.search.loaded){
                $('#_cmd_msg').html('falling back to google search...');
                molhokwai.google.search.response.get(cmd.toString());
            }
        }
        
        $('#_cmd').val('');
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
