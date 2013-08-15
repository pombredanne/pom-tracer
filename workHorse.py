#!/usr/bin/env python3

__author__ = 'dcatalano'
import sys
from bs4 import BeautifulSoup
import os
from os.path import expanduser


class workHorse:

    def __init__(self, filename, trace):
        self.filename = filename
        self.trace = trace
        os.remove(self.trace)
        self.m2dir = expanduser('~')
        self.m2dir += '/.m2/repository/'
        self.parent_data = []
        self.parent_data2 = []

    def currentPomAttributes(self):
        try:
            fh = open(self.filename, 'r')
        except OSError:
            print("Oops that was not supposed to happen. Bye...")
            sys.exit(1)

        try:
            self.wh = open(self.trace, 'x')
        except OSError:
            print("Oops that was not supposed to happen. Bye...")
            sys.exit(1)

        soup = BeautifulSoup(fh, "xml")

        groupId_list = soup.find_all('groupId')
        artifactId_list = soup.find_all('artifactId')
        packaging_list = soup.find_all('packaging')
        name_list = soup.find_all('name')
        version_list = soup.find_all('version')
        relativePath_list = soup.find_all('relativePath')

        self.checkListForParent(groupId_list)
        self.checkListForParent(artifactId_list)
        self.checkListForParent(packaging_list)
        self.checkListForParent(name_list)
        self.checkListForParent(version_list)
        self.checkListForParent(relativePath_list)

        self.extract_parent_data(self.parent_data)
        for i in self.parent_data2:
            #print(str(i.items()))
            print(str(i.keys()) + '\n')
            print(str(i.values()) + '\n')
        #parent_data2.items
        self.wh.close()

    def __currentPomAttributes(self):
        print('internal wrapped method')

    def checkListForParent(self, the_list):
        for element in the_list:
            parent_info = element.find_parent()
            if parent_info.name == 'parent':
                #self.save_for_next_iteration(element)
                self.parent_data.append(element)
            else:
                self.writeToFile(element)

    def writeToFile(self, tag):
        #self.wh.write(str(self.filename))
        #self.wh.write('\n')
        #self.wh.write('name:')
        #self.wh.write(tag.name)
        #self.wh.write('| string:')
        #self.wh.write(tag.string)
        #self.wh.write('| tag:')
        self.wh.write(str(tag))
        self.wh.write('\n\n')

    def extract_parent_data(self, listOfTagsFromParent):
        parentDict = {}
        #print(str(type(listOfTagsFromParent)))
        for element in listOfTagsFromParent:
            #print(str(type(element.name)))
            #print(str(type(str(element.string))))
            #print(str(type(element.tag)))
            parentDict.update({element.name: element.string})
        self.parent_data2.append(parentDict)
