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
/*  Flow class
    @type class
    @params (dictionary): {
        which : [name of an implemented flow, default flow, if empty]
    }              
*/
var Flow = function(params){
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

		if(this.params){
        	this.elements = new Elements({ elements : page[this.params.page].elements });
        	this.headerElements = new Elements({ elements : page.common.header.elements });
		}
    };
	if(this.params){
    	this.page = new Page(this.params);
	}

    var Form = function(params){
        this.params = params;

		this.submit = function(params){
			flow.flow(params);
		};
    };
	if(this.params){
    	this.form = new Form(this.params);
	}

    this.to = this.dbg;

	this.flow = function(params){
		var seq = null;
		for(k in params){
			if(!seq){
				seq = sequences[params[k]][l.push(k)];
			}
			else{
				seq = seq[params[k]][l.push(k)];
			}
		}
		
	};
};

var sequences = [
	{page: {
		"index" :
			{form : {
				"wantNeedHave" : 
					{page : {
						"wantNeedHaveResults" : {
						}
					}}
			}}
	}}
];

/*  Pages
    @type dictionary
*/
var page = {};
page['common'] = {
    header : {
        elements : [
			{'span' : {
				'attributes' : {
					'class' : 'jQs diblo w100% tac fstit',
					'innerHTML' : '(js based mockup, wireframes...)'
				}
			}},
            {'p' : {
                'attributes' : {
                    'class' : 'jQs tar margb-1.5% margr-3.5%',
                    'innerHTML' : 'Hello&nbsp;'
                },
                'children' : [
                    {'a' : {
                        'attributes' : {
                            'class' : 'jQs flr',
                            'href' : 'javascript:flow.to({page:"LoginPage"});',
                            'innerHTML' : '?'
                        }
                    }}
                ]
            }}
        ]
    }
};

page['index'] = {
    elements : [
        {'form' : {
            'attributes' : {
                'id' : "wantNeedHave",
                'name' : "wantNeedHave",
                'class' : 'jQs clbo'
            },
            'children' : [
                {'p' : {
                    'attributes' : {
                        'innerHTML' : 'Your request/command:'
                    }
                }},
                {'textarea' : {
                    'attributes' : {
                        'class' : 'out-grey jQs bcotransparent co#AAA5A5',
                        'innerHTML' : 'Want a Vegan Macadamia Nu Brittle Ice...'
                    }
                }},
                {'p' : {
                    'attributes' : {
                        'class' : 'jQs tar w70% margl35%'
                    },
                    'children' : [
                        {'input' : {
                            'attributes' : {
                                'type' : 'button',
                                'value' : 'Submit: click to submit, or double tap the Ctrl key and type submit',
                                'onclick' : onSubmit,
                                'class' : 'display-block jQs padv0.5% bcotransparent co#FFFCFA' 
                            }
                        }}
                    ]
                }}
            ]
        }}
    ]
};


page['wantNeedHaveResults'] = {
    elements : [
        {'div' : {
            'attributes' : {
                'id' : "results",
                'name' : "results",
                'class' : 'jQs clbo'
            },
            'children' : [
                {'p' : {
                    'attributes' : {
                        'innerHTML' : 'Found 1 offering:'
                    }
                }},
                {'ul' : {
                    'attributes' : {
                    },
                    'children' : [
                        {'li' : {
                            'attributes' : {
                                'innerHTML' : 'Adress: Found none',
                                'class' : 'jQs padv0.5% co#AAA5A5', 
                                'style' : 'list-style-type:none;'
                            }
                        }},
                        {'li' : {
                            'attributes' : {
                                'innerHTML' : 'Location: (lat, long)',
                                'class' : 'jQs padv0.5% co#AAA5A5', 
                                'style' : 'list-style-type:none;'
                            }
                        }},
                        {'li' : {
                            'attributes' : {
                                'innerHTML' : 'Description: We make Macadamia Nu Brittle Vegan Ice based on the recipe kindly provided to us by the creators...'
												+'It tastes different (of course), but if you love the original, you\' love this one... we love it...',
												+'<br/>You can find our recipe here (---), or come enjoy it with... ',
                                'class' : 'jQs padv0.5% co#AAA5A5', 
                                'style' : 'list-style-type:none;'
                            }
                        }}
                    ]
                }},
                {'p' : {
                    'attributes' : {
                        'innerHTML' : 'Found 1 recipe (ingredients, preparation):'
                    }
                }},
                {'ul' : {
                    'attributes' : {
                    },
                    'children' : [
                        {'li' : {
                            'attributes' : {
                                'innerHTML' : 'Ingredients: 1L soy milk, vnnilla, white sugar, brown sugar...' 
												+'<br/>Preparation: Pour the soy milk into... ',
                                'class' : 'jQs padv0.5% co#AAA5A5', 
                                'style' : 'list-style-type:none;'
                            }
                        }}
                    ]
                }}
            ]
        }}
    ]
};

