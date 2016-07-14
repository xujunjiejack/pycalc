import sys
import json
import logging
from os import path
from parsingRules import parsing_maps,filters, filtering_functions


def setup_logger(loggername, logfile=None, logfile_mode='w', level=logging.INFO, stdout= True, format='%(name)s/%(level)s:%(message)s'):
    ''' This sets up a logger object and returns it. 
        '''
    l = logging.getLogger(loggername)
    formatter = logging.Formatter(format)
    if logfile:
        filehandler = logging.FileHandler(logfile, mode=logfile_mode)
        filehandler.setFormatter(formatter)
        l.addHandler(filehandler)
    if stdout:
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)
        l.addHandler(streamHandler)
    l.setLevel(level)
    return l

def prettify_str(list_like, indent=2, sort_keys=True):
    """
    Returns a well formatted string with \\n and \\t so that it looks good. 
    Takes a list-like, serializable object
    you can also specify the indent, it defaults to 2

    Throws a TypeError if object is not serializable
    """
    try:
        return json.dumps(list_like, indent=indent, sort_keys = True)
    except:
        print('Cannot Serialize this object in wtp_utils.py prettify_str')
        raise TypeError

def logfile(path,message = None, keep_alive = False, mode='w'):
    """ Writes a string to a file, optionally specify mode. 
            'r' reading
            'w' writing
            'a' append to the end
            'b' binary mode
            ... etc. look at doc for open for more options. 
        """
    f = open(path, mode)
    written = 0
    if(message):
        written = f.write(message)
    if(keep_alive):
        return f
    else:
        f.close()
        return written

def sprint(*messages, files=[sys.stdout], **kwargs):
    '''
        Helper method to print to multiple files
        files replaces the 'file' keyarg in print, 
        but for the remainder of keyword args check out the 
        docs for print.  
    '''
    for f in set(files):
        print(*messages, file=f, **kwargs )
        f.flush()

def iterable_is_all_equal(iterable):
    '''
        returns true if all elements in iterable are equal
        e.g. 
        [1,2,2,3] -> false
        [1,1,1,1] -> true

        testing equality using the defintion of set
        i.e. all indexes must be unique. so we reduce the iterable 
        to a set and it should have length of 1, else they are not all the same.
    '''
    return len(set(iterable)) is 1

def splitall(fpath):
    '''takes a string representation of a path
        and splits is up into an os.joinable array'''
    split_path = []
    while fpath != '':
        s = path.split(fpath)
        split_path.append(s[1])
        fpath = s[0]
    return split_path.reverse()

def parse_tablename(tablename,log = logging ):
    """ This function breaks up the tablename based on the WTP conventions
            (i.e. sections are seperated by `_`) and the rules provided by
            the file are path_to_defs during __init__. 

            After breaking up the tablename into as many pieces as we can 
            without any outside information it's returned as a dictionary.

            The information to be returned should be defined in 
            self.maps loaded from the defs file during 
            __init__. 
        """
    attrib_dict = {}

    log.debug('parsing table %s'%tablename)

    table_split = tablename.split('_') # ASSUMING SECTIONS SPLIT by _  
    table_type = get_table_type(table_split)

    attrib_dict['type'] = table_type
    log.debug('type determined to be %s'%table_type)

    
    for attrib in parsing_maps[table_type]:
        spaceless_attrib = attrib.replace(' ', '_')
        parts  = eval(parsing_maps[table_type][attrib])
        if type(parts) is list: # it could be a string, in which case..
            parts = '_'.join(parts) # we don't want to join them with `_`
        attrib_dict[spaceless_attrib] = parts

    log.debug('\t expanded to -> \n\t%s'\
        %prettify_str(attrib_dict).replace('\n','\n\t'))
    return attrib_dict

def get_table_type( table_split, log= logging):
    """ This function determines the most likely type of this table based 
        on the components of table_split. basically it should be 
        table_split[0] unless it doesn't match. This is WTP convention

        This function relies on the filters defined in parsing rules.
        filters should be a dictionary with various types defined as keys.
        these are the types this function can produce. 

        parsingRules.fileters & parsingRules.filtering_functions
        ------------
            the values to each of these keys should be a dictionary of filters.
            the filter keys should also be found in filtering functions 
            (a dictionary that maps the filtering functions to the actual 
                function objects)
            The filtering functions should take 2 positional arguments,
                1. table_split
                2. the value from the filter (within filters dictionary)
            and return True of False

            e.g. the following should be in parsing rules file.
            filters = {
                'type1':{
                    "filter1":{arg1:1,arg2:2},
                    "filter2":3
                }
            }
            filtering_functions = {
                "filter1":foo1,
                "filter2":foo2
            }
            def foo1(table_split, arg): return True
            def foo2(table_split, arg): return False

            This will say that if table_split is type1, it will pass through
                both filters 1 & 2. i.e. filter1 and filter 2 will return true, 
                as in, table_split should pass  

        args:
            table_split: the table name split by `_`.

        """

    if table_split[0] not in filters:
        log.debug('%s did not match any known filters (%s) return misc'\
            %(table_split,  list(filters.keys())))            
        return 'misc'
    type = table_split[0]

    ### Check for any reason to exclude table from this type
    for aspect in filters[type]:
        # every parsingRules file should have filter_functions and filters
        # defined. they are loaded during __init__

        try:  # if function returns false, this table does not pass and returns misc
            if not filtering_functions[aspect](table_split, filters[type][aspect]):
                return 'misc'
        except NameError as ne:
            log.error("Function %s does not exist in parsingRules file"%filtering_functions[aspect].__name__)
            log.error("Potential correction needed in filtering_functions mapping.")
            log.error(ne)
            raise Exception() 
        except TypeError as te:
            log.error("The function definitions have wrong number of arguments.")
            log.error("Function should take only two arguments, first being table_split list and the second being argument.")
            log.error(te)
            raise Exception()
        except KeyError:
            log.error("The filter (eg.length) attribute does not have a mapped function in filtering_functions")
            raise Exception()
    log.debug('returning type: %s'%type)
    return type


def prettify_str(list_like, indent=2, sort_keys=True):
    """
    Returns a well formatted string with \\n and \\t so that it looks good. 
    Takes a list-like, serializable object
    you can also specify the indent, it defaults to 2

    Throws a TypeError if object is not serializable
    """
    try:
        return json.dumps(list_like, indent=indent, sort_keys = True)
    except:
        print('Cannot Serialize this object in wtp_utils.py prettify_str')
        raise TypeError


