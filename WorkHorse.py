#!/usr/bin/env python3

__author__ = 'dcatalano'
import sys
from bs4 import BeautifulSoup


class WorkHorse:

    def __init__(self, filename):
        self.hasParent = False
        self.filename = filename
        try:
            fh = open(self.filename, 'r')
        except OSError:
            print("Oops that was not supposed to happen. Bye...")
            sys.exit(1)
        self.soup = BeautifulSoup(fh, "lxml")

    def printStuff(self):
        print()

    # strange occurrence, search will not find capital letters in xml tag search for lowercase
    def findParent(self):

        print("project: " + str(self.soup.find_all("project")) + "\n\n")
        print("artifactid: " + str(self.soup.find_all("artifactid")) + "\n\n")
        print("name: " + str(self.soup.find_all("name")) + "\n\n")
        print("version: " + str(self.soup.find_all("version")) + "\n\n")
        print("packaging: " + str(self.soup.find_all("packaging")) + "\n\n")
        print("modelversion: " + str(self.soup.find_all("modelversion")) + "\n\n")
        print("module: " + str(self.soup.find_all("module")) + "\n\n")
        print("modules: " + str(self.soup.find_all("modules")) + "\n\n")
        print("groupid: " + str(self.soup.find_all("groupid")) + "\n\n")
        print("parent: " + str(self.soup.find_all("parent")) + "\n\n")