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
                if (typeof($($('form:visible:last')).formFirstField)=='function'
                     && $($('form:visible:last')).formFirstField()) {
                    $($('form:visible:last')).formFirstField().focus();
                }
                else {
                    if (document.getElementById('_cmd')){
                        document.getElementById('_cmd').focus();                    
                    }
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
              return ($(this).text().toLowerCase().indexOf(params[0].toLowerCase())>=0)
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
    if (cmd.split(':').length>1){
        params=cmd.split(':')[1].split(',');
    }
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


/* caught eval to more or less brutally evaluate the given command,
    catch any (probable) exception, and continue
*/
var cec_rv='boom, crashshsh...';
var caught_eval=function(value){
    try{
        var e_v=eval(value);
        if (typeof(e_v)=='function'){
            return e_v();
        }
        else{
            return e_v;
        }
    }
    catch(e){
        return cec_rv;
    }
};

/* ci web */
var cli_web_registered = [];
var cli_web_register = function(_fct){
    cli_web_registered.push(_fct);
};

/* Ctrl+S event: 'submit' and cli web submit */
shortcut.add("Ctrl+S",function() {
    $('#_cmd').val('submit');
    on_cli_web_submit();
},{
    'type':'keydown',
    'propagate':false,
    'target':document
});

/* Ctrl+E event: 'edit' and cli web submit */
shortcut.add("Ctrl+E",function() {
    $('#_cmd').val('edit');
    on_cli_web_submit();
},{
    'type':'keydown',
    'propagate':false,
    'target':document
});

/* Ctrl+O event: 'view' and cli web submit */
shortcut.add("Ctrl+O",function() {
	if ($('#_cmd_msg a').length>0 
		&& $('#_cmd_msg a').html().indexOf('view')>0){
    	$('#_cmd').val('view');
	}
	else if ($('#posts_post_title').length>0 
		&& $('#posts_post_title').val().length>0){
    	$('#_cmd').val($('#posts_post_title').val());
	}
    on_cli_web_submit();
},{
    'type':'keydown',
    'propagate':false,
    'target':document
});

/* on_cli web submit event handler */
var on_cli_web_submit=function(){
    /* history */
    set_cmd_history($('#_cmd').val());
    var cmd_msg = '';
    var output = '';
    var rv = false;
    
    /* >>(command) for direct server call */
    if ($('#_cmd').val().substring(0,2)=='>>'){
        $.getJSON(
            $('#_cmd').val().replace(' ','/'),
            function(json){
                var status = json.status;
                output = json.output
                cmd_msg = json.message + ' ('+json.result+')';
                rv = true;            
            }
        );
    }
    
    /* >(command) for direct server call */
    if ($('#_cmd').val().substring(0,1)=='>'){
        /* nothing yet */
    }
    
    /* quick fix */
    if ($('#_cmd').val()=='home'){ $('#_cmd').val('root');}

    /* FIRST: RAW EVAL ATTEMPT */
    try {
        /* raw eval */
        rv=caught_eval($('#_cmd').val());
        
        /* added 'punctuation' eval */
        if (rv==cec_rv){
            rv=caught_eval($('#_cmd').val().replace(' ', '.'));
        }

        /* added 'punctuation' & method last eval */
        if (rv==cec_rv){
            rv=caught_eval($('#_cmd').val().replace(' ', '.')+'()');
        }

        /* added 'underscore' & method, with last item as parameter eval */
        if (rv==cec_rv){
            var mp = $('#_cmd').val().split(' ');
            var l = mp.length;
            var e_s = '';
            for(i in mp){
                e_s += mp[i];
                if (i<l-2){ e_s += '_'; }
                else if (i==l-1){ e_s = '("'+e_s+'")'; }
            }
            rv=caught_eval(e_s);
        }
        

        /* THEN: REGISTERED FUNCTIONS ASSUMPTIONS */
        if (rv==cec_rv || rv == $('#_cmd').val()){
            if (cli_web_registered.length>0){
                var i=0;
                rv = false;
                while(!rv && i<cli_web_registered.length){
                    /*continue*/
                    rv = cli_web_registered[i]($('#_cmd').val());
                    i++;
                }
                if (!rv) rv = cec_rv;
                else {
                    if ($('#_cmd_msg').html().indexOf('-with google translate-')<0){
                        cmd_msg += ' -with google translate-';
                    }
                }
            }
        }
                
        /* THEN: PAGE CONTENT BASED ASSUMPTIONS */
        /* assumptions */
        var x=rv;
        var or=false; // XOR
        try{ or=eval(rv)==rv; }catch(e){}
        if (rv==cec_rv || ((!x && or) || (x && !or))){
            /* assumption: element focus */
            rv=focus($('#_cmd').val());
            
            if (!rv){
                /* assumption: element click */
                rv=click($('#_cmd').val());
            }
        }
        var pages_match = function(val){
            /* THEN: APPLICATION/SYSTEM CONTENT BASED ASSUMPTIONS */
            /* page title match */
            var _pages_match={};
            for(_id in server.pages){
                var s_p_i_p_t=server.pages[_id].post_title;
                var index=s_p_i_p_t.toLowerCase().indexOf(val);
                if (index>=0){
                    _pages_match[s_p_i_p_t.toLowerCase()]=index;
                }
            }
            var p_match=null;
            var i_match=-1;
            for(p_t in _pages_match){
                if(_pages_match[p_t]>=i_match){
                    i_match=_pages_match[p_t];
                        p_match=p_t;
                }
            }
            if(i_match>=0 && p_match){
                return '/'+server.request.application+'/default/page/'+p_match;
            }
            else {
                return null;
            }
        };
        var p_m_val = $('#_cmd').val().toLowerCase();
        rv = pages_match(p_m_val);        
        rv = !rv ? pages_match(p_m_val.replace(' ', '_')) : rv;
        var p_m_vals = p_m_val.split(' '); var i = 0;
        while(!rv && i<p_m_vals.length){
            rv = !rv ? pages_match(p_m_vals[i]) : rv;
            i++;
        }
        if (rv) {
            window.location = rv;
            return
        }
        
        /* FINALLY: LAST CHANCE... */
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
                $('#_cmd_msg').html(  h.replace('('+n+')','('+(n+1)+')') + cmd_msg );
            }
            else {
                $('#_cmd_msg').html('done (1)' + cmd_msg);
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
