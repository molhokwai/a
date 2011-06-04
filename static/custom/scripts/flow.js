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
        this.elements = new Elements({ elements : page[this.params.page].elements });
        this.headerElements = new Elements({ elements : page.common.header.elements });
    };
    this.page = new Page(this.params);
    this.to = this.dbg;
};


/*  Pages
    @type dictionary
*/
var page = {};
page['common'] = {
    header : {
        elements : [
            {'p' : {
                'attributes' : {
                    'class' : 'jQs tar margb-1.5% margr-3.5%',
                    'innerHTML' : 'Hello '
                },
                'children' : [
                    {'a' : {
                        'attributes' : {
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
                'id' : "WantNeedHaveForm",
                'name' : "WantNeedHaveForm"
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
                                'onclick' : 'onSubmit();',
                                'class' : 'display-block jQs padv0.5% bcotransparent co#FFFCFA' 
                            }
                        }}
                    ]
                }}
            ]
        }}
    ]
};
