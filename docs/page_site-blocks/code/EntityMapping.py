from Entity import *

class EntityMapping(object):

    """
     

    :version:
    :author:
    """

    """ ATTRIBUTES
    entity  (public)
    optional_url  (public)
    content  (public)
    opt_mapping  (public)
    	Object (dictionary) required if Entity mapping does not match LayoutMapping

    """
    entity = None
    url = None
    content = None
    mapping = None

    def __init__(self, url=None, content=None, mapping=None):
        """
         

        @return  :
        @author
        """
        if url:
			self.url = url
		if content:
			self.content = content
		if mapping:
			self.mapping = mapping



