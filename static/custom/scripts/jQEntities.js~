/*************
  context : 
  Dynamic pages entities' display
**************/
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

