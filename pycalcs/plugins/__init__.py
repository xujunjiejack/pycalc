''' this script is called when this package is imported
	it will look through the package and enumerate all the classes
	found within. 


'''

import plugins.__import_extensions__
from defaultplugin import defaultplugin 

__import_extensions__.load_package('classes')

__plugins__ = {}

# check that all the plugins are correct
for pname,plugin in __import_extensions__.__imported__.items():
	if issubclass(plugin, defaultplugin) and pname != 'defaultplugin':
		print('adding %s to __plugins__'%pname)
		__plugins__[plugin.title] = plugin




