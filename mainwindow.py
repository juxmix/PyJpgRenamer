#!/usr/bin/python
# -*- coding: latin-1 -*-
'''
Created on 7 de febr. 2019

@author: Juanma Sánchez
'''
import Tkinter, tkFileDialog
import logging
from jpgrenamer import jpgrenamer
import os

logging.basicConfig(level=logging.INFO)

class mainwindow:

    def __init__(self):
        self._dirSelected = None
        self._jpgSelected = None

        self._top = Tkinter.Tk()
        self._top.geometry("490x100")

        #campos de texto
        self._frmCampos = Tkinter.Frame(self._top)
        self._frmCampos.winfo_toplevel().title("jpg Renamer")
        self._frmCampos.pack(side=Tkinter.TOP)
        self._lblDir = Tkinter.Label(self._frmCampos,text="Carpeta: ")
        self._txtDir = Tkinter.Text(self._frmCampos, height=1, width=45)
        self._btnDir = Tkinter.Button(self._frmCampos, text="...", command = self.selectDir)
        self._lblJpg = Tkinter.Label(self._frmCampos,text="Imagen: ")
        self._txtJpg = Tkinter.Text(self._frmCampos, height=1, width=45)
        self._btnJpg = Tkinter.Button(self._frmCampos, text="...", command = self.selectJpg)
        self._lblDir.grid(column=0, row = 1)
        self._txtDir.grid(column=1, row = 1)
        self._btnDir.grid(column=2, row = 1)
        self._lblJpg.grid(column=0, row = 2)
        self._txtJpg.grid(column=1, row = 2)
        self._btnJpg.grid(column=2, row = 2)
        #Widgets botones
        self._frmBotones = Tkinter.Frame(self._top)
        self._frmBotones.pack(side=Tkinter.BOTTOM)
        self._btnNormaliza = Tkinter.Button(self._frmBotones, text ="Normaliza", command = self.normaliza)
        self._btnDesNormaliza = Tkinter.Button(self._frmBotones, text ="DesNormaliza", command = self.desNormaliza)
        self._btnEnDirs = Tkinter.Button(self._frmBotones, text ="EnCarpetas", command = self.enCarpetas)
        self._btnSalir = Tkinter.Button(self._frmBotones, text ="Salir", command = quit)
        self._btnNormaliza.grid(column=0, row = 1)
        self._btnDesNormaliza.grid(column=1, row = 1)
        self._btnSalir.grid(column=2, row = 1)
        self._btnEnDirs.grid(column=3,row = 1)
        #go
        self._top.mainloop()

    def normaliza(self):
        if self._dirSelected:
            logging.info("DIR: "+self._dirSelected)
            fotos = self.getJpgsInDir(self._dirSelected)
            for f in fotos:
                #print(f)
                jpgren = jpgrenamer(f)
                jpgren.normalizeJpgName()
        elif self._jpgSelected:
            jpgimg = jpgrenamer(self._jpgSelected)
            self._jpgSelected = jpgimg.normalizeJpgName()
            self._txtJpg.delete(1.0, "end")
            self._txtJpg.insert("end", self._jpgSelected)
            #print(self._jpgSelected)
        else:
            logging.warning("Nada seleccionado")

    def desNormaliza(self):
        if self._dirSelected:
            logging.info("Unnormalize Dir: " + self._dirSelected)
            fotos = self.getJpgsInDir(self._dirSelected)
            for f in fotos:
                jpgren = jpgrenamer(f)
                jpgren.unNormalizeJpgName()
        elif self._jpgSelected:
            jpgimg = jpgrenamer(self._jpgSelected)
            self._jpgSelected = jpgimg.unNormalizeJpgName()
            self._txtJpg.delete(1.0, "end")
            self._txtJpg.insert("end", self._jpgSelected)
            #print(self._jpgSelected)
        else:
            logging.warning("Nada seleccionado")

    def enCarpetas(self):
        if self._dirSelected:
            logging.info("Subcarpeta en: " + self._dirSelected)
            fotos = self.getJpgsInDir(self._dirSelected)
            dirs=set()
            numFotos = 0;
            for f in fotos:
                jpgren=jpgrenamer(f)
                dirs.add(jpgren.getSubFolderName())
                jpgren.toSubFolder()
                #logging.info(jpgren.getFileSinPath()+" -> DIR: "+jpgren.getSubFolderName())
                numFotos += 1
            logging.info("Moved ("+str(numFotos)+") in ("+str(len(dirs))+") folders")

    def getJpgsInDir(self, direc):
        os.chdir(direc) #Reading a nonworking dir get name error
        ficheros = [os.path.abspath(x) for x in os.listdir(direc)]
        fotos = []
        for f in ficheros:
            if f.lower().endswith("jpg"):
                fotos.append(f)
        return fotos

    def selectDir(self):
        #self._top.withdraw()
        self._dirSelected = tkFileDialog.askdirectory()
        logging.debug("DIR: " + self._dirSelected)
        self._txtDir.focus_set()
        self._txtDir.delete(1.0, "end")
        self._txtDir.insert("end", self._dirSelected)
        self._txtJpg.delete(1.0, "end")
        self._jpgSelected = None

    def selectJpg(self):
        self._jpgSelected = tkFileDialog.askopenfilename()
        logging.debug("JPG: " + self._jpgSelected)
        self._txtJpg.focus_set()
        self._txtJpg.delete(1.0, "end")
        self._txtJpg.insert("end", self._jpgSelected)
        self._txtDir.delete(1.0, "end")
        self._dirSelected = None

if __name__ == '__main__':
    mw = mainwindow()
