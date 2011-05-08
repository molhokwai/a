from types import *

class Entity():

    """
     

    :version:
    :author:
    """

    """ ATTRIBUTES

    _**attr  (public)

    """
    @staticmethod
    def fetch(query):
        """
        - Executes the query object
        - Returns a List of Entity objects with attributes populated from fetched entities         

        @param type _type : 
        @param object _key : 
        @return Entity :
        @author
        """
        from gluon.contrib import simplejson
        e_dicts = map(lambda x: simplejson.loads(x.data), query.select())
        entities = []
        for i in range(len(e_dicts)):
            e = Entity()
            e.__dict__.update(e_dicts[i]['meta'])
            e.__dict__.update(e_dicts[i]['entity'])
            entities.append(e)
        return entities
