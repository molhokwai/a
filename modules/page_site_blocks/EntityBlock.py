class EntityBlock(object):

    """
     Dynamic Entity assignment to Block

    :version:
    :author:
    """

    """ ATTRIBUTES

    entities  (public)
    block  (public)
    query  (public)
        (Sql string | Else)

    """
    entities = None
    block = None
    query = None

    def __init__(self, **kwargs):
        if kwargs:
            self.__dict__.update(kwargs)
