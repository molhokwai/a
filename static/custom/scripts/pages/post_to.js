var responseData = null;
var defaultTranslLanguages = ['fr'];
var translateParams = null;
var previousLanguage = null;
var currentLanguage = null;
var params = null;
var detectLanguageCallback = function(response) {
	currentLanguage = response.data.detections[0][0].language;

	/* supported languages call */
	params['urlActionAppend'] = '/languages';
	params['sourceLanguage'] = currentLanguage;
	params['callback'] = 'supportedLanguagesCallback';
	params['script'] = 'supportedLanguages';
	execSingletonScript();
}
var supportedLanguagesCallback = function(response){
/* set Languages: assumption to be verified @stack-inspection time */
var supportedLanguages = response.data.translations.supported;
	for(i in supportedLanguages){
		if (previousLanguage!=currentLanguage 
			|| !$('.vcs-post fieldset div.languages div.'+translateParams.targetLanguage+' input').length>0){
			var div = document.createElement('div');
			var label = document.createElement('label');
			var input = document.createElement('input');
			label.html(supportedLanguages[i]);
			input.type = 'checkbox';
			input.value = supportedLanguages[i];
			$(input).bind('click', function(){
				if (targetLanguages.length<maxTargetLanguages){
					setTargetLanguages();
				}
				else {
					$(this)[0].checked = false;
				}
			});
			$(div).appendClass(supportedLanguages[i]);

			$(div).append(input);
			$(div).append(label);
			$(div).append(' | ');
			$('.vcs-post fieldset div.languages').append(div);
		}
	}
	previousLanguage = currentLanguage;

	/* translation call */
	params['urlActionAppend'] = '';
	params['sourceLanguage'] = currentLanguage;
	params['callback'] = 'translateCallback';
	params['script'] = 'translate';
	execSingletonScript();
};
var translateCallback = function(response){
	/* language fields singleton set  */
	if(!$('.vcs-post fieldset .translations div.'+translateParams.targetLanguage+' textarea').length>0){
		var div = document.createElement('div');
		var label = document.createElement('label');
		var textarea = document.createElement('textarea');
		label.html(translateParams.targetLanguage);
		textarea.rows = 3;
		$(div).appendClass(translateParams.targetLanguage);

		$(div).append(label);
		$(div).append(textarea);
		$('.vcs-post fieldset .translations').append(div);
	}

	/* language textarea value set  */
	$('.vcs-post fieldset .translations div.'+translateParams.targetLanguage+' textarea').html(
		responseData.translations[0].translatedText
	);
};

var script = {
	'detectLanguage' : null,
	'supportedLanguages': null,
	'translate': null
};
/* original from: http://code.google.com/apis/language/translate/v2/getting_started.html */
var execSingletonScript = function(){
	if (!script[params.script]){
		script[params.script] = document.createElement('script');
		script[params.script].type = 'text/javascript';
		script[params.script].id = 'google_translate_detect';
		document.getElementsByTagName('head')[0].appendChild(script[params.script]);    
	}
	$('#'+script[params.script].id)[0].src = 'https://www.googleapis.com/language/translate/v2'
				+ (params && params.urlActionAppend ? params.urlActionAppend : '')
				+ '?key=' + params.key
				+ '&callback=' + params.callback 
				+ '&q=' + params.sourceText
				+ (params && params.sourceLanguage ? '&source=' + params.sourceLanguage : '')
				+ '&target=' + params.targetLanguage;
};


var targetLanguages = null;
var setTargetLanguages = function(){
	targetLanguages = []; 
	$.each('.vcs-post fieldset div.languages div input', function(){
		if ($(this)[0].checked){
			targetLanguages.push($(this)[0].val());
		}
	});
};

var maxTargetLanguages = 2;
var doTranslate = function(e){
	setTargetLanguages();
	if (!targetLanguages.length){
		targetLanguages = defaultTranslLanguages; 
	}

	for(i in targetLanguages){
		params = { 
			key : 'AIzaSyDGeSz7vrDX2AmOqGLaKsCal17eX_vmW_E',
			targetLanguage: targetLanguages[i],
			sourceText: $('.vcs-post fieldset div.message textarea').val(),
			urlActionAppend: '/detect',
			callback: 'detectLanguageCallback',
			script: 'detect'
		};
		execSingletonScript();
	}
};

$(document).ready(function(){
	$('.vcs-post fieldset div.message textarea').bind('change', doTranslate)
	$('.vcs-post fieldset div a.submit').bind('click', doTranslate)
});

