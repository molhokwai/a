from EntityMapping import *
from LayoutMapping import *

class BlockBase(object):

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



 	def layoutOutput(self)
		"""
		 Generic method:
		 	- Using reflection to match Entity relevant attributes to corresponding block
		 layoutMapping placeholders
		 	- Executing replacements (looping through entities) and returning output
			Using optional entityMapping.mapping Object (dictionary, given if Entity mapping 
			does not match LayoutMapping)

		@return string :
		@author
		"""
		pass



