#!/usr/bin/env python 
# coding: utf8 
from types import *
from gluon.html import *
from gluon.http import *
from gluon.validators import *
from gluon.sqlhtml import *
# request, response, session, cache, T, db(s) 
# must be passed and cannot be imported!

#########################################################################
## CLASS :
##    Functions
##
#########################################################################

class Function:
    _name = ''
    _ref = None
    _input = None
    _output = None
    
    def __init__(self, _name, _ref, _input=None, _output=None):
        self._name = _name
        self._ref = _ref
        self._input = _input
        self._output = _output

class Request:
    _request = None
    _input = None
    
    def __init__(self, _request, _input=None):
        self._request = _request
        self._input = _input

        
class Functions:
    """
        TODO:
            Building google app engine native db structure,
            and making adding functions dynamic, in two steps:
            -    Adding function in this file
            -    Adding function in db
            => [_functions] property to dynamic db retrieve, parse & return property            
    """
    def functions(self):
        return [
            {0 : Function(
                'example',
                eval('Functions().example'),
                [{StringType:{'a':''}}, {FloatType:{'b':0.1}}, {IntType:{'c':-1}}, {DictType:{'d':{}}}, 
                            {ListType:{'e':[]}}, {MethodType:{m:eval('Functions().x')}}],
                [DictType, ListType, StringType, FloatType, IntType]
            )},
            {1 : Function(
                'generate_sequence',
                eval('Functions().generate_sequence'),
                [{ListType:'functions'}],
                [BooleanType,ListType]
            )},
            {2 : Function(
                'sequence_is_valid',
                eval('Functions().sequence_is_valid'),
                [{Sequence:'sequence'}],
                [BooleanType,Sequence]
            )}
        ]
        
    def example(a, b, c=-1, d={}, e=[], m=eval('Functions().x')):
        return ({a:b}, [m(c,d,e)], '', 1.0, 1)

    def generate_sequence(self, functions=None):
        """
        Generates a sequence of random sequence of functions call, 
        with IO passing between them
             
        :version:
        :author:
        """
        if functions is None:
            functions = self.functions()

        # Generate a random number between 1 and len(functions)
        nr_of_functions = 10

        # Generate a random list of [nr_of_functions] functions
        nr_list = []
        while len(nr_list) <= nr_of_functions:            
            # Generate a random number between 1 and len(functions)
            nr = -1
            if not nr in nr_list:
                nr_list.append(nr)
            
        sequence = Sequence([functions[i] for i in nr_list])
        return self.sequence_is_valid(sequence),sequence

    def execute_function(self, function):
        """Executes the function"""
        pass
        
    def sequence_is_valid(self, sequence):
        """
            Checks if there is a possible valid sequence of parameters flow/passing.
            Returns the valid Sequence (by setting the flow attribute) if any
        """
        pass

    def execute_sequence(self, sequence, _input=None):
        """
            Executes the sequence, using the flow attribute
            Keeps the last output through the sequence, to return it at the end
        """
        pass

    def persist_sequence(self, sequence):
        """
            Persists the sequence in datastore
        """
        pass

    def find_sequence(self, _input, request=None):
        """
            Finds potential sequence Match from given input and request specifics
            if given
        """
        pass

    def parse_request(self, request):
        """
            Parses the request, and returns the inferred input
        """
        pass

    def respond_request(self, request):
        """
            Responds to the given request
            Ideally:
                This a sequence that the system can find by itself, and 
                it does so.
        """
        _input = request.request
        if (type(_input) != ListType):
            _input = self.parse_request(request)

        return self.execute_sequence(self.find_sequence(_input, request), _input)

    def request_feedback(self, request, sequence, output):
        """
            Responds to the given request
            Ideally:
                This a sequence that the system can find by itself, and 
                it does so.
        """
        _input = request
        if (type(request) != ListType):
            _input = self.parse_request(request)

        return self.execute_sequence(self.find_sequence(_input, request), _input)

    def find_functions(self):
        """
            Wide purpose function to look for new functions
            'everywhere' possible and add them
        """
        pass

    def loop(self, o, key_func=None, value_func=None):
        """For List or Dict"""
        pass

    def x(self, c, d, e):
        pass

    def find_and_replace(subj, obj):
        for k in obj:
            while(subj.find(k)>=0):
                subj = subj.replace(k, obj[k])
        return subj

    def convert_to_timezone():
        """From: http://www.computerhope.com/jargon/t/time.htm
            Getting html page body
            Parsing corr. table to key, values
            Converting & returning
            
            => Extracting (programming) Pattern to be used
                in similar processes
        """
        pass
        
class Sequence:
    """Attributes
        _list:
            The list of sequences' functions
        _flow:
            The flow of parameters IO through the sequence
            Example: [{1:3},{3:9},{9:29}]
    """
    _list = []
    _flow = []
    
    def __init__(self, _list, _flow):
        self._list = _list
        self._flow = _flow

    def flow(self, _flow=None):
        if not _flow is None:
            self._flow = _flow
        return self._flow
