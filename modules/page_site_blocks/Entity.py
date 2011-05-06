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
        e_dicts = map(lambda x: simplejson.loads(x.post_attributes_json)["entity"], query.select())
        entities = []
        for i in range(len(e_dicts)):
            e = Entity()
            e.__dict__.update(e_dicts[i])
            entities.append(e)
        return entities
