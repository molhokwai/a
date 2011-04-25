#!/usr/bin/env python 
# coding: utf8 
from gluon.html import *
from gluon.http import *
from gluon.validators import *
from gluon.sqlhtml import *
# request, response, session, cache, T, db(s) 
# must be passed and cannot be imported!

class RequestHandler:
    request = None
    response = None
    session = None
    cache = None
    T = None
    db = None
    auth = None
    app_objects = None
    modules_config = None
        
    def __init__(self, request, response, session, cache, T, db, auth, app_objects):
        self.request = request
        self.response = response
        self.session = session
        self.cache = cache
        self.T = T
        self.db = db
        self.auth = auth
        self.app_objects = app_objects
        try:
            if app_objects.config.APP_MODULES_DETAILS:
                a_o_a_m_d = app_objects.config.APP_MODULES_DETAILS
                if len(a_o_a_m_d)>0:
                    self.modules_config = a_o_a_m_d
        except Exception, ex:
            app_objects.log_wrapped('Request Handler Handling Error (%s/modules/request_handler/Requesthandler/__init__/line:36+/-)' % request.application, ex)
        if not self.modules_config:
            self.modules_config = app_objects.app_modules_config

    _instructions = None
    @property
    def instructions(self):
        if not self._instructions:
            self._instructions = self.parse()
        return self._instructions
    
    def parse(self, _request = None):
        """     Parsing of request from left to right
                Instruction keyword not preceding object keyword:
                - default: read
                Instruction action keyword in Instruction not preceding object keyword:
                - default: add
        """
        s_a_o_u = self.app_objects.utilities
        if _request is None: _request = self.request
        
        """
            Mathematical Simplification:
                Type 'data' required so:
                    Make array though split by type 'data':
                    And parse each instruction into instructions array                    
        """
        module_config = self.modules_config['request_handling']
        _sections = _request.args
        instructions_type_name = []
        for i in range(len(_sections)):
            _previous = instructions_type_name[i-1] if i>0 else None
            _current = s_a_o_u.instruction_type_subject(_sections[i],module_config)
            if _current[0] == 'object':
                if _previous is None or s_a_o_u.is_object(_previous,module_config):
                    _act = 'add'
                    if len(s_a_o_u.instructions_filter(instructions_type_name, module_config))>0: _act = 'add'
                    instructions_type_name.append((_act,_current[1],_sections[i+1]))
                elif s_a_o_u.is_action(_previous,module_config):
                    instructions_type_name.append((_previous[2],_current[1],_sections[i+1]))
                i+=1
            else:
                # _current[0] == 'action'
                instructions_type_name.append((_current[0],_current[1],_sections[i]))
    
        # remove mute instructions (actions)
        self._instructions = s_a_o_u.instructions_filter(instructions_type_name, module_config)
        return self._instructions

    def execute(self, _instructions = None):
        """ CRUD execution of instructions actions on instructions objects, in sequence given, incrementing output list, 
                feeding current (last) output to next instruction.
        
             Instructions actions on instructions objects: 
             -    Taking last output object
             -    Finding the list property on the object to add to by name of current object
             -    Appending to the list property
             -    Saving
        """
        if _instructions is None: _instructions = self._instructions
        request_handled = True
        return _instructions

def handle_request(request, response, session, cache, T, db, auth, app_objects):
    app_details = app_objects.details
    app_config = app_objects.config
    log_wrapped = app_objects.log_wrapped
    utilities = app_objects.utilities

    try:
        # request handler proxy
        requestHandler = app_objects.RequestHandler(
                            request, response, session, cache, T, db, auth, app_objects)
        if len(requestHandler.instructions):
            requestHandler.execute()
            return requestHandler
    except Exception, ex:
        log_wrapped('Request Handler Handling: Error (%s/modules/request_handler/handle_request/line:106+/-)' % request.application, ex)
