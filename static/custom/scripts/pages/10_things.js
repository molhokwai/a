var steps = {
	current : 0,
	def : {
		0: { 'set':false },
		2: { 'set':false },
		last : function(){
			var i = 0;
			for(k in steps.def){
				if(!isNaN(parseInt(k)) && parseInt(k)>i) { i=parseInt(k); }
			}
			return i;
		}
	},
	setLinks : function(params){
		if (!steps.def[params.step]){
			steps.def[params.step] = {};
		}
		if (!steps.def[params.step]['set']){
			$('#step_'+params.step+' ul.flat li a').each(function(i){
				$(this)[0].href = 'javascript:steps.step.show('
						+'{ step:'+(params.step+1)+', title:"'+$(this).html()+'" });';
			});
			steps.def[params.step]['set'] = true;
		}
	},
	step : {
		show : function(params){
			$('#step_'+params.step).show();
			$('#step_'+(steps.current)).hide();
			if (params.step>0){
				$('#step_'+params.step+' h3').html(params.title);
			}

			if (params.step<steps.def.last()){
				steps.setLinks({ step:params.step });
			}

			if (params.step>0){
				$('._nav').show();
			}
			else {
				$('._nav').hide();
			}

			steps.current = params.step;
		},
		city_country : {
			handleValueSubmit: function(){
				var title = $('#city_country').val();
				if (title && title.indexOf('city, country')<=0 && title != ''){
					steps.step.show({ step:steps.current+1,title:title });
				}
			},
			handleInputFocus : function(){
				if ($('#city_country').val().indexOf('city, country')>=0){
					$('#city_country').val('');
					$('#city_country').css({ fontStyle: 'normal' });
				}
			}
		}
	}
};

$(document).ready(function(){
	steps.setLinks({ step:0 });
});
