#!/usr/bin/env python3

__author__ = 'dcatalano'
import sys
from bs4 import BeautifulSoup


class workHorse:

    def __init__(self, filename):
        self.hasParent = False
        self.filename = filename
        try:
            fh = open(self.filename, 'r')
        except OSError:
            print("Oops that was not supposed to happen. Bye...")
            sys.exit(1)
        self.soup = BeautifulSoup(fh, "xml")
        self.

    def currentPomAttributes(self):
        self.groupIdString = self.soup.groupId.string
        print(self.groupIdString)

    def printStuff(self):
        print()

    # strange occurrence, search will not find capital letters in xml tag
    # search for lowercase
    def findParent(self):

        print("project: " + str(self.soup.find_all("project")) + "\n\n")
        print("artifactid: " + str(self.soup.find_all("artifactid")) + "\n\n")
        print("name: " + str(self.soup.find_all("name")) + "\n\n")
        print("version: " + str(self.soup.find_all("version")) + "\n\n")
        print("packaging: " + str(self.soup.find_all("packaging")) + "\n\n")
        model_version_str = str(self.soup.find_all("modelversion"))
        print("modelversion: " + model_version_str + "\n\n")
        print("module: " + str(self.soup.find_all("module")) + "\n\n")
        print("modules: " + str(self.soup.find_all("modules")) + "\n\n")
        print("groupid: " + str(self.soup.find_all("groupid")) + "\n\n")
        print("parent: " + str(self.soup.find_all("parent")) + "\n\n")

    def children(self):
        index = 0
        children_list = self.soup.children
        for i in children_list:
            print("child(" + str(index) + "): " + str(i))
            for j in i:
                print("child(" + str(index + 1) + "): " + str(j))

    def descendants(self):
        descendant_list = self.soup.descendants
        for i in descendant_list:
            print("descendants: " + str(i))

    def contents(self):
        contents_list = self.soup.contents

        if len(contents_list) == 1:
            grand_children = contents_list[0].children
            for i in grand_children:
                #print("grand child.name: " + str(i.name))
                print("grand child.string: " + str(i.string))
                #print("grand child.string: " + i.name)
                #print("grand child.tag: " + str(i.tag))
                #print("grand child.attrs: " + str(i.attrs))

#        while True:
#            try:
#                i = contents_list.pop()
#            except IndexError:
#                break
#            print(str(i))

    def test(self):
        #groupid = self.soup.groupid
        #print(self.soup.prettify())
        #print(str(self.soup.parent))
        #print(str(self.soup.module))
        print(str(self.soup.groupId))
        print(str(self.soup.groupId.name))
        print(str(self.soup.groupId.string))
        #print(str(self.soup.project))
