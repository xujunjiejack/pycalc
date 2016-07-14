'''
this is a general script that can be included in any package 
to implement a simple plugins scheme.

INSTRUCTIONS:
1. include this file in the package
2. within the __init__.py file import this module
3. run __import_extensions__.load_package()
4. that will return a list of modules within the package as long as they 
	don't start with an '_'


set ignore_errors to T/F
that will either raise an error (if F) or just print a message


load_package takes either 'classes', 'modules', or 'functions'
in order to figure out what to return
'''
from importlib import import_module
from glob import glob
from keyword import iskeyword
from os.path import dirname, join, split, splitext
from inspect import isclass, isfunction

ignore_errors = False # should it just print a message if module error
# ignore_errors = False # should raise an error if module error

class Err(Exception): pass # file specific exception for use here only

__imported__ = {}

def load_classes(module):
	''' this adds the classes in a module to __imported__'''
	moddic = module.__dict__
	# get the classes within the file
	classes = {k:v for k,v in moddic.items() if isclass(v)}  
	for cname, _class in classes.items():
		__imported__[cname] = _class

def load_functions(module):
	''' this adds the functions in a module to __imported__'''
	moddic = module.__dict__
	# get the classes within the file
	funcs = {k:v for k,v in moddic.items() if isfunction(v)}  
	for fname, _func in funcs.items():
		__imported__[fname] = _func


def load_module(module_str):
	''' this loads a module object an returns it. for further 
		checking
		if errors occur. will return a mmErr with problem
		to raise or not
	'''
	try:
		# attempt to import the module
		# e.g. import data_handlers.pyfile
		module =import_module(module_str)
		return module
	except Exception as e: # error. ignoring. 
		err = Err(('exception {%s} while loading '
				'the %r plug-in.')%(e,module_str))
		return err


def load_package(_type):
	assert _type in ['modules', 'classes', 'functions'], ('load_package takes '
		'only functions, modules or classes as its argument'
		'to decide what type of things to import')

	basedir = dirname(__file__) # get this package name
	cur_dir = split(basedir)[-1]
	pyfiles = glob(join(basedir, '*.py')) # search for python files
	
	# print('basedir', basedir)
	# print('cur_dir', cur_dir)



	for filepath in pyfiles: # look at each file in turn
		filename = split(filepath)[-1] # get the file name not it's path
		modulename = splitext(filename)[0] # remove .py extension to import it
		
		if  (   not modulename.startswith('_') # e.g. __init__.py
				and modulename.isidentifier()  # T iff str module is a var at present
				and not iskeyword(modulename)  # if its a special keyword
			):

			# FYI __name__ = this directory name
			# module = load_module(__name__ + '.' + modulename)
			module = load_module(cur_dir + '.' + modulename)
			if isinstance(module, Err): 
				if ignore_errors: 
					print(module.args[0]) # print err message
					continue # go to next module
				else: raise module # raise exception
			
			# else module loaded successfully
			if _type == 'modules':
				__imported__[modulename] = module
			elif _type == 'classes':
				load_classes(module)
			else: # functions
				load_functions(module)
