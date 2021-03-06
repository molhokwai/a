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
