/* method executed on page load, through:
    .../components/net.molhokwai/molhokwai.common.js */
var onPageLoad = function(){
  /* theme first display fix */
  var doRedirect = false;
  var urlParams = window.location.search.split('&');
  var newUrlParams = [];
  for(var i=0;i<urlParams.length;i++){
      var indTh = urlParams[i].indexOf('theme=');
      if(indTh!=1){
          newUrlParams.push(urlParams[i]);
      }
      else {
          doRedirect = true;
      }
  }
  if (doRedirect){
      var url = window.location.pathname;
      for(var i=0;i<newUrlParams.length;i++){
          if (i==0){ url+='?'; }
          else{ url+='&'; }
          url += newUrlParams[i];
      }
      window.location = url;
  }
}

/* configuration & settings */
settings={
       wymeditor:{
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
    },

    /* JQUERY SIZING & STYLING */
	jQs : [
		[new RegExp("(width|w|large)([0-9].)(em|mm|px|pt|%)[^\s]"),'width'],
		[new RegExp("(height|h|long)([0-9].)(em|mm|px|pt|%)[^\s]"),'height'],
		[new RegExp("(margin-left|margl|ml|left,l)([0-9].)(em|mm|px|pt|%)[^\s]"),'margin-left'],
		[new RegExp("(margin-right|margr|mr|right,r)([0-9].)(em|mm|px|pt|%)[^\s]"),'margin-right'],
		[new RegExp("(margin-top|margt|mt|top,t)([0-9].)(em|mm|px|pt|%)[^\s]"),'margin-top'],
		[new RegExp("(margin-bottom|margb|b|bottom,b)([0-9].)(em|mm|px|pt|%)[^\s]"),'margin-bottom'],
		[new RegExp("(padding-left|padl|pleft|pl)([0-9].)(em|mm|px|pt|%)[^\s]"),'padding-left'],
		[new RegExp("(padding-right|padr|pright|pr)([0-9].)(em|mm|px|pt|%)[^\s]"),'padding-right'],
		[new RegExp("(padding-top|padt|ptop|pt)([0-9].)(em|mm|px|pt|%)[^\s]"),'padding-top'],
		[new RegExp("(padding-bottom|padb|pbottom|pb)([0-9].)(em|mm|px|pt|%)[^\s]"),'padding-bottom'],
		[new RegExp("(float-left,left|l)[^\s]"),'width'],
		[new RegExp("(float-right,right|r)[^\s]"),'width'],
		[new RegExp("(float-left,left|l)[^\s]"),'width'],
		[new RegExp("(float-left,left|l)[^\s]"),'width'],
		[new RegExp("(float-left,left|l)[^\s]"),'width'],
		[new RegExp("(float-left,left|l)[^\s]"),'width'],
		[new RegExp("(width|w|large)([0-9].)(em|mm|px|pt|%)[^\s]"),'width'],
		[new RegExp("(width|w|large)([0-9].)(em|mm|px|pt|%)[^\s]"),'width'],
		[new RegExp("(width|w|large)([0-9].)(em|mm|px|pt|%)[^\s]"),'width'],
		[new RegExp("(width|w|large)([0-9].)(em|mm|px|pt|%)[^\s]"),'width'],
		[new RegExp("(width|w|large)([0-9].)(em|mm|px|pt|%)[^\s]"),'width'],
		[new RegExp("(width|w|large)([0-9].)(em|mm|px|pt|%)[^\s]"),'width'],
		[new RegExp("(width|w|large)([0-9].)(em|mm|px|pt|%)[^\s]"),'width'],
		[new RegExp("(width|w|large)([0-9].)(em|mm|px|pt|%)[^\s]"),'width'],
		[new RegExp("(width|w|large)([0-9].)(em|mm|px|pt|%)[^\s]"),'width'],
	]
}

/* ... */
var markup_textareas=function(selector){
    if(selector){
        $(selector).wymeditor();
    }
    else{
        $('textarea').wymeditor();
    }
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
    /* CLI WEB */
    /* cli web dbl ctrl shortcut... */
    $('body').keyup(function(event){
      if (event.keyCode==17){
          if (ctrl_timeout!=null){
              $('#cli_web').show();
              $('#_cmd').focus();
          }
          ctrl_timeout=setTimeout('clearTimeout(ctrl_timeout); ctrl_timeout=null;', ctrl_max_interval);
      }
    });
    
    $('#_cmd').bind('keyup', function(e){
        if((e.keyCode ? e.keyCode : e.which) == 13) {
            on_cli_web_submit();
        }
        
        /* history */
        var e_k_c=(e.keyCode ? e.keyCode : e.which);
        switch(e_k_c){
            case 38: walk_cmd_history(-1); break;
            case 40: walk_cmd_history(+1); break;
        }
    });

    focus('form');

    /* GOOGLE TOOLS */
    /* search */
    if (settings.google.search.load){
        settings.google.search.loaded=google_search_load();
    }
    
    /* SERVER ATTRIBUTE */
    /* pages */
    $.getJSON(
        '/'+server.request.application+'/default/json/pages',
        function(json){
            if(json.status==1){
                server.pages=json.result;
            }
        }
    );

    /* JQUERY SIZING & STYLING */
    $('.jQs').each(function(){
        var l = [[new RegExp("(width|w|large)([0-9].)(em|mm|px|pt|%)[^\s]"),'width']
        /* 
          Further mapping required:
          '[new RegExp("([0-9].)(em|mm|px|pt|%)(width|w|large)[^\s]"),'width'] 
        */
        ];
        for(i in l){
            var m = l[i][0].exec($(this)[0].className);
            if(m && m.length>0){
                var s = $(this).attr('style');
                if(!s){
                    s = '';
                }
                $(this).attr({'style' : s + l[i][1]+':'+m[2]+m[3]+';'});
            }
        }
    });
    
});

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

        /* THEN: REGISTERED FUNCTIONS ASSUMPTIONS */
        if (rv==cec_rv){
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

        /* THEN: APPLICATION/SYSTEM CONTENT BASED ASSUMPTIONS */
        /* page title match */
        var pages_match={};
        for(_id in server.pages){
            var s_p_i_p_t=server.pages[_id].post_title;
            var index=s_p_i_p_t.toLowerCase().indexOf($('#_cmd').val().toLowerCase());
            if (index>=0){
                pages_match[s_p_i_p_t.toLowerCase()]=index;
            }
        }
        var p_match=null;
        var i_match=-1;
        for(p_t in pages_match){
            if(pages_match[p_t]>=0){
                if(i_match<0 || (pages_match[p_t]<i_match)){
                    i_match=pages_match[p_t];
                    p_match=p_t;
                }
            }
        }
        if(i_match>=0 && p_match){
            rv=true;
            window.location='/'+server.request.application+'/default/page/'+p_match;
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


var entities = {
    'display' : {
        '_do' : function(sel){
            if(sel==null){ sel='.display'; }
            
            $(sel).each(function(){
                /* to format/correct the html for processing */
                $(this).html($(this).html());
                
                var args = $(this).html().split('#:#');
                var i=0;
                var rm=true;
                while(i<args.length){
                    if(rm){
                        args = args.splice(i);
                        if(args[0]=='display'){ rm=false};
                        i++;
                    }
                    else{
                        var f=args[1];
                        var text=args[2];
                        var l=parseInt(args[3]);
                        /* callback_array not used */
                        var cb_array=null;
                        if(args.length>4){ cb_array=eval(args[4]); }
                        switch(f){
                            case 'truncate':
                                if(text.length>l){
                                    $(this).html($(this).html().replace('#:#'+text, text.substring(0,l)+'...'));
                                }
                                else{
                                    $(this).html($(this).html().replace('#:#'+text, text));
                                }
                                break;
                        }

                        for(var j=0;j<args.length;j++){
                            $(this).html($(this).html().replace('#:#'+args[j],''));
                        }
                        i=args.length;
                    }
                }
            });
        }
    }
};



/*************
  context : 
  lie search
**************/
/* thanks to: http://web2pyslices.com/main/slices/take_slice/51 */
var liveSearch = {
    'containerSelector' : {
        'results' : '#ajaxresults',
        'clearPanel' : '.left_content'
    },
    'results' : [],
    'clearPanelHtml' : '',
    'getData' : function(url, value){
        if(value != ""){
            $(liveSearch.containerSelector.results).show();
            $.getJSON(url,{'partialStr':value},function(json){
                if (liveSearch.results.length==0){
                    if(liveSearch.containerSelector.clearPanel){
                        liveSearch.clearPanelHtml = $(liveSearch.containerSelector.clearPanel).html();
                        $(liveSearch.containerSelector.clearPanel).html('');
                        
                        var div=document.createElement('div');
                        div.id='ajaxresults';
                        $(liveSearch.containerSelector.clearPanel).append(div);
                    }
                }
                
                var rmIndexes = [];
                for(i in json.result){
                    for(j in liveSearch.results){
                        if(json.result[i]==liveSearch.results[j]){
                            rmIndexes.push(i);
                            break;
                        }
                    }
                }
                
                for(i in rmIndexes){
                    json.result.splice(rmIndexes[i],rmIndexes[i]);
                }                
                
                var html='';
                var l=liveSearch.results.length;
                for(i in json.result){
                    var _id='liveSearch_results'+(l+i);
                    json.result[i]=json.result[i].replace('#id', _id)
                    liveSearch.results.push(json.result[i]);
                    $(liveSearch.containerSelector.results)[0].innerHTML+=json.result[i];
                    entities.display._do('#'+_id)
                }
            });
        }
    }   
};


/*************
  context : browser
  utilities
**************/

/* convenience (for cli_web also) methods */
var back=b=function(){
  history.go(-1);
  return true
}
var forward=fwd=f=function(){
  history.go(+1);
  return true
}
var exit=quit=q=function(){
  self.opener=self;
  self.close();
  return true
}
