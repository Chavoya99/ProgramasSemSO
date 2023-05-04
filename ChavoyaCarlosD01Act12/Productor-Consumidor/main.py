# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 17:27:01 2023

@author: Chavoya
"""

import sys
import random
from pynput import keyboard as kb
from pynput.keyboard import Key
from PrtCsm import *

#librería para la interfaz
from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import  QMessageBox, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class productor:
    casilla = 0
    cantidad = 0
    
class consumidor:
    casilla = 0
    cantidad = 0

class productorConsumidor(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()  
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.scene = QGraphicsScene()
        self.teclaPresionada = None
        self.ui.pushButton.clicked.connect(self.iniciar)
        self.hamburguesa = QtGui.QPixmap("hamburguesa.png")
        self.hamburguesa = self.hamburguesa.scaled(110,110)
        self.plato = QtGui.QPixmap("plato.png")
        self.plato = self.plato.scaled(110, 110)
        
        self.casillas = []
        self.llenarCasillas()
        self.consumidor = consumidor()
        self.productor = productor()
        self.tamanoBuffer= 0
            
    def pulsa(self, tecla):
       if tecla != None:
           self.teclaPresionada = tecla

    def llenarCasillas(self):
        for i in range(2):
            for j in range(11):
                elemento = self.ui.buffer.itemAtPosition(i,j).widget()
                self.casillas.append(elemento)
                elemento.setPixmap(self.plato)            
    
    def iniciar(self):
        self.ui.pushButton.setEnabled(False)
        escuchador = kb.Listener(self.pulsa) #Keyboard listener para detectar pulsación de teclas
        escuchador.start()
        continuar = True
        
        while(continuar):
            banderaProductor = False
            banderaConsumidor = False
            salir = False
            while(not salir):
                volado = random.randint(0, 6)
                cantidad = random.randint(3, 6)
                
                if volado % 2 == 0:#Si sale par entra el productor
                    if self.tamanoBuffer < 22:#Verifica si hay menos de 22 productos
                        self.ui.label.setText("Turno: Productor")
                        banderaProductor = True
                        salir = True

                else:
                    if self.tamanoBuffer > 0:
                        self.ui.label.setText("Turno: Consumidor")
                        banderaConsumidor = True
                        salir = True
                   
            self.ui.label_24.setText(f"Cantidad: {cantidad}")
            
            if banderaProductor:
                productor.cantidad = cantidad
                producido = 0
                
                while(producido < productor.cantidad and self.tamanoBuffer < 22):
                    if productor.casilla == 22:
                        productor.casilla = 0
                    
                    elemento = self.casillas[productor.casilla]
                    elemento.setPixmap(self.hamburguesa)
                    self.tamanoBuffer +=1
                    producido += 1
                    productor.casilla += 1
                    QtTest.QTest.qWait(800)#Contador 1 segundo
                    
                    if self.teclaPresionada == Key.esc:#Termina si se presiona ESC
                        break   
                    
            elif banderaConsumidor:
                consumidor.cantidad = cantidad
                consumido = 0
                
                while(consumido < consumidor.cantidad and self.tamanoBuffer > 0):
                    if consumidor.casilla == 22:
                        consumidor.casilla = 0
                    
                    elemento = self.casillas[consumidor.casilla]
                    elemento.setPixmap(self.plato)
                    self.tamanoBuffer -= 1
                    consumido += 1
                    consumidor.casilla += 1
                    QtTest.QTest.qWait(800)#Contador 1 segundo
                
                    if self.teclaPresionada == Key.esc:#Termina si se presiona ESC
                        break
            
            if self.teclaPresionada == Key.esc:#Termina si se presiona ESC
                break
            
        escuchador.stop()
        msj = QMessageBox.information(self,"Aviso", 
                      "Ejecución finalizada",
                      QMessageBox.Ok)
        self.close()
        
        

if __name__=="__main__":
   application = QtCore.QCoreApplication.instance()
   if application is None:
       application=QtWidgets.QApplication(sys.argv)
   application.setQuitOnLastWindowClosed(True)
   GUI = productorConsumidor()
   GUI.show()
   sys.exit(application.exec_())