from defaultplugin import defaultplugin
from utils.gui import promptbox
from utils.db import (get_all_tablenames, db_connect, get_columns, 
	get_primary_keys, drop_table)
from utils.waisman_general_utils import parse_tablename
class docalc(defaultplugin):
	''' this plugin generalizes doing calcs'''

	title = 'Make a Calc table'

	def __init__(self):
		self.con = db_connect(DSN='wtp_data')

	def command(self, window):
		''' prompt user for dtaa table to make calc from
			then parses the tablename to figure out phase respondent and instr
			abbrv

			and makes a calc table based off that.

			then selects the columns with the same scale and computes sum 
			and mean for each scale.
		'''
		data_tables = [t for t in get_all_tablenames(self.con) if\
		 t.startswith('data_')]
		
		def check_enteredtable_is_data_table(txt):
			ret = txt in data_tables
			if not ret:
				print('%s not found in datatables'%txt)
			return ret
		
		datatable = promptbox(('enter the data table name you would '
			'like to calc'), validation=check_enteredtable_is_data_table, 
			title='', error_text='{text} not found in datatables')
		print('enetered %s'%datatable)

		# we now have datatable
		if datatable is None: return # we're done here

		parsed = parse_tablename(datatable)
		if (		('type' not in parsed) 
					or ('instrument abreviation' not in parsed)
					or ('phase' not in parsed)
					or ('respondent' not in parsed)
					or (parsed['type'] != 'data') ):
			print('problem with the table. could not parse it successfully')
			print ('only to %s'%parsed)
			return # we're done here

		resp = parsed['respondent']
		phase = parsed['phase']
		instr = parsed['instrument abreviation']

		calc_table_name = 'calc_%s_%s_%s'%(phase, instr, resp)

		data_cols = get_columns(self.con, datatable)
		pks = get_primary_keys(self.con, datatable)

		calc_cols = []


