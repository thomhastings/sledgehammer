'''Worker thread to make login requests with credentials pulled off of Queue'''

import threading 
import Queue

import requests
from utils import prefix_print

class LoginThread(threading.Thread):
    _threadlock = threading.Lock()
    _end_all_threads = False

    def __init__(self, target, in_queue, out_queue):
        self.target = target
        self.in_queue = in_queue
        self.out_queue = out_queue

        super(LoginThread,self).__init__()

    def run(self):
        while True:

            '''
            Class variable _end_all_threads is shared amongst all threads.
            so instead of checking _end_all_threads in the while statement
            (which would not let me acquire the lock first) I check it here
            and explicitly break out of the loop.

            Potentially overkill.  Is reading a shared boolean an atomic operation?
            '''

            LoginThread._threadlock.acquire()
            end = LoginThread._end_all_threads
            LoginThread._threadlock.release()

            if end:
                break

            try:
                data = self.in_queue.get(block=False)
                username = data[0]
                password = data[1]

                msg = "Trying credentials: %s, %s" % (username, password)

                response = requests.get(self.target, auth=(username, password), headers={'Connection': 'close'})

                msg = msg + "\t\t\t[Status Code: %s]" % (response.status_code)

                LoginThread._threadlock.acquire() 
                prefix_print(msg)
                LoginThread._threadlock.release()

                if response.status_code == 200:
                    self.out_queue.put((username, password))

                    #Manipulating a class variable is not thread safe, needs lock
                    LoginThread._threadlock.acquire()
                    LoginThread._end_all_threads = True
                    LoginThread._threadlock.release()

            except Queue.Empty:

                #Manipulating a class variable is not thread safe, needs lock
                LoginThread._threadlock.acquire()
                LoginThread._end_all_threads = True
                LoginThread._threadlock.release()