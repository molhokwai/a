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
	common : {
		header : {
			elements : [
				{'span' : {
					'attributes' : {
						'class' : 'jQs diblo w100% tac fstit',
						'innerHTML' : '(js based mockup, wireframes...)'
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
								'href' : 'javascript:flow.to({page:"LoginPage"});',
								'innerHTML' : '?'
							}
						}}
					]
				}}
			]
		}
	},

	index : {
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
							'class' : 'jQs tar w70% margl35%'
						},
						'children' : [
							{'input' : {
								'attributes' : {
									'type' : 'button',
									'value' : 'Submit: click to submit, or double tap the Ctrl key and type submit',
									'onclick' : molhokwai.flow.handlers.onSubmit,
									'class' : 'display-block jQs padv0.5% bcotransparent co#FFFCFA' 
								}
							}}
						]
					}}
				]
			}}
		]
	},

	wantNeedHaveResults : {
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
					}}
				]
			}}
		]
	}
};


