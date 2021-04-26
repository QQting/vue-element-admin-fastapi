#!/usr/bin/env python3

import multiprocessing
import subprocess
import sys, getopt
import atexit
from signal import signal, SIGINT

import os
os.environ['LD_LIBRARY_PATH'] = os.getcwd()

def usage():
    print("Usage:")
    print("\t-n <device_num>")
    print("\t-s <start_id>")
    print("Example:")
    print("\tpython multi_agents.py -n 5 -s 5566")    

def worker(id):
    """thread worker function"""
    subprocess.run(["./agent_example", "--id", str(id)])
    return

def sig_handler(arg1, arg2):
    for p in multiprocessing.active_children():
        p.terminate()
    sys.exit()

def main(args):
    try:
        opts, args = getopt.getopt(args, "hn:s:", ["help", "num=", "start_id="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    number = 1
    start_id = 1
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-n", "--number"):
            number = int(a)
        elif o in ("-s", "--start_id"):
            start_id = int(a)
        else:
            assert False, "unhandled option"    

    print("number=%d, start_id=%d" % (number, start_id))

    jobs = []
    for i in range(number):
        p = multiprocessing.Process(target=worker, args=((start_id+i),))
        jobs.append(p)
        p.start()

    signal(SIGINT, sig_handler)


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) == 0:
        usage()
    else:
        main(args)
