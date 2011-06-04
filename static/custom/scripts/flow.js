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
    this.form = this.dbg;
    this.to = this.dbg;
};

