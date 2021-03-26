#!/usr/bin/python3
# -*- coding: latin-1 -*-
import os
import logging
import re
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
        self.__folderName = self.getSubFolderName()

    def getPathFromImgName(self):
        return os.path.dirname(os.path.abspath(self.__fullname))

    def getFileSinPath(self):
        return os.path.basename(self.__fullname)

    def getNamePrefix(self):
        try:
            sDate = Image.open(self.__fullname)._getexif()[36867]
            logging.debug("RAW EXIF DATE: " + sDate)
        except Exception as e:
            sDate = None
            logging.warning("Error reading EXIF Date of: "+ self.getFileSinPath())

        regexpdate = re.compile('\d{4}:\d{2}:\d{2} \d{2}:\d{2}:\d{2}')
        if sDate != None and regexpdate.match(sDate):
            #logging.info("Valid date")
            sDate = sDate.replace(':','')
            sDate = sDate.replace(' ','_')
            return sDate + "-"
        else:
            #raise Exception("Invalid EXIF date tag: "+sDate)
            return None

    def getNormalizedName(self):
        if self.__normalizedname == None:
            if self.isNormalizedJpg():
                self.__normalizedname = self.getFileSinPath()
            else:
                pref = self.getNamePrefix()
                if pref == None: #Error in EXIF Date
                    self.__normalizedname = self.__filename
                else: #Date OK
                    self.__normalizedname = pref + self.__filename
        logging.debug("Normalized name: " + self.__normalizedname)
        return self.__normalizedname

    def getSubFolderName(self):
        dir = self.getNamePrefix()
        if dir == None:
            __folderName = None
        else:
            dir = dir[:dir.index("_")]
            __folderName = dir[:4] + "-" +dir[4:6]+"-"+dir[6:]
        #logging.debug("SUBDIR: "+ __folderName)
        return __folderName

    def toSubFolder(self):
        path = self.getPathFromImgName()
        subdir = self.getSubFolderName()
        if subdir != None:
            todir =  path + os.path.sep + subdir
            if os.path.isdir(todir):
                #logging.info("Dir: " + todir + " existe!")
                pass
            else:
                os.mkdir(todir)
            #Here the folder exists
            tofile = todir + os.path.sep + self.getFileSinPath()
            logging.info("FROM: "+self.__fullname+" -> ."+os.path.sep+self.getSubFolderName())
            os.rename(self.__fullname, tofile)
            #Update fields
            self.__fullname = tofile
            self.__pathname = self.getPathFromImgName()
            self.__filename = self.getFileSinPath()
            self.__normalizedname = self.getNormalizedName()
            self.__folderName = self.getSubFolderName()
        else:
            logging.warning("Invalid EXIF Date. Not moving: '" + self.getFileSinPath()+"'")

    def isNormalizedJpg(self):
        pref = self.getNamePrefix()
        if pref != None and self.getFileSinPath().startswith(pref):
            return True
        else:
            return False

    def normalizeJpgName(self):
        if not self.isNormalizedJpg():
            pref = self.getNamePrefix()
            if pref != None:
                oldName = self.__fullname
                newName = os.path.join(self.getPathFromImgName(),self.getNormalizedName())
                os.rename(oldName, newName)
                self.__fullname = newName
                logging.info("OLD: "+oldName+" / NEW: "+self.getNormalizedName())
            else:
                logging.warning("Invalid EXIF date. Not renaming "+self.getFileSinPath())
            return self.__fullname

    def unNormalizeJpgName(self):
        if self.isNormalizedJpg() and self.getNamePrefix() != None:
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
        elif self.getNamePrefix() == None:
            logging.warning("Invalid EXIF Date. Not unnormalizing: " + self.getFileSinPath())
        return self.__fullname
