''' Functions to handle parsing command line arguments '''

import argparse

def cmd_line_args():
    '''Setup command line options parser, parse arugments and return options tuple.'''

    title_text = "sledgehammer.py - Dictionary Attack / Brute force HTTP login credentials"
    underline =  "-" * len(title_text)
    title_text = "\n" + underline + "\n" + title_text + "\n" + underline


    epilog_text = ("sledgehammer.py is an HTTP authentication dictionary attack tool.\n"
                    "Requires a list of usernames and a list of passwords as input.\n"
                    "The script will make a login request to the target URL using every combination " 
                    "of usernames and passwords from the input files.")

    parser = argparse.ArgumentParser(description=title_text, formatter_class=argparse.RawTextHelpFormatter, epilog=epilog_text) 
    parser.add_argument("URL", type=str, help="target login URL", metavar="target URL")
    parser.add_argument("-p", type=str, required=True, 
        dest="passwords_file", help="text file with list of passwords(one per line)", metavar="<pwdfile>")
    parser.add_argument("-u", type=str, required=True, 
        dest="usernames_file", help="text file with list of usernames(one per line)", metavar="<usrfile>")

    parser.add_argument("-t", type=int, default=5, dest="threads", metavar="<numthreads>", help="number of worker threads making HTTP requests (default: 5)")

    return parser.parse_args()
