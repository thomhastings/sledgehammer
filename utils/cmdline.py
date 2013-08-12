''' Functions to handle parsing command line arguments '''

import argparse


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
