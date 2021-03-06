#!/usr/bin/env python
import sys
import os
import re

# FILE ARGUMENTS AND CONTEXT / GLOBAL VARIABLES AND OBJECTS 
print """
	Required Arguments:
	------------------
		action: mask_store_keys | restore_keys

	Optional Arguments:
	------------------
		app_path: path to the application
		store_fname: the store file name
		fpath_keys_regexes_file : path to a json file containing the files keys regexes dict
"""
i=0
filepath = None
dirpath = None

action = None
app_path = '/home/herve/dev_molhokwai.net.a'
store_fname = None 
fpath_keys_regexes = {
	'%s/models/0_db.b.py'%app_path : ['(auth\.settings\.hmac\_key=)(\'.*\')', '(api\_key=)(\'.*\')']	
}
for arg in sys.argv:
	if i==0: 
		filepath = os.path.abspath(arg)
		dirpath = os.path.abspath(os.path.dirname(arg))
	if i==1: action = arg
	if i==2: app_path = arg
	if i==3: store_fname = arg
	if i==4:
		f = open(arg, 'r') 
		fpath_keys_regexes = eval(f.read())
		f.close()
	i+=1
if store_fname is None:
	store_fname = '%s/handle_secret_keys.store.json'%dirpath

# PROCESS METHODS
def get_mask(key):
	return "'%s'" % "".join(["x" for n in range(len(key))])

def mask_store_keys():
	fpath_keys_store = {}
	for fpath in fpath_keys_regexes:
		f_keys = ''
		fpath_keys_store[fpath] = {} 
		regexes = fpath_keys_regexes[fpath]
		f_keys_r = open(fpath, 'r')
		for line in f_keys_r:
			f_keys += line
			for i in range(len(regexes)):
				search = re.search(regexes[i], line)
				if search:
					fpath_keys_store[fpath][regexes[i]] = search.group(2)
		f_keys_r.close()

		f_masks_w = open(fpath, 'w')
		for k in fpath_keys_store[fpath]:
			key = fpath_keys_store[fpath][k] 
			f_keys = f_keys.replace(key, get_mask(key))
		f_masks_w.write(f_keys)
		f_masks_w.close()
		
		print 'done for: %s' % fpath

	f_store_w = open(store_fname, 'w')
	f_store_w.write(str(fpath_keys_store))
	f_store_w.close()
	
	print '------------------'
	print 'done: secret keys masked and stored.'

def restore_keys():
	f_store_w = open(store_fname, 'r')
	fpath_keys_store = eval(f_store_w.read())
	f_store_w.close()

	for fpath in fpath_keys_store:
		f_keys_r = open(fpath, 'r')
		f_keys = ''
		for line in f_keys_r:
			for regex in fpath_keys_store[fpath]:
				search = re.search(regex, line)
				if search:
					key = fpath_keys_store[fpath][regex]
					line = line.replace(get_mask(key), key) 
			f_keys += line
		f_keys_r.close()

		f_keys_w = open(fpath, 'w')
		f_keys_w.write(f_keys)
		f_keys_w.close()

		print 'done for: %s' % fpath

	print '------------------'
	print 'done: secret keys restored.'
		
	

# PROCESS
if action:
	exec('%s()'%action)
