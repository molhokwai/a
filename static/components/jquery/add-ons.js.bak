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
