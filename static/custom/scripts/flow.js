/* THE SYSTEM, A PERFECT ONE: 
       FUNCTIONAL/TECHNICAL DETAILS
   --------------------------------  

   Choice of Technology
   --------------------
   1. Javascript, for fast prototyping.
   2. For implementation, depending on:
       - Importance of Speed
       - Importance of Architectural Consistency
       - Importance of _Server-Side-ability_
   : *PyJs*
*/
try{
	if(molhokwai){
		// just checking for existence
	}
	else {
		// 'blind' condition 
		var molhokwai = {};
	}
}
catch(e){
	var molhokwai = {};
}

molhokwai["flow"] = {
    /* Handlers */
	handlers : {
    	onSubmit : function(e){
        	molhokwai.flow.flow.form.submit(molhokwai.flow.flow.form.params);
        	return false;
		}
    },

    /* Container selector */
	container : '#elements',

    /* Utilites */
	utilities : {
    	addElements : function(_elements){
            $(molhokwai.flow.container).each(function(){
        		for(i in _elements){
					$(this).append(_elements[i]);
        		}
			});
		},
    	getElementsHtml : function(){
            return $(molhokwai.flow.container).html();
		},
    	clearElements : function(){
            $(molhokwai.flow.container).html("");
		}
    },

    /* Flow class instance */
    flow : null,

    /* State */
    State : {
			page : {
        	common : {
            	header : null
        	},
        	elements : null
    	}
	},

	History : [
	],

	onDocumentReady : function(params){
		var m_flow = molhokwai.flow;
        var flow = m_flow.flow = new m_flow.Flow(params);
		var State = m_flow.State;

        if(!State.page.common.header){
            State.page.common.header = flow.page.headerElements;
           	m_flow.utilities.addElements(State.page.common.header);
        }
        State.page.elements = flow.page.elements;
        m_flow.utilities.addElements(State.page.elements);

        rules.jQs.onDocumentReady();
    },


	/*  Flow class
    	@type class
    	@params (dictionary): {
        	which : [name of an implemented flow, default flow, if empty]
    	}              
	*/
	Flow : function(params){
		this.dbg = function(params){
		   var s='flow.[] params:\n';
		   var i=0;
		   for(k in params){
			   if(i>0){ 
				   s+='\n';
			   }
			   s+='\t'+ k +':'+ params[k];
			   i++;
		   }
		   window.alert(s);
		};

		this.params = params;

		var Page = function(params){
			this.params = params;

			var Elements = function(params){
				var elementTrees = params.elements;
				var _elements = [];
				for(i in elementTrees){
					_elements.push(elements.generateTree(elementTrees[i]));
				}
				return _elements;
			};

			var m_flow = molhokwai.flow;
			if(this.params){
				this.elements = new Elements({ elements : m_flow.page[this.params.page].elements });
				this.headerElements = new Elements({ elements : m_flow.page.common.header.elements });
			}
		};
		if(this.params){
			this.page = new Page(this.params);
		}

		var Form = function(params){
			this.params = params;

			this.submit = function(params){
				molhokwai.flow.flow.flow(params);
			};
		};
		if(this.params){
			this.form = new Form(this.params);
		}

		this.to = this.dbg;

		/*	Flow process according to given parameters 
			& configuration sequences
		
			@params:
				Parsing: into a dict list, in this order:
				[element l0, element l1, element l2] (l: level)
				Constraint: Keys expected in params: 
					-	page
					-	form
					-	others are grouped into 'element'
		*/
		this.flow = function(params){
			var m_flow = molhokwai.flow;
			var l = ['', '', ''];
			for(k in params){ 
				switch(k){
					case 'page': l[0] = params[k]; break;
					case 'form': l[1] = params[k]; break;
					default: l[2] = params[k]; break;
				}
			}

			var sequences = molhokwai.flow.sequences;
			var seq = null;
			for(k in sequences){
				if(k==l[0]){
					seq = sequences[k];
					for(var i=1;i<l.length;l++){
						seq = seq[l[i]];
					}
				}
			}
			for(e in seq){
				if(seq[e]=='page'){
					m_flow.History.push(
						{flow:m_flow, html:m_flow.utilities.getElementsHtml()}
					);
        			m_flow.utilities.clearElements();

        			m_flow.onDocumentReady({page:e});
				}
				if(typeof(seq[e])=='function'){
					seq[e](params);
				}
			}
		};
	}
};


