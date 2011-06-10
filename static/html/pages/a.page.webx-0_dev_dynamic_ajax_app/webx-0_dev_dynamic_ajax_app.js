/* CLIENT SIDE */
var patterns : {
};

patterns['list'] = {
	/* @params:
			name: 'sites' | | 'pages' | 'sequences'
			urls : placeholder urls (see patterns.list.display...)
	 */
	onDocumentReady : function(params){
		patterns.list.manage.config.name = params.name;
        if(params.urls){
		    patterns.list.manage.config.urls = params.urls;
        }
		

		patterns.list.properties.user = ajax.users.get({ which:'current' });
		patterns.list.properties.value = patterns.list.get({ 
				what : 'list', 
				user : patterns.list.properties.user 
		});
	};

	manage : { 
    	config : {
        	name : 'sites',
        	urls : {
				'create' : 'javascript:patterns.list.display({what: "create", obj : patterns.list.get({what:"template"}) });',
				'read' : 'javascript:patterns.list.display({what: "read", obj : patterns.list.element.get(this.id) });',
				'update' : 'javascript:patterns.list.display({what: "update", obj : patterns.list.element.get(this.id) });',
				'delete' : 'javascript:patterns.list.display({what: "delete", obj : patterns.list.element.get(this.id) });',
			}
    	},

		properties : {
			user : null,
			list : null,
			template : null
		}
	},

	/* Singletons */
	/* @params:
			what: 'template' | 'list' | 'element'
			optional user: current user (session | cookie)
	 */
	get : function(params){
		if (!patterns.list.properties[params.what]){
			var name = pattern.list.manage.config.name; 
			patterns.list.properties[params.name] = ajax.flow[name]get(params); 
		}
		return patterns.list.properties[params.name];
	},

	/* Singletons */
	/* @params:
			what: 'template' | 'list' | 'element'
			optional user: current user (session | cookie)
	 */
    element : {
	    get : function(params){
            /* browse list */
	    }
    },

	/* @params:
			what: 'list'
			crud: 'create' | 'read' | 'update' | 'delete'
			optional user: current user (session | cookie) 
	 */
	crud : function(params){
		var name = pattern.list.manage.config.name;

        /* CRUD 
			test json RPC: 15MNS.
		   	If no:
				Implement methods in flow */
		return ajax.flow[name][params.crud](params);
	},

	/*
		@params
			what : 'list' | 'new' | 'edit' | delete
			obj : json list | json object
	*/
	display : function(params){
		/* LIST:
			test jquery: 15MNS.
		   	If no:
				parse json, display list */
		
		/* FORM */
		patterns.list.generate.form();
	},

	generate : {
		form : function(){
			var template = pattern.list.manage.vars.template; 
			jsonToForm('form').generate(
    			template,
    			/* { callback : { method : { method parameters } } } */
                /* see crud setting (json rpc or callback... */
    			{ onCrud : { patterns.list.crud : { what:'list', crud : null } } }
			);
		}
	},
};


