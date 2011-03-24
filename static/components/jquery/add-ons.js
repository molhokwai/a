/* by Dan Kubb, from http://www.gerd-riesselmann.net/development/focus-first-form-field-with-jquery 
    with (minor) additions
*/
$.fn.offsetTop = function() {
  var e = this.get(0);
  if(!e.offsetParent) return e.offsetTop;
  return e.offsetTop + $(e.offsetParent).offsetTop();
};

$.fn.formFirstField = function() {
    var firstField;
    var _form=this;
    
    $.each([ 'input', 'select', 'textarea' ], function() {
      var field = $(this + ':visible:enabled:first', _form).get(0);
      if(field)
        if(!firstField || $(field).offsetTop() < $(firstField).offsetTop())
          firstField = field;
    });
    return firstField;
}

/* from: http://jquery-howto.blogspot.com/2009/09/get-url-parameters-values-with-jquery.html */
$.extend({
  getUrlVars: function(){
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
      hash = hashes[i].split('=');
      vars.push(hash[0]);
      vars[hash[0]] = hash[1];
    }
    return vars;
  },
  getUrlVar: function(name){
    return $.getUrlVars()[name];
  }
});
