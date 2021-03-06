var elements = {
	attributesMap : {
		'class' : 'className',
		'bind' : function(params){
			if(params.name.substring(0,2)=='on'){
				params.name = params.name.substring(2);
			}
			$(params.element).bind(params.name, params.value);
		},
		'click' : function(params){
			return elements.attributesMap.bind(params);
		},
		'onclick' : function(params){
			return elements.attributesMap.bind(params);
		},
		'change' : function(){ 
			return elements.attributesMap.bind(params);
		},
		'onchange' : function(){ 
			return elements.attributesMap.bind(params);
		}
	},

    generateTree : function(tree){
        var element = null;
		for(el in tree){
			var obj = tree[el];
			element = document.createElement(el);
			if('attributes' in obj){
				for(a in obj['attributes']){
					var attr = a;
					if(attr in elements.attributesMap){
						var eaM = elements.attributesMap;
						if(typeof(eaM[a])=='string'){
							attr = eaM[a];
							eval("element."+attr+"='"+obj["attributes"][a]+"';");
						}
						else if(typeof(eaM[attr])=='function'){
							eaM[attr]({"element":element, "name":a, "value":obj["attributes"][a]});
						}
					}
					else{
						eval("element."+a+"='"+obj["attributes"][a]+"';");
					}
				}
			}
			if('children' in obj){
				for(i in obj['children']){
					element.appendChild(elements.generateTree(obj['children'][i]));
				}
			}
		}
        return element;
    }
};

