
class LayoutMapping():

    """
     Attributes title & string:
         - String (xml/html...) with placeholders for entity mapping

    :version:
    :author:
    """

    """ ATTRIBUTES

    container (public)
    title  (public)
    summary (public)
    content  (public)

    """

    container = None
    title = None
    summary = None
    content = None
    _list = {'container' : '', 'content' : ''}


    def __init__(self, **kwargs):
        if kwargs:
            self.__dict__.update(kwargs)
