#!/usr/bin/env python
'''
Filename:        sledgehammer.py
Author:            Phil Grohe

Description:
HTTP login dicionary attack / brute forcing tool
'''

import argparse
import os.path
import sys
import urlparse
import requests
import itertools

def cmd_line_args():
    parser = argparse.ArgumentParser(description="Dictionary Attack / Brute force HTTP login credentials")
    parser.add_argument("target", type=str, help="Target URL")
    parser.add_argument("-p", "--password", type=str, required=True, 
        dest="passwords_file")
    parser.add_argument("-u", "--username", type=str, required=True, 
        dest="usernames_file", help="File with list of usernames")

    return parser.parse_args()

def prefix_print(msg, error=False):
    prefix = "[+]" if not error else "[!]"
    print prefix + " " + msg

def abort_on_missing_file(filename):
    if not os.path.exists(filename):
        prefix_print("File \'%s\' was not found.  Exiting." % (filename), True)
        sys.exit(0)

def try_credentials(username, password):
    #stub for testing
    print "Trying credentials: %s, %s" % (username, password)

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
        for uname in uname_infile:
            cur_uname = uname.rstrip()
            for pwd in pwd_infile:
                cur_pwd = pwd.rstrip()
                try_credentials(cur_uname, cur_pwd)
            pwd_infile.seek(0);
        '''
        for x in itertools.product(uname_infile, pwd_infile):
            try_credentials(x[0].rstrip(), x[1].rstrip())
        ''' 


if __name__ == '__main__':
    main()
