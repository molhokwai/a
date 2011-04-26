###################################
## REQUEST HANDLING
###################################
try:
    exec('from applications.%s.modules import request_handler as request_handler_module' % this_app)
    requestHandler = request_handler_module.handle_request(request, response, session, cache, T, db, auth, app_objects)
    """
        Eventual Redirection:
        if not instruction_results or not len(instruction_results)>0:
            redirect(URL(r=request, c='default', f=request.function, args=request.args, vars=request.vars))
    """
except Exception, ex:
    log_wrapped('Error (%s/controllers/request_handling.py:9)' % this_app, ex)


###################################
## CONTROLLER FUNCTIONS
###################################

# The main function
def handle():
    if requestHandler.instructions and len(requestHandler.instructions)>0:
        return response.json({
            'status' : 1,
            'message' : 'done',
            'result' : requestHandler.instructions
        })
    else:
		args = request.args
		c = args[0]
		f = None
		if len(args)>2:
			redirect(URL(r=request, c=args[0], f=args[1], 
				args=[args[i] for i in range(2,len(args))], vars=request.vars))
		else:
			redirect(URL(r=request, c=args[0], 
				args=[args[i] for i in range(1,len(args))], vars=request.vars))

        return response.json({
            'status' : 0,
            'message' : 'not done',
            'result' : None
        })
