from BlockBase import *
from EntityBlock import *
from Entity import *
from Menu import *
from Footer import *
from Container import *

class Template(object):

    """
     

    :version:
    :author:
    """

    """ ATTRIBUTES

    blocks  (public)
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
    blocks = None
    entityBlocks = None 

    def output(self):
        """
         Method using blocksOutput method, and doing footer, header, container... output

        @return  :
        @author
        """
        pass

    def __init__(self, entityBlocks):
        """
        @param EntityBlock entityBlocks : 
        @return  :
        @author
        """
        pass

    def _blocksOutput(self, entityBlocks=None):
        """
         

        @param EntityBlock opt_entityBlocks : Uses the class's entityBlocks attribute unless optional entityBlocks parameter given
        @return BlockBase :
        @author
        """
        pass

    def _populateEntityBlocks(self, entityBlocks=None):
        """
         Method used in getBlocks to get corresponding entities

        @param EntityBlock opt_entityBlocks : Uses the class's entityBlocks attribute unless optional entityBlocks parameter given
        @return Entity :
        @author
        """
        pass



