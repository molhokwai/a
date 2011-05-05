from Entity import *
from BlockBase import *

class EntityBlock(object):

    """
     Dynamic Entity assignment to Block

    :version:
    :author:
    """

    """ ATTRIBUTES

    entities  (public)
    block  (public)
		Reference to corresponding Block attribute (block<T>.layoutMapping.title,
		block<T>.layoutMapping.content...)
    blockLayoutMapping  (public)
		(Sql string | Else)
    query  (public)

    """
	entities = None
	block = None
	blockLayoutMapping = None
	query = None


