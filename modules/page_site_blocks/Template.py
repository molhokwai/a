from Entity import *
from EntityMapping import *

class Template(object):

    """
     

    :version:
    :author:
    """

    """ ATTRIBUTES

    menu  (public) (documentation only)
    footer  (public) (documentation only)
    container  (public) (documentation only)
    entityBlocks  (private)
        Abstract attribute to be implemented in child Page

    Mapping by type:
        - Entity type (Post, NewsUpdate, Service...)
        - Block by coordinates :
            ([0,0] -left top,   [0,1]  -left borrom,
              [1,0] -right top, [1,1] -right bottom )
    """
    entityBlocks = None 

    _blocks = None
    @property
    def blocks(self):
        """
        Property, returning the blocks from the entityBlocks Attribute, keeping the x,y list coordinates.

        @return  :
        @author
        """
        if not self._blocks:
            self._blocks = []
            for x in range(len(self.entityBlocks)):
                self._blocks.append([])
                for y in range(len(self.entityBlocks[x])):
                    self._blocks[x].append(self.entityBlocks[x][y].block)
        return self._blocks
                

    def __init__(self, entityBlocks):
        """
        @param EntityBlock entityBlocks : 
        @return  :
        @author
        """
        self.entityBlocks = entityBlocks

                    
    def populateEntityBlocks(self, entityBlocks=None):
        """
        Method used to get and assign the entities for each entityBlock. 

        @param EntityBlock opt_entityBlocks : Uses the class's entityBlocks attribute unless optional entityBlocks parameter given
        @return Entity :
        @author
        """
        if not entityBlocks:
            entityBlocks = self.entityBlocks
        for x in range(len(entityBlocks)):
            for y in range(len(entityBlocks[x])):
                entityBlock = entityBlocks[x][y]
                entityBlock.entities = Entity.fetch(entityBlock.query)                
                for i in range(len(entityBlock.entities)):
                    if not entityBlock.block.entityMappings:
                        entityBlock.block.entityMappings = []
                    print '-------------| len(entityBlock.block.entityMappings) : %i ' % len(entityBlock.block.entityMappings)
                    entityMapping = EntityMapping(entityBlock.entities[i])
                    if i<len(entityBlock.block.entityMappings):
                        entityBlock.block.entityMappings[i] = entityMapping
                    else:
                        entityBlock.block.entityMappings.append(entityMapping)
