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
    }
};

/* ... */
var markup_textareas=function(selector){
    if(selector){
        $(selector).wymeditor();
    }
    else{
        $('textarea').wymeditor();
    }
};

/* ... */
var vi_textarea=function(selector){
    if(selector){
       editor($(selector)[0]);
    }
    else{
       editor($('textarea')[0]);
    }
};

/* Convenience _namespace_ */ 
var application = {
	UI : {
		Elements : {
			show : function(params){
				$(params.selector).show(params.how);
			},

			hide : function(params){
				$(params.selector).hide(params.how);
			},

			translateElement : {
				show : function(){
					application.UI.Elements.show({selector:'#google_translate_element', how:'slow'});
				},

				hide : function(){
					application.UI.Elements.hide({selector:'#google_translate_element', how:'slow'});
				}
			}
		}
	}
};


/* ... */
var wrapperWidth=function(e){
    var winW = $(window).width();
    var wrapW = '60%';
    if(winW<1680 && winW>=1200){
        wrapW = '70%';
    } else if(winW<1200 && winW>=1024){
        wrapW = '80%';
    } else if(winW<1024){
        wrapW = '80%';
    }
    if($('#wrapper').width()>winW){
        $('#wrapper').width(winW - 50);
    }
};


/*************
  context : 
  live search
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
  context : 
  search in pages
**************/
var search = find_in_pages = search_in_pages = in_pages = function(text){
   molhokwai.util.object.walk(
	   server.pages, 
	   null, 
	   [function(v, p){
		   if (v.post_text.toLowerCase().indexOf(p.text.toString().toLowerCase())>0){
			   var a = document.createElement('a');
			   a.href = '/'+server.request.application+'/default/page/'+v.id;
			   a.target = '_blank';
			   a.innerHTML = v.post_title + ' ';
			   $("#_cmd_result_msg").append(a);
		   }
	   },
	   {'text':text}
	   ]
   );
   return true
};


/*************
  context : browser
  utilities
**************/

/* convenience (for cli_web also) methods */
var back=b=function(){
  history.go(-1);
  return true
};
var forward=fwd=f=function(){
  history.go(+1);
  return true
};
var exit=quit=q=function(){
  self.opener=self;
  self.close();
  return true
};
