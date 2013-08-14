#!/usr/bin/env python3

import argparse
import workHorse
from os.path import expanduser

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="Name of the file")
args = parser.parse_args()

trace = expanduser("~")

trace += '/workspaces/jira-ticket-1401/pom-trace.txt'
wh = workHorse.workHorse(args.filename, trace)

#wh.findParent()
#wh.children()
#wh.descendants()
#wh.contents()
#wh.test()
wh.currentPomAttributes()
