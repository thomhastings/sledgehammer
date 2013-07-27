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

def cmd_line_args():
    parser = argparse.ArgumentParser(description="Dictionary Attack / Brute force HTTP login credentials")
    parser.add_argument("-t", "--target", type=str, required=True, dest="target")
    parser.add_argument("-d", "--dictionary", type=str, required=True, dest="dict_file")
    return parser.parse_args()

def prefix_print(msg, error=False):
    prefix = "[+]" if not error else "[!]" 
    print prefix + " " + msg


def main():
    args =  cmd_line_args()

    #check word list file exists
    if not os.path.exists(args.dict_file):
        prefix_print("Dictionary file \'%s\' was not found.  Exiting." % (args.dict_file), True)
        sys.exit(0)

    #check url scheme 
    if urlparse.urlparse(args.target).scheme not in ['http', 'https']:
        prefix_print("Incorrect / missing URL scheme on target \'%s\'.  Only HTTP / HTTPS are supported." % (args.target), True)
    
if __name__ == '__main__':
    main()
