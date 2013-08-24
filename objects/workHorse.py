#!/usr/bin/env python3

__author__ = 'dcatalano'

import sys
import re
import os
from os.path import expanduser
from bs4 import BeautifulSoup

class workHorse:

    def __init__(self, pathToPom):
        self.pathToPom = pathToPom
        self.m2dir = expanduser('~') + '/.m2/repository/'
        self.listOfPomsAndAttributes = []
        self.rootPomDir = os.path.dirname(self.pathToPom)
        self.currentPomDir = os.path.dirname(self.pathToPom)

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

        self.module_data = []
        self.current_pom_data = []
        self.parent_data = []

        self.checkListForParent('groupId')
        self.checkListForParent('artifactId')
        self.checkListForParent('packaging')
        self.checkListForParent('name')
        self.checkListForParent('version')
        self.checkListForParent('relativePath')
        self.checkListForParent('module')

        currentPomDict = self.currentPomDataToDict(self.current_pom_data)
        moduleList = self.moduleDataToDict(self.module_data)
        parentDict = self.parentDataToDict(self.parent_data)

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

    def currentPomDataToDict(self, listOfTagsFromParent):
        currentPomDict = {}
        for element in listOfTagsFromParent:
            currentPomDict.update({element.name: element.string})
        currentPomDict.update({'pathToFile': self.pathToPom})
        return currentPomDict

    def moduleDataToDict(self, listOfTagsFromParent):
        moduleList = []
        for element in listOfTagsFromParent:
            # TODO create a new workhorse object and run currentPomAttributes() attach list to
            if element.name == 'module':
                filename = self.getFilenameOfModulePom(element.string)
                self.currentPomDir = os.path.dirname(filename)
                wh = workHorse(filename)
                hierarchy = wh.currentPomAttributes()
                moduleList.append({element.name: element.string, 'moduleHierarchy': hierarchy})
            else:
                moduleList.append({element.name: element.string})

        return moduleList

    def parentDataToDict(self, listOfTagsFromParent):
        parentDict = {}
        for element in listOfTagsFromParent:
            parentDict.update({element.name: element.string})

        if len(listOfTagsFromParent) > 0:
            self.pathToPom = self.getFilenameOfNextPom(parentDict)
            parentDict.update({'pathToFile': self.pathToPom})
        else:
            self.pathToPom = None
        return parentDict

    def getFilenameOfNextPom(self, parentDict):
        group = parentDict['groupId']
        group = group.replace('.', '/')
        directoryToPom = str(self.m2dir) + str(group) + '/' + str(parentDict['artifactId']) + '/' \
                         + str(parentDict['version']) + '/' + str(parentDict['artifactId']) + '-' \
                         + str(parentDict['version']) + '.pom'
        return directoryToPom

    def getFilenameOfModulePom(self, directoryToFile):
        match = re.search('(^([\.])(/(.+[pom\.][xml]))$)', directoryToFile)
        if match is not None:
            #print(self.currentPomDir + match.group(3))
            modulePomFile = self.currentPomDir + match.group(3)
            return modulePomFile
            # print(match.group(3))
            # print(match.groups())
            # print(str(match))
        else:
            modulePomFile = self.rootPomDir + '/' + directoryToFile + '/pom.xml'
            return modulePomFile

    def writeToFile(self, filename):
        if os.path.isfile(filename):
            os.remove(filename)
        try:
            wh = open(filename, 'x')
        except OSError:
            print("Oops, that was not supposed to happen. Can't open \"" + filename + "\". Bye...")
            sys.exit(1)

        # TODO - not implemented yet
        wh.close()