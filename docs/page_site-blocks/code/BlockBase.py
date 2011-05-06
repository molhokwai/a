from types import *

class BlockBase():

	"""


	:version:
	:author:
	"""

	""" ATTRIBUTES


	coordinates  (public)
		Location coordinates:
		  ([0,0] -left top,   [0,1]  -left borrom,
	entityMappings  (public)
		EntityMapping.mapping object (dictionary) required if Entity attributes does not
		directy map to LayoutMapping placehoders
			[1,0] -right top, [1,1] -right bottom )
	layoutMapping  (public)
	"""
	coordinates = [0,0]
	entityMappings = None
	layoutMapping = None


 	def __init__(self, coordinates, entityMappings=None, layoutMappings=None):
		self.coordinates = coordinates
		if entityMappings:
			self.entityMappings = entityMappings
		if layoutMappings:
			self.layoutMappings = layoutMappings


	_layoutOutput = None
 	def layoutOutput(self)
		"""
		 Generic method:
		 	- Using reflection to match Entity relevant attributes to corresponding block
		 	  layoutMapping placeholders
		 	- Executing replacements (looping through entities) and returning output

		@return string :
		@author
		"""
		if not self._layoutOutput:
			self._layoutOutput = ''
			for entityMapping in entityMappings:
				for key in entityMapping.__dict__:
					e_attr = entityMapping.__dict__.get(key):
					l_attr = layoutMapping.__dict__.get(key):
					if l_attr:
						l_attr_v = ''	
						if type(e_attr) in [StringType, IntType]:
                            l_attr_v = l_attr % {key : str(e_attr)}

						elif type(e_attr) == ListType:
							for i in range(len(e_attr)):
                                l_attr_v += l_attr % {key : e_attr}

						elif type(e_attr) == DictType:
							for e_attr_k in e_attr:
                                l_attr_v += l_attr % {e_attr_k : e_attr[e_attr_k]}

						layoutMapping.__dict__.update({key:l_attr_v})
                        self._layoutOutput += layoutMapping.container % dict(content=layoutOutput.__dict__.get(key))
		return self._layoutOutput
			


