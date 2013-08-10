#!/usr/bin/env python3

import sys
import argparse
import WorkHorse

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="Name of the file")
args = parser.parse_args()

wh = WorkHorse.WorkHorse(args.filename)

wh.findParent()