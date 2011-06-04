var elements = {
	attributesMap : {
		'class' : 'className'
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
						attr = elements.attributesMap[attr];
					}
					eval("element."+attr+"='"+obj["attributes"][a]+"';");
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

