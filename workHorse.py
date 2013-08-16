#!/usr/bin/env python3

__author__ = 'dcatalano'

import sys
from bs4 import BeautifulSoup
import os
from os.path import expanduser


class workHorse:

    def __init__(self, pathToPom):
        self.pathToPom = pathToPom
        self.m2dir = expanduser('~') + '/.m2/repository/'
        self.listOfPomsAndAttributes = []

    def setm2dir(self, m2dir):
        self.m2dir = m2dir

    def currentPomAttributes(self):
        try:
            fh = open(self.pathToPom, 'r')
        except OSError:
            print("Oops, that was not supposed to happen. Can't open \"" + str(self.pathToPom) + "\". Bye...")
            sys.exit(1)

        self.soup = BeautifulSoup(fh, "xml")
        fh.close()

        self.parent_data = []
        self.module_data = []
        self.current_pom_data = []

        self.checkListForParent('groupId')
        self.checkListForParent('artifactId')
        self.checkListForParent('packaging')
        self.checkListForParent('name')
        self.checkListForParent('version')
        self.checkListForParent('relativePath')
        self.checkListForParent('module')

        # TODO switch order since parent changes path to pom.xml and current uses it
        parentDict = self.parentDataToDict(self.parent_data)
        moduleList = self.moduleDataToDict(self.module_data)
        currentPomDict = self.currentPomDataToDict(self.current_pom_data)

        levelDict = {'current': currentPomDict,
                     'parent': parentDict,
                     'module': moduleList}

        self.listOfPomsAndAttributes.append(levelDict)
        if self.pathToPom is not None:
            self.currentPomAttributes()

        return self.listOfPomsAndAttributes

    def checkListForParent(self, search_string):
        the_list = self.soup.find_all(search_string)

        for element in the_list:
            parent_info = element.find_parent()
            if parent_info.name == 'parent':
                self.parent_data.append(element)
            elif parent_info.name == 'modules':
                self.module_data.append(element)
            elif parent_info.name == 'project':
                self.current_pom_data.append(element)

    def parentDataToDict(self, listOfTagsFromParent):
        parentDict = {}
        for element in listOfTagsFromParent:
            parentDict.update({element.name: element.string})

        # TODO add K path V self.pathToPom
        if len(listOfTagsFromParent) > 0:
            self.pathToPom = self.getFilenameOfNextPom(parentDict)
        else:
            self.pathToPom = None
        return parentDict

    def moduleDataToDict(self, listOfTagsFromParent):
        moduleList = []
        for element in listOfTagsFromParent:
            # TODO create a new workhorse object and run currentPomAttributes() attach list to
            moduleList.append({element.name: element.string})

        return moduleList

    def currentPomDataToDict(self, listOfTagsFromParent):
        currentPomDict = {}
        for element in listOfTagsFromParent:
            currentPomDict.update({element.name: element.string})
        # TODO add K path V self.pathToPom
        return currentPomDict

    def getFilenameOfNextPom(self, parentDict):
        group = parentDict['groupId']
        group = group.replace('.', '/')
        directoryToPom = str(self.m2dir) + str(group) + '/' + str(parentDict['artifactId']) + '/' \
                         + str(parentDict['version']) + '/' + str(parentDict['artifactId']) + '-' \
                         + str(parentDict['version']) + '.pom'
        return directoryToPom

    def writeToFile(self, filename, tag):
        if os.path.isfile(filename):
            os.remove(filename)
        try:
            wh = open(filename, 'x')
        except OSError:
            print("Oops, that was not supposed to happen. Can't open \"" + filename + "\". Bye...")
            sys.exit(1)

        wh.write(str(self.pathToPom))
        wh.write('\n')
        wh.write('name:')
        wh.write(tag.name)
        wh.write('| string:')
        wh.write(tag.string)
        wh.write('| tag:')
        wh.write(str(tag))
        wh.write('\n\n')

        wh.close()