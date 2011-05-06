from types import *

class BlockBase:

    """


    :version:
    :author:
    """

    """ ATTRIBUTES

    entityMappings  (public)
        EntityMapping.mapping object (dictionary) required if Entity attributes does not
        directy map to LayoutMapping placehoders
            [1,0] -right top, [1,1] -right bottom )
    layoutMapping  (public)
    """
    entityMappings = None
    layoutMapping = None


    def __init__(self, entityMappings=None, layoutMapping=None):
        if entityMappings:
            self.entityMappings = entityMappings
        if layoutMapping:
            self.layoutMapping = layoutMapping


    _layoutOutput = None
    def layoutOutput(self):
        """
         Generic method:
            - Using reflection to match Entity relevant attributes to corresponding block
              layoutMapping placeholders
            - Executing replacements (looping through entities) and returning output

        @return string :
        @author
        """
        def convert_attr(attr):
            if str(type(attr)).find('<class')>=0:
                return attr.xml()
            else:
                return attr
                
        if not self._layoutOutput:
            self._layoutOutput = []
            for i in range(len(self.entityMappings)):
                self._layoutOutput.append(self.layoutMapping.listOrder)
                
                entity = self.entityMappings[i].entity                
                for key in entity.__dict__:
                    e_attr = entity.__dict__.get(key)
                    l_attr = self.layoutMapping.__dict__.get(key)
                    
                    if l_attr:
                        l_attr_v = ''   
                        if type(e_attr) == ListType:
                            for i in range(len(e_attr)):
                                l_attr_v += convert_attr(l_attr) % {key : e_attr[i]}
                        else:
                            l_attr_v += convert_attr(l_attr) % e_attr

                        self.layoutMapping.__dict__.update({key:l_attr_v})
                        if key in self._layoutOutput[i]:
                            self._layoutOutput[i][self._layoutOutput[i].index(key)]= l_attr_v
                        
            self._layoutOutput = self.layoutMapping.container.xml() % dict(content='\n'.join(map(lambda y: '\n'.join(y), self._layoutOutput)))
        return self._layoutOutput
