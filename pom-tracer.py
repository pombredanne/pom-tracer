#!/usr/bin/env python3

import argparse
import workHorse
from os.path import expanduser

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="Name of the file")
args = parser.parse_args()

trace = expanduser("~") + '/workspaces/jira-ticket-1401/pom-trace.txt'

if args.filename[0] == '~':
    args.filename = expanduser('~') + args.filename[1:]

wh = workHorse.workHorse(args.filename, trace)
wh.currentPomAttributes()
