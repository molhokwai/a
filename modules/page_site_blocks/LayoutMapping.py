class LayoutMapping():

    """
     Attributes title & string:
         - String (xml/html...) with placeholders for entity mapping

    :version:
    :author:
    """

    """ ATTRIBUTES
    **attr, like:
        container (public)
        title  (public)
        summary (public)
        content  (public)
        ...

    """
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
