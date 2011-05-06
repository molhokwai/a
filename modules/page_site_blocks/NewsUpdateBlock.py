from BlockBase import *
from EntityMapping import *
from LayoutMapping import *

class NewsUpdateBlock (BlockBase):

	"""
   

	:version:
	:author:
	"""

	""" ATTRIBUTES

	entityMappings  (public)
		Required Implementation of the parent BaseBlock class's attribute.
   
 		EntityMapping.mapping object (dictionary) required if Entity attributes does not
		directy map to LayoutMapping placehoders
	layoutMapping  (public)
   		Required Implementation of the parent BaseBlock class's attribute.

	"""
	entityMappings = None
	layoutMappings = None



