var elements = {
	attributesMap : {
		'class' : 'className',
		'onclick' : function(params){
			$(params.element).bind(params.name, params.value);
		},
		'onchange' : function(){ 
			return elements.attributesMap.onclick;
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
							eval("element."+eaM[attr]({"name":a, "value":obj["attributes"][a]})+";");
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

