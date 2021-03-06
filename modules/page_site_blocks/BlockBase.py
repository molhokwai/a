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
                attr = attr.xml()                
            return attr
                
        if not self._layoutOutput:
            self._layoutOutput = []

            try:
                for i in range(len(self.entityMappings)):
                    entity = self.entityMappings[i].entity
                    self._layoutOutput.append([self.layoutMapping.listOrder[j] for j in range(len(self.layoutMapping.listOrder))])
                    self._layoutOutput[i] = filter(lambda x:x in entity.__dict__, self._layoutOutput[i])
                    
                    for key in entity.__dict__:
                        if key in self._layoutOutput[i]:
                            e_attr = entity.__dict__.get(key)
                            l_attr = self.layoutMapping.__dict__.get(key)
                            
                            if l_attr and e_attr:
                                l_attr_v = ''   
                                if type(e_attr) == ListType:
                                    for j in range(len(e_attr)):
                                        _e = e_attr[j]
                                        _d = {key : _e}
                                        if type(_e) == DictType: _d = _e
                                        l_attr_v += convert_attr(l_attr) % _d
                                else:
                                    l_attr_v += convert_attr(l_attr) % e_attr
        
                                self._layoutOutput[i][self._layoutOutput[i].index(key)]= l_attr_v    
            except Exception, ex:
                print 'Error occured in modules/page_site_blocks/BlockBase:layoutOutput() %s' % str(ex)
                        
            self._layoutOutput = convert_attr(self.layoutMapping.container) % dict(content='\n'.join(map(lambda y: '\n'.join(y), self._layoutOutput)))
        return self._layoutOutput
