from utils import gui

class defaultplugin(object):
	''' this is the default plugin to form a prototype for all the 
		plugins added to this project.

		in order to add a plugin it must be a subclass of this thing
	'''

	title = 'defaultplugin'

	def __init__(self):pass

	def command(self, *args, **kwargs):
		''' the main entry point for this plugin. do anything you want here'''
		print('the default plugin does nothing')
	
	def set_gui(self, window):
		''' sets the gui for this plugin. make it whatever you like here!'''
		window.add_button(self.title, lambda p=self:p.command(window))