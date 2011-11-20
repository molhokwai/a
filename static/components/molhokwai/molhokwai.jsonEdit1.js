/*#########################################################################################
## JSON EDITOR
##  -   Builds json tree and outputs it to before given element
##  -   Updates json data on change the fly
##  -   Updates given element on change the fly
##  
##  TO EVENTUALLY DO:
##  -   In net.molhokwai.js architecture
#########################################################################################*/

/*  ###################################
    PROCESS 
    ###################################*/

/* Make object out of atom passed 
   @params
       obj : the object
       oKe : list:
            -   function to make and output key representation DOM element
            -   optional extra params dictionary
       oAe : list:
            -   function to make and output atom (string, number) representation DOM element
            -   optional extra params dictionary
       l : level, depth, within the object
       p : the path to the current element
       index : the index of the atom to add (eventual) items delimiter if >0
       eps : extra parameters dictionary (see jsOtoS function for sample usage)
*/
var walk = function(obj, oKe, oAe, l, index, p, eps){
    if (l==null){ l=-1; }
    if (index==null){ index=0; }
    if (p==null){ p=[]; }

    var o = [];      
    if (typeof(obj) in {'number':'', 'string':''}){
        if (l+1<p.length){
            p.splice(l+1);
        }

        if (oAe){
            /*Refactoring: function get_eps(oAe|oKe, eps)*/
            var ep = oAe.length>1 ? oAe[1]: null;
            if(ep){
                if(eps){
                    for(k in ep){
                        eps[k] = ep[k];
                    }
                }
                else { eps = ep; }
            }
            o.push(oAe[0](obj, l, index, p, eps));
        }
        else{
            o.push(obj);
        }
    }
    else {
        l++;
        if($.isArray(obj)){
            var ol=obj.length;
            if(ol>1){
                /*Refactoring: hashtable 'class' usage */
                if(eps==null){ eps={}; }
                eps['l']={l:{'ol':ol}};
            }
            for(i in obj){
                if(l in p){ p[l]=i; }
                else { p.push(i); }
                o.push(walk(obj[i], oKe, oAe, l, i, p, eps));
            }
        }
        else if (typeof(obj) in {'object':''}){
            var i=0;
            var ol=0;
            var odl=eps && eps.odl? eps.odl : null;
            for(k in obj){ ol++; };
            /*Refactoring: function get_eps(oAe|oKe, eps)*/
            var ep = oKe.length>1 ? oKe[1]: null;
            if(ep){
                if(eps){
                    for(k in ep){
                        eps[k] = ep[k];
                    }
                }
                else { eps = ep; }
            }
            if(ol>1){
                /*Refactoring: hashtable 'class' usage */
                if(eps==null){ eps={}; }
                eps['l']={l:{'ol':ol}};
            }
            for(k in obj){
                if(l in p){ p[l]=k; }
                else { p.push(k); }
				if(odl){
                    o.push(
                        (i==0?odl[0]:'')
                        +oKe[0](k, l, i, p, eps)
                        +odl[1]
                    );
                    o.push(
                        walk(obj[k], oKe, oAe, l, i, p, eps)
                        +(i==ol-1?odl[2]:
                            (ol>1?odl[3]:''))
                    );
                }
				else if (eps && eps.HTML){
					var _o = oKe[0](k, l, i, p, eps);
					_o.appendChild(
						walk(obj[k], oKe, oAe, l, i, p, eps)
					);
					o.push(_o);
				}
                else {
                    o.push(oKe[0](k, l, i, p, eps));
                    o.push(walk(obj[k], oKe, oAe, l, i, p, eps));
                }
                i++;
            }
        }
    }
    
    var jrv = eps && eps.jrv;
    if(jrv!=null){
        return o.join(jrv);
    }
    else {
        return o;
    }
};

/* Handled HTML tags */
var hHTMLTagsRegExps = [/a/, /blockquote/, /div/, /h\d/, /li/, /ol/, /p/, /span/, /ul/];
/* Make object out of atom passed 
   @params
       a : atom (string, number)
       l : level, depth, within the object
       index : the index of the atom to add (eventual) items delimiter if >0
       p : the path to the element
       eps : extra parameters dictionary
            - ['ebs'] : event bindings tuples list ([['jquery event bind name', function]])
*/
var mAe = function(a, l, index, p, eps){
    var t=null;
    if(typeof(a)=='string' && a.length<50 || (typeof(a)=='number')){
        var t=document.createElement('input');
        t.type='text';
        t.className='';
    }
    else if(typeof(a)=='string' && a.length>=50){
        var t=document.createElement('textarea');
        t.className='wymeditor ';
    }
    
    if(t){
        if (p){
            t.id = p.join('#:#');
        }

        $(t).val(a);
        if (t.type=='textarea'){
            $(t).html(a);
        }

        t.className+='a-level '+'l_'+l +' '+ 'a-index '+'i_'+index;
        if (eps){
            for(k in eps){
                if(k=='mAe_ebs'){
                    var ebs=eps[k];
                    for(i in ebs){
                        $(t).bind(ebs[i][0], ebs[i][1]);
                    }
                }
            }
        }
    }
    return t;
};
/* Make js string out of atom passed 
    +(see previous method for comments)
*/
var mAjs = function(a, l, index, p, eps){
    var ol=(eps && eps.l && eps.l[l] ? eps.l[l].ol : null);

    var t=typeof(a);
    a=(t=='string'?fs(a):a);
    var q=(t=='number'?'':'"');
    var v=q+a+q;

    if(ol && ol>1 && index>0){ v=','+v; }
    if(ol && ol>1 && index==ol-1){ eps.l[l].ol=null; }
    return v;
};

/* Make object out of key passed
   @params
       k : (dict)key object
       l : level, depth, within the object
       index : the index of the atom to add (eventual) items delimiter if >0
       p : the path to the element 
       eps : extra parameters 
            - ['ebs'] : event bindings tuples list ([['jquery event bind name', function]])
*/
var mKe = function(k, l, index, p, eps){
    var s = '';

    /* isHTMLTag: only closing and ending tag to set as eps.odl (object delimiter)
        for HTML tags generation */
    var isHTMLTag = false;
	if (!eps || !eps.HTML){
		for(i in hHTMLTagsRegExps){
			if (k.toString().match(hHTMLTagsRegExps[i])){
				isHTMLTag = true;
				break;
			}
		}
	}

    var _id = k+'-'+l+'-'+index; 
    if (p){
        _id = p.join('#:#');
    }
    var _className = 'k-level '+'l_'+l +' '+ 'k-index '+'i_'+index; 

    if(!isHTMLTag){
        s = document.createElement('span');
        s.id = _id;
        $(s).html(k);
        s.className = _className;
    }
    else {
        if (!eps){
            eps = {};
        }
        eps.odl = ['<'+k+' id="'+_id+'" class="'+_className+'">', 
                   '', '', '</'+k+'>'];
    }
    
    if (eps){
        for(k in eps){
            if(k=='mKe_ebs'){
                var ebs=eps[k];
                for(i in ebs){
                    $(s).bind(ebs[i][0], ebs[i][1]);
                }
            }
        }
    }
    return s;
};
/* Make js string out of atom (key) passed 
    +(see previous method for comments)
*/
var mKjs = function(a, l, index, p, eps){
    var q=typeof(a)=='number'?'':'"';
    var v=q+a+q;
    return v;
};

/* Update json object 
    jquery event handling function
*/
var ujsO = function(){
    var p = '["' + $(this)[0].id.split('#:#').join('"]["') +'"]';
    var q = '"';
    if(typeof(v)=='number'){ q=''; }
    var v = q+fs($(this).val())+q;
    eval('jsO'+p+'='+v);
    jsS.val(jsOtoS(jsO));
};

/*  ###################################
    UTILITITES
    ###################################*/

/* Format string for eval 
       s : the string 
*/
var fs = function(s){
    while(s.indexOf('\n')>=0){
        s=s.replace('\n','    ');
    }
    var n=-1;
    var ip=0; 
    while(s.indexOf('\n')>=0){
        s=s.replace('\n','');
    }
    while(s.indexOf('\r')>=0){
        s=s.replace('\r','');
    }
    while(s.indexOf('"', ip)>=0){
        s=s.substring(0,ip)+s.substring(ip,s.length-1).replace('"','\\"');
        ip=s.indexOf('"',ip)+2;
    }
    return s;
};

/* Flush recursive list
   @params
       L : list
       ff : flush function
       RLf : Recursive List flush    
*/
var fRL = function(o,RLf){
    if ($.isArray(o)){
        for(i in o){
            RLf.push(fRL(o[i],RLf));
        }
    }
    else{
        return o;
    }
};

/* Levels & Indexes display
   @params
       s : selector
*/
var LId = function(s){
    $(s).children().each(function(){
        var m = $(this)[0].className.match(/level\s*(\-?\+?\d*)/);
        if(m){
            $(this).animate({marginLeft : '+='+Math.abs(parseInt(m[1]))*5+'%'});
        }
    });
};

/* Json Object to string
   @params
       jsO : the jsO object
*/
var jsOtoS = function(jsO){
    return walk(jsO, 
        [mKjs], 
        [mAjs],
        null, null, null,
        {
            'HTML': false,
            'odl':['{',':','}',','],
            'jrv' : ''
        }
    );
};
/* Json Object to HTML
   @params
       jsO : the jsO object
*/
var jsOtoHTML = function(jsO){
    return walk(jsO, 
        [mKjs], 
        [mAjs],
        null, null, null,
        {
            'HTML': true,
            'jrv' : ''
        }
    );
};

/* Update Json Source 
*/
var ujsS = function(){
    jsS.val(jsOtoS(jsO));
};

var RLf = [];
var jsO = {};
var jsS = null;
var jsT = null;

var onjsSChange = function(e){
    jsTb();
};
var jsTb = function(si, di, options){
    if(!jsS){
        if (!si || !di){
            throw "source id (si) and destination id (di) required for function jsTb  call";
        }
        jsS = $('#'+si);
        jsS.bind('change', onjsSChange);
    }
    try{
        jsO = eval('('+jsS.val()+')');
    }
    catch(e){
        jsO = $.parseJSON(jsS.val());
    }
        
    var eL = walk(
        jsO, 
        [(options && options.makeKeyEntity ? options.makeKeyEntity : mKe), {}], 
        [(options && options.makeAtomEntity ? options.makeAtomEntity : mAe), {
            'mAe_ebs' : [['change', ujsO]]
        }]
    );
    RLf = [];
    fRL(eL, RLf);
    
    if(!jsT){
        if (!si || !di){
            throw "source id (si) and destination id (di) required for function jsTb  call";
        }
        jsT = document.createElement('div');
        jsT.id = di;
        jsT.className = 'width100pc';
        $('#'+si).before(jsT);
        jsT = $('#'+di);
    }
    else{
        jsT.html('...');
    }

    for(i in RLf){
        jsT.append(RLf[i]);
    }
    LId('#'+di);
}
