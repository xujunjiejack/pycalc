import plugins # specific to this module. used for plugins like inquisit scoring

# for db connections / logfiles / pretty printing and all that jam 
from utils import gui, db 

class pycalc:

	def __init__(self):
		self.plugins = {}
		window = gui.gui('Pycalcs')
		for name,plugin in plugins.__plugins__.items():
			self.plugins[name] = plugin()
			self.plugins[name].set_gui(window)
		window.mainloop()

		