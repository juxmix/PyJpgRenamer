'''
Created on 7 de febr. 2019

@author: super
'''
import Tkinter, tkFileDialog
from jpgrenamer import jpgrenamer
import os

class mainwindow:
 
    def __init__(self):
        self._dirSelected = None
        self._jpgSelected = None
        
        self._top = Tkinter.Tk()
        self._top.geometry("390x100")

        #campos de texto
        self._frmCampos = Tkinter.Frame(self._top)
        self._frmCampos.pack(side=Tkinter.TOP)
        self._lblDir = Tkinter.Label(self._frmCampos,text="Carpeta: ")
        self._txtDir = Tkinter.Text(self._frmCampos, height=1, width=30)
        self._btnDir = Tkinter.Button(self._frmCampos, text="...", command = self.selectDir)
        self._lblJpg = Tkinter.Label(self._frmCampos,text="Imagen: ")
        self._txtJpg = Tkinter.Text(self._frmCampos, height=1, width=30)
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
        self._btnSalir = Tkinter.Button(self._frmBotones, text ="Salir", command = quit)
        self._btnNormaliza.grid(column=0, row = 1)
        self._btnDesNormaliza.grid(column=1, row = 1)
        self._btnSalir.grid(column=2, row = 1)        
        #go
        self._top.mainloop()
  
    def normaliza(self):
        if self._dirSelected:
            print(self._dirSelected)
            fotos = self.getJpgsInDir(self._dirSelected)
            for f in fotos:
                jpgren = jpgrenamer(f)
                jpgren.normalizeJpgName()
        elif self._jpgSelected:
            #print(self._jpgSelected)
            jpgimg = jpgrenamer(self._jpgSelected)
            self._jpgSelected = jpgimg.normalizeJpgName()
            self._txtJpg.delete(1.0, "end")
            self._txtJpg.insert("end", self._jpgSelected)            
            print(self._jpgSelected)
        else:
            print("Nada seleccionado")
   
    def desNormaliza(self):
        if self._dirSelected:
            print(self._dirSelected)
            fotos = self.getJpgsInDir(self._dirSelected)
            for f in fotos:
                jpgren = jpgrenamer(f)
                jpgren.unNormalizeJpgName()                     
        elif self._jpgSelected:
            #print(self._jpgSelected)
            jpgimg = jpgrenamer(self._jpgSelected)
            self._jpgSelected = jpgimg.unNormalizeJpgName()
            self._txtJpg.delete(1.0, "end")
            self._txtJpg.insert("end", self._jpgSelected)            
            print(self._jpgSelected)
        else:
            print("Nada seleccionado")
    
    def getJpgsInDir(self, direc):
        ficheros = [os.path.abspath(x) for x in os.listdir(direc)]
        fotos = []
        for f in ficheros:
            if f.lower().endswith("jpg"):
                fotos.append(f)    
        return fotos
        
    def selectDir(self):
        #self._top.withdraw()
        self._dirSelected = tkFileDialog.askdirectory()
        print("DIR: " + self._dirSelected)
        self._txtDir.focus_set()
        self._txtDir.delete(1.0, "end")
        self._txtDir.insert("end", self._dirSelected)
        self._txtJpg.delete(1.0, "end")
        self._jpgSelected = None
    
    def selectJpg(self):
        self._jpgSelected = tkFileDialog.askopenfilename()
        print("JPG: " + self._jpgSelected)
        self._txtJpg.focus_set()
        self._txtJpg.delete(1.0, "end")
        self._txtJpg.insert("end", self._jpgSelected)
        self._txtDir.delete(1.0, "end")
        self._dirSelected = None
        
if __name__ == '__main__':
    mw = mainwindow() 