'''Miscellaneous utility code'''

import os.path

def prefix_print(msg, error=False):
    '''Print to stdout with a [+] or a [!] depending on error param.'''

    prefix = "[+]" if not error else "[!]"
    print prefix + " " + msg

def abort_on_missing_file(filename):
    '''Check if files exist and exit with message if they do not. '''

    if not os.path.exists(filename):
        prefix_print("File \'%s\' was not found.  Exiting." % (filename), True)
        sys.exit(0)
