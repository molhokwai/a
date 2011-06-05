/* THE SYSTEM, A PERFECT ONE: 
       FUNCTIONAL/TECHNICAL DETAILS
   --------------------------------  

*/

/*  sequence
	@type dictionary
	@attributes: 
		The sequences of the flow 
*/
molhokwai["flow"]['sequences'] = {
	"index" : {
		"wantNeedHave" : {
			"wantNeedHaveResults" : 'page'
		}
	}
};

/*  page
	@type dictionary
	@attributes:
		Each page of the flow 
*/
molhokwai["flow"]['page'] = {
};

molhokwai.flow.page['common'] = {
};

molhokwai.flow.page.common['header '] = {
	elements : [
		{'span' : {
			'attributes' : {
				'class' : 'jQs diblo w100% tac fstit fs0.9em',
				'innerHTML' : '(js based inception application: user interface processes...)'
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
						'href' : 'javascript:molhokwai.flow.flow.to({page:"fallback"});',
						'innerHTML' : '?'
					}
				}}
			]
		}}
	]
};

molhokwai.flow.page.common['footer'] = {
	elements : [
		{'p' : {
			'attributes' : {
				'class' : 'jQs tace margb-1.5% margr-3.5% tace',
			},
			'children' : [
				{'a' : {
					'attributes' : {
						'class' : 'display-block border-grey jQs padv0.5% padl4% bcotransparent w30% co#FFFCFA fs1em mr38% tdno',
						'href' : 'javascript:molhokwai.flow.flow.to({page:"index"});',
						'innerHTML' : 'Start a new request/command'
					}
				}}
			]
		}}
	]
};


molhokwai.flow.page['index'] = {
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
						'class' : 'jQs w100%' 
					},
					'children' : [
						{'a' : {
							'attributes' : {
								'onclick' : molhokwai.flow.handlers.onSubmit,
								'innerHTML' : 'Submit: click to submit, or double tap the Ctrl key and type submit',
								'class' : 'display-block border-grey jQs padv1% padl4% bcotransparent w70% margl30.5% co#FFFCFA tdno'
							}
						}}
					]
				}}
			]
		}}
	]
};

molhokwai.flow.page['wantNeedHaveResults'] = {
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
								'class' : 'no-bullets jQs padv0.5% co#AAA5A5'
								//,'style' : 'list-style-type:none;'
							}
						}},
						{'li' : {
							'attributes' : {
								'innerHTML' : 'Location: (lat, long)',
								'class' : 'no-bullets jQs padv0.5% co#AAA5A5'
								//,'style' : 'list-style-type:none;'
							}
						}},
						{'li' : {
							'attributes' : {
								'innerHTML' : 'Description: We make Macadamia Nu Brittle Vegan Ice based on the recipe kindly provided to us by the creators...'
											+'It tastes different (of course), but if you love the original, you&#39; love this one... we love it...'
											+'<br/>You can find our recipe here (---), or come enjoy it with... ',
								'class' : 'no-bullets jQs padv0.5% co#AAA5A5'
								//,'style' : 'list-style-type:none;'
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
								'class' : 'no-bullets jQs padv0.5% co#AAA5A5'
								//,'style' : 'list-style-type:none;'
							}
						}}
					]
				}},
				{'p' : {
					'attributes' : {
						'class' : 'jQs tace margb-1.5% margr-3.5% tar',
					},
					'children' : [
						{'a' : {
							'attributes' : {
								'class' : 'display-block border-grey jQs padv0.5% padr4% bcotransparent w30% co#FFFCFA fs1em tdno',
								'href' : 'javascript:molhokwai.flow.flow.to({page:"fallback"});',
								'innerHTML' : 'Into this request/command'
							}
						}}
					]
				}}
			]
		}}
	]
};

	
molhokwai.flow.page['intoCommandRequest'] = { 
	elements : [
		{'form' : {
			'attributes' : {
				'id' : "intoCommandRequest",
				'name' : "intoCommandRequest",
				'class' : 'jQs clbo'
			},
			'children' : [
				{'p' : {
					'attributes' : {
						'innerHTML' : 'Your request/command on this request/command:'
					}
				}},
				{'textarea' : {
					'attributes' : {
						'class' : 'out-grey jQs bcotransparent co#AAA5A5',
						'innerHTML' : ''
					}
				}},
				{'p' : {
					'attributes' : {
						'class' : 'jQs tar w70% margl35%'
					},
					'children' : [
						{'a' : {
							'attributes' : {
								'type' : 'button',
								'innerHTML' : 'Submit',
								'href' : 'javascript:molhokwai.flow.to({page:"fallback"})',
								'class' : 'display-block link jQs padv0.5% bcotransparent co#FFFCFA'
							}
						}},
					]
				}}
			]
		}}
	]
};

molhokwai.flow.page['fallback'] = { 
	elements : [
		{'div' : {
			'attributes' : {
				'id' : "fallback",
				'name' : "fallback",
				'class' : 'jQs clbo'
			},
			'children' : [
				{'p' : {
					'attributes' : {
						'innerHTML' : 'This page is not implemented.'
					}
				}},
				{'p' : {
					'attributes' : {
						'innerHTML' : 'This is an inception application, with no server-side processes going on, that is dynamic Html pages generation'
										+' and dynamic user interface processes (flow) generation...'
					}
				}}
			]
		}}
	]
};


