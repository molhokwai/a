try {
    molhokwai.util['google_trans'] = {
        /* for reference */
        'combo_html' : '<select class="goog-te-combo"><option value="">Select Language</option><option value="af">Afrikaans</option><option value="sq">Albanian</option><option value="ar">Arabic</option><option value="be">Belarusian</option><option value="bg">Bulgarian</option><option value="ca">Catalan</option><option value="zh-CN">Chinese (Simplified)</option><option value="zh-TW">Chinese (Traditional)</option><option value="hr">Croatian</option><option value="cs">Czech</option><option value="da">Danish</option><option value="nl">Dutch</option><option value="et">Estonian</option><option value="tl">Filipino</option><option value="fi">Finnish</option><option value="fr">French</option><option value="gl">Galician</option><option value="de">German</option><option value="el">Greek</option><option value="ht">Haitian Creole</option><option value="iw">Hebrew</option><option value="hi">Hindi</option><option value="hu">Hungarian</option><option value="is">Icelandic</option><option value="id">Indonesian</option><option value="ga">Irish</option><option value="it">Italian</option><option value="ja">Japanese</option><option value="ko">Korean</option><option value="lv">Latvian</option><option value="lt">Lithuanian</option><option value="mk">Macedonian</option><option value="ms">Malay</option><option value="mt">Maltese</option><option value="no">Norwegian</option><option value="fa">Persian</option><option value="pl">Polish</option><option value="pt">Portuguese</option><option value="ro">Romanian</option><option value="ru">Russian</option><option value="sr">Serbian</option><option value="sk">Slovak</option><option value="sl">Slovenian</option><option value="es">Spanish</option><option value="sw">Swahili</option><option value="sv">Swedish</option><option value="th">Thai</option><option value="tr">Turkish</option><option value="uk">Ukrainian</option><option value="vi">Vietnamese</option><option value="cy">Welsh</option><option value="yi">Yiddish</option></select>',

        'cli_web_register' : function(){
		    try {
			    cli_web_register(function(val){
			       val = val.toLowerCase();

			       var tokens=['lang:', 'language:', 'trans:', 'translate:'];
			       var token_found=false;
			       for(var i=0;i<tokens.length;i++){
				       if (val.indexOf(tokens[i])>=0){
						    token_found = true;
				       }
			       }
			       if (!token_found) return
				
			       var $combo = $('select.goog-te-combo');
			       for(var i=0; i<$combo[0].options.length;i++){
				       var $opt = $($combo[0].options[i]);
				       var lang = val.split(':')[1];
				       if ($opt.val() == lang || $opt.html().toLowerCase().indexOf(lang)>=0){
					       $('#google_translate_element').show();
					       $combo.click();
					       $opt.focus();
					       return true
				       }
			       }
			    });
		    }
		    catch(e){
			    try{if(console)console.log(e);}catch(e){}
		    }
        },

        set_languages : function(selector){
            var $combo = $('select.goog-te-combo');
            if (utilities.google_translate.languages.length==0){
                for(var i=0; i<$combo[0].options.length;i++){
                   var $opt = $($combo[0].options[i]);
                    utilities.google_translate.languages.push($opt.html());
                }
            }
            if (selector) {
                var ar = [];
                var ugtl_ar = utilities.google_translate.languages;
                for(var i=1;i<ugtl_ar.length;i++){
                    ar.push(ugtl_ar[i]);
                }
                $(selector).html(ar.join(', '));
            }
        }
    }
    molhokwai.util.google_trans.cli_web_register();
}
catch(e){
    try{if(console)console.log(e);}catch(e){}    
}

