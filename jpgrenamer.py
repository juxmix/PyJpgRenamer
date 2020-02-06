#!/usr/bin/python
# -*- coding: latin-1 -*-
import os
import logging
from PIL import Image

class jpgrenamer:
    __normalizedname = None
    """Clase para normalizar los nombres de los jpg"""
    def __init__(self, fullname):
        self.__fullname = fullname
        logging.debug("Fullname: " + fullname)
        self.__pathname = self.getPathFromImgName()
        self.__filename = self.getFileSinPath()
        self.__normalizedname = self.getNormalizedName()

    def getPathFromImgName(self):
        return os.path.dirname(os.path.abspath(self.__fullname))

    def getFileSinPath(self):
        return os.path.basename(self.__fullname)

    def getNamePrefix(self):
        sDate = Image.open(self.__fullname)._getexif()[36867]
        sDate = sDate.replace(':','')
        sDate = sDate.replace(' ','_')
        return sDate + "-"

    def getNormalizedName(self):
        if self.__normalizedname == None:
            if self.isNormalizedJpg():
                self.__normalizedname = self.getFileSinPath()
            else:
                self.__normalizedname = self.getNamePrefix() + self.__filename
        logging.debug(self.__normalizedname)
        return self.__normalizedname

    def isNormalizedJpg(self):
        if self.getFileSinPath().startswith(self.getNamePrefix()):
            return True
        else:
            return False

    def normalizeJpgName(self):
        if not self.isNormalizedJpg():
            oldName = self.__fullname
            newName = os.path.join(self.getPathFromImgName(),self.getNormalizedName())
            os.rename(oldName, newName)
            self.__fullname = newName
            logging.info("OLD: "+oldName+" / NEW: "+self.getNormalizedName())
            return self.__fullname

    def unNormalizeJpgName(self):
        if self.isNormalizedJpg():
            oldName = self.__fullname
            pref = self.getNamePrefix()
            newName = self.getFileSinPath().replace(pref,"")
            newName = os.path.join(self.getPathFromImgName(),newName)
            os.rename(oldName, newName)
            self.__fullname = newName
            self.__pathname = self.getPathFromImgName()
            self.__filename = self.getFileSinPath()
            self.__normalizedname = self.getNormalizedName()
            logging.info("OLD: "+oldName+" / NEW: "+self.__filename)
            return self.__fullname
