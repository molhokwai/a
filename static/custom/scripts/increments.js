var incrementsSettings = {
    elBaseName : 'nr'
};
var _is = incrementsSettings;

var callParams = function(_total){
  _total = _total ? _total : total();
  var rv = '?name=increments_white_woman_with_black_guy_flv'
          +'&data={'
          +'"'+_is.elBaseName+'":'+_total.toString()+','
          +'"u_last":"'+new Date().toString()+'"'
          +'}';
  return rv
};
var onNrTextChange = function(e){
  ajaxSave();
};
var ajaxRead = function(){
      $.ajax({
          url : '/a/data'
              + '/read?name=increments_white_woman_with_black_guy_flv',
          success : function(data){
              var json = eval('('+data+')');
              $('#'+_is.elBaseName+'').html(json.result.nr.toString());
              $('#'+_is.elBaseName+'_u_last').html(json.result.u_last.toString());
              $('#'+_is.elBaseName+'_msg').html('read done');
          },
          error : function(data){
              $('#'+_is.elBaseName+'_msg').html(data);
          }
      });
};
var ajaxSave = function(_total){
      $.ajax({
          url : '/a/data'
              + '/save'+callParams(_total),
          success : function(data){
              try{
                  var json = eval('('+data+')');
                  $('#'+_is.elBaseName+'').html(json.result.nr.toString());
                  $('#'+_is.elBaseName+'_u_last').html(json.result.u_last.toString());
                  $('#'+_is.elBaseName+'_text').val('');
                  $('#'+_is.elBaseName+'_msg').html('updated');
              }
              catch(e){
                  $('#'+_is.elBaseName+'_text').val('');
                  $('#'+_is.elBaseName+'_msg').html('updated. diplay process error:'+e.description);
              }
          },
          error : function(data){
              $('#'+_is.elBaseName+'_msg').html(data);
          }
      });
};
var total = function(){
  var n = parseInt($('#'+_is.elBaseName+'_text').val());
  n = !isNaN(n) ? n : 0;
  return parseInt($('#'+_is.elBaseName+'').html())+n;
};
$(document).ready(function(){
  $('#'+_is.elBaseName+'').bind('click', function(){
      var _t = parseInt($('#'+_is.elBaseName+'').html())+1;
      $('#'+_is.elBaseName+'').html(_t.toString());
      ajaxSave(_t);
  });
  $('#'+_is.elBaseName+'_text').bind('change', onNrTextChange);

  ajaxRead();
});
