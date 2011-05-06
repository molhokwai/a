from Template import *

class PageBase (Template):

    """
     

    :version:
    :author:
	"""

	""" ATTRIBUTES

    blocks  (protected)
        Implementation of the Parent's (Template) abstract attribute, 
		for a global site default Base Page
    entityBlocks  (protected)
        Implementation of the Parent's (Template) abstract attribute, 
		for a global site default Base Page
    """
    blocks = None
    entityBlocks = None


    def __init__(self, entityBlocks=None):
        """
         The construction method of the page passes the  page's implemented entityBlocks
         attribute to the Template base class construction , or the optional entityBlocks 
		Parameter.

        @return  :
        @author
        """
		if entityBlocks:
			self.entityBlocks = entityBlocks
		Template.__init__(self, self.entityBlocks)

