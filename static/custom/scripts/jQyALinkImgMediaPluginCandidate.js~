/* YET ANOTHER PLUGIN CANDIDATE: A LINK IMG MEDIA */

/* yaimpcln : jQyALinkImgMediaPluginCandidateLongName
    You can always put everything in a 'namespace' (just a js 'dictionary' object, a js object),
    and change the variables names
    And also have these as options:
        -   #jQyALinkImgMediaPluginCandidate
        -   .jQyALinkImgMediaPluginCandidate
        -   yaimpclnImgSrc
 */
var yaimpclnHrefs = {};
var yaimpclnCallbacks = [];
$(document).ready(function(callback){
    $('.jQyALinkImgMediaPluginCandidate').each(function(){
        yaimpclnHrefs['yaimpclnImgSrc'+yaimpclnIV] = $(this)[0].href;
        yaimpclnIV++;
    });

    var yaimpclnIV = 0;
    $('.jQyALinkImgMediaPluginCandidate').each(function(){
        yaimpclnHrefs['yaimpclnImgSrc'+yaimpclnIV]=$(this)[0].href;
        $(this).bind('click', function(e){
            var _img = null;
            if($('#jQyALinkImgMediaPluginCandidate img').length){
                _img = $('#jQyALinkImgMediaPluginCandidate img')[0];
            } else {
                _img = $(document.createElement('img'))[0];
            }
            
            if($(_img).height()>10 && $(_img).width()>10){
                $('#jQyALinkImgMediaPluginCandidate').height($(_img).height());
                $('#jQyALinkImgMediaPluginCandidate').height($(_img).height());
            }
            else{
                $('#jQyALinkImgMediaPluginCandidate').height('620px');
                $('#jQyALinkImgMediaPluginCandidate').width('620px');
            }
            $('#jQyALinkImgMediaPluginCandidate').append(_img);
            _img.src = yaimpclnHrefs[$(this)[0].id];
            $('#jQyALinkImgMediaPluginCandidate').show('slow');
            
            for(i in yaimpclnCallbacks){
                yaimpclnCallbacks[i]();
            }
        });

        $(this)[0].id = 'yaimpclnImgSrc'+yaimpclnIV;
        $(this)[0].href = '#'+$(this)[0].id;
        yaimpclnIV++;                
    });
    $('#jQyALinkImgMediaPluginCandidate').hide();
});


