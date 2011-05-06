
class EntityMapping():

    """
     

    :version:
    :author:
    """

    """ ATTRIBUTES
    entity  (public)
    content  (public)
    optional_url  (public)
    optional_imageUrl  (public)
    opt_mapping  (public)
    	Object (dictionary) required if Entity mapping does not match LayoutMapping
		key : the LayoutMapping attribute, value: the entity corresponding attribute

    """
    entity = None
    content = None
    url = None
    imageUrl = None
    mapping = None

	def setContent(self, value):
		self.content = value
	def setUrl(self, value):
		self.url = value
	def setImageUrl(self, value):
		self.imageUrl = value

    def __init__(self, entity, mapping=None):
        """
		If mapping object provided, attributes are appended to object accordingly         

        @return  :
        @author
        """
		self.entity = entity
		if mapping:
			self.mapping = mapping
		for attr in mapping:
			value = self.entity.__dict__.get(mapping[attr])
			self.__dict__.update({attr:value})


