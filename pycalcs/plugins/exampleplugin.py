from defaultplugin import defaultplugin

class exampleplugin(defaultplugin):
	title = 'EXAMPLE. INCLUDED JUST TO BE AN EXAMPLE FOR DEVELOPERS'
	
	def command(self, window):
		''' this doesn't really do anything'''

		print(('THIS DOESNT REALLY DO ANYTHING. ITS INCLUDED FOR DEVELOPERS '
			'TO SEE HOW TO MAKE PLUGINS'))
