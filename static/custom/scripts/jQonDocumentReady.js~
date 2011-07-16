

/* on document ready... */
$(document).ready(function(){
    /* CLI WEB */
    /* cli web dbl ctrl shortcut... */
    $('body').keyup(function(e){
      if ((e.keyCode ? e.keyCode : e.which) == 17){
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

    /* FORM */
    /* focus */
    focus('form');

    /* submit on Enter */
    $('form').each(function(){
        if($(this)[0].className.toLowerCase().indexOf('autonome')<0){
            var f = $(this);
            $(this).children().each(function(){
                if($(this)[0].type in {'text':'','password':''}){
                    $(this).bind('keyup', function(e){
                        if((e.keyCode ? e.keyCode : e.which) == 13) {
                            f.submit();
                        }
                    });
                }
            });
        }
    });

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
        /* 
          Further mapping required:
          '[new RegExp("([0-9].)(em|mm|px|pt|%)(width|w|large)[^\s]"),'width'] 
        */
        var s = rules.jQs._do($(this)[0].className);
        if($(this).attr('style')){
            s = $(this).attr('style') +' '+ s;
        }
        $(this).attr({'style' : s});
    });


    /* WRAPPER WIDTH
        Depending on themes, uncomment
    wrapperWidth(); 
    */
    $(window).resize(wrapperWidth);
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
