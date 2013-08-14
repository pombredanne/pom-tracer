#!/usr/bin/env python3

__author__ = 'dcatalano'
import sys
from bs4 import BeautifulSoup
import os


class workHorse:

    def __init__(self, filename, trace):
        self.filename = filename
        self.trace = trace
        os.remove(self.trace)

    def currentPomAttributes(self):
        try:
            fh = open(self.filename, 'r')
        except OSError:
            print("Oops that was not supposed to happen. Bye...")
            sys.exit(1)

        try:
            wh = open(self.trace, 'x')
        except OSError:
            print("Oops that was not supposed to happen. Bye...")
            sys.exit(1)

        soup = BeautifulSoup(fh, "xml")

        self.writeToFile(soup.find_all('groupId')[soup.find_all('parent')
                                                  is None if 0 else 1], wh)
        self.writeToFile(soup.find_all('artifactId')[soup.find_all('parent')
                                                     is None if 0 else 1], wh)
        self.writeToFile(soup.find_all('packaging')[soup.find_all('parent')
                                                    is None if 0 else 1], wh)
        self.writeToFile(soup.find_all('name')[soup.find_all('parent')
                                               is None if 0 else 1], wh)
        wh.close()

    def writeToFile(self, tag, wh):
        wh.write('tag:')
        wh.write(str(tag))
        wh.write('| name:')
        wh.write(tag.name)
        wh.write('| string:')
        wh.write(tag.string)
        wh.writelines('')

        #wh.write(self.soup.groupId.name)
        #wh.write(' : ')
        #wh.writelines(self.soup.groupId.string)
        #wh.write(' | ')

        #print(self.groupIdString)
        #print(str(self.soup.groupId))
        #print(str(self.soup.groupId.name))
        #print(str(
