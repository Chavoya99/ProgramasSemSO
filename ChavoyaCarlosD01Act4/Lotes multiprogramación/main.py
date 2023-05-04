# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 15:48:57 2023

@author: Chavoya
"""
from ventana1 import *
from ventana2 import *
import time
import os
import sys
import random
from pynput import keyboard as kb

#librería para la interfaz
from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import  QMessageBox
from PyQt5.QtGui import *
from PyQt5.QtCore import *



class proceso:
    def __init__(self):
        self.operacion = ""
        self.op1 = 0
        self.op2 = 0
        self.TME = 0
        self.TT = 0
        self.TR = 0
        self.ID = 0
        self.resultado = 0
        self.numLote = 0

class appCaptura(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()  
        self.ui = Ui_MainWindow1()
        self.ui.setupUi(self)
        self.ventana2 = appProcesos()
        
        self.operaciones = ["+","-","*","/","%"]
        self.procesos = []
        self.listaID = []
        self.capturados = 0
        self.totalProcesos = 0
        
        #botones
        self.ui.pushButton_2.clicked.connect(self.capturarDatos)
        
    
    def mostrarVentana2(self):
        self.ventana2.show()
        self.ventana2.partirEnLotes(self.procesos)
        self.close()
        
            
        
    def capturarDatos(self):
        ID = 0
        self.totalProcesos = self.ui.spinBox_5.value()
        if self.totalProcesos != 0:
            for i in range(self.totalProcesos):
                nuevo = proceso()
                nuevo.ID = ID
                nuevo.op1 = random.randint(0, 100)
                operacion = self.operaciones[random.randint(0,4)]
                
                if operacion == "/" or operacion == "%":
                    nuevo.op2 = random.randint(1, 100) 
                else:
                    nuevo.op2 = random.randint(0,100)
                
                nuevo.operacion = str(nuevo.op1) +" "+ operacion +" "+ str(nuevo.op2)
                nuevo.TME = random.randint(5,16)
                nuevo.TR = nuevo.TME
                    
                
                if operacion == "+":
                    nuevo.resultado = nuevo.op1 + nuevo.op2
                    
                elif operacion == "-":
                    nuevo.resultado = nuevo.op1 - nuevo.op2
                    
                elif operacion == "*":
                    nuevo.resultado = nuevo.op1 * nuevo.op2
                    
                elif operacion == "/":
                         nuevo.resultado = round((nuevo.op1 / nuevo.op2),4)
                         
                elif operacion == "%":
                         nuevo.resultado = nuevo.op1 % nuevo.op2
                
                self.procesos.append(nuevo)
                ID += 1 #incremento automatico de ID
                
            self.mostrarVentana2()
        else:
            msj = QMessageBox.critical(self,"Error", 
                          "Elije una cantidad de procesos mayor a 0",
                          QMessageBox.Ok)
            
     
        
class appProcesos(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow2()
        self.ui.setupUi(self)
        self.listaProcesos = []
        self.aux = []
        self.procesoActual = None
        self.ui.pushButton.clicked.connect(self.iniciarProcesos)
        self.asignaLote()
        self.teclaPresionada = None
    def partirEnLotes(self,lista):
        i = 0
        for j in range(len(lista)):
            self.aux.append(lista[j])
            i += 1
            if(i%4 == 0 or i == len(lista)):
                self.listaProcesos.append(self.aux)
                self.aux = []
        self.asignaLote()
    
    def asignaLote(self):
        for x in range(len(self.listaProcesos)):
            for y in range(len(self.listaProcesos[x])):
                self.listaProcesos[x][y].numLote = x+1
    #Intervenciones de teclado    
    def pulsa(self, tecla):
       if tecla != None:
           self.teclaPresionada = tecla

    def pausa(self):
        self._running = False
        self.ui.estado.setText("Pausa")
        self.ui.estado.setStyleSheet("background-color: Red;")
        while self.teclaPresionada != kb.KeyCode.from_char('c'):
            QtTest.QTest.qWait(500)
        self._running = True
        self.ui.estado.setText("Ejecución")
        self.ui.estado.setStyleSheet("background-color: #66FF00;")
        
    def iniciarProcesos(self):
        self.ui.pushButton.setEnabled(False)
        pendientes = len(self.listaProcesos)-1
        totales = len(self.listaProcesos)
        terminados = 0
        contador = 0
        banderaInicio = True
        banderaError = False
        
        self.ui.estado.setText("Ejecución")#Label de estado
        self.ui.estado.setStyleSheet("background-color: #66FF00;")
        self.ui.label_4.setText(f"Terminados: {terminados}")
        self.ui.label.setText(f"Lotes pendientes: {pendientes}")
         
        for i in range(totales): #Totales es igual a numero de lotes
            #procesosLote = len(self.listaProcesos[i])
            self.ui.label_2.setText(f"Lote en ejecución: {i+1}")
            loteEjecucion = self.listaProcesos[i].copy()
            while(len(loteEjecucion) > 0):
                self.procesoActual = loteEjecucion.pop(0)
                self.ui.tableWidget_2.setRowCount(1)
                #Tabla De Ejecución
                self.ui.tableWidget_2.setItem(0,0,QtWidgets.QTableWidgetItem(str(self.procesoActual.ID)))
                self.ui.tableWidget_2.setItem(0,1,QtWidgets.QTableWidgetItem(self.procesoActual.operacion))
                self.ui.tableWidget_2.setItem(0,2,QtWidgets.QTableWidgetItem(str(self.procesoActual.TME)))
                self.ui.tableWidget_2.setItem(0,3,QtWidgets.QTableWidgetItem(str(self.procesoActual.TT)))
                self.ui.tableWidget_2.setItem(0,4,QtWidgets.QTableWidgetItem(str(self.procesoActual.TR)))
                
                
                x = 0                    
                tableRow = 0
                self.ui.tableWidget.setRowCount(len(loteEjecucion))
                while(x < len(loteEjecucion)):
                #Tabla de procesos en espera
                    self.ui.tableWidget.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(loteEjecucion[x].ID)))
                    self.ui.tableWidget.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(loteEjecucion[x].TME)))
                    self.ui.tableWidget.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(loteEjecucion[x].TT)))
                    tableRow+=1
                    x+=1
                if banderaInicio:
                    banderaInicio = False
                    QtTest.QTest.qWait(800)
                tableRow = 0
                
                #Sección del lote en ejecución
               
                escuchador = kb.Listener(self.pulsa) #Keyboard listener para detectar pulsación de teclas
                escuchador.start()
                banderaTerminado = True
                while(self.procesoActual.TT < self.procesoActual.TME):

                    
                    if self.teclaPresionada == kb.KeyCode.from_char('e'):
                        banderaError = True
                        banderaTerminado = True
                        break
                    elif self.teclaPresionada == kb.KeyCode.from_char('p'):
                        self.pausa()
                    elif self.teclaPresionada == kb.KeyCode.from_char('i'):
                        if len(loteEjecucion) > 0:
                            banderaTerminado = False
                            break
                        
                    #Actualizando datos
                    self.procesoActual.TT +=1
                    self.procesoActual.TR -=1
                    self.ui.tableWidget_2.setItem(0,3,QtWidgets.QTableWidgetItem(str(self.procesoActual.TT)))
                    self.ui.tableWidget_2.setItem(0,4,QtWidgets.QTableWidgetItem(str(self.procesoActual.TR)))    
                    
                    contador+=1#Contador global
                    self.ui.contador.setText(str(contador))
                    QtTest.QTest.qWait(1000)#Contador 1 segundo
                    
                    
                escuchador.stop()
                self.teclaPresionada = None
                #Tabla de procesos terminados
                if banderaTerminado:
                    self.ui.tableWidget_3.insertRow(self.ui.tableWidget_3.rowCount()) 
                
                    self.ui.tableWidget_3.setItem(self.ui.tableWidget_3.rowCount()-1, 0, QtWidgets.QTableWidgetItem(str(self.procesoActual.ID)))
                                              
                    self.ui.tableWidget_3.setItem(self.ui.tableWidget_3.rowCount()-1, 1, QtWidgets.QTableWidgetItem(self.procesoActual.operacion))
                    
                    self.ui.tableWidget_3.setItem(self.ui.tableWidget_3.rowCount()-1, 3, QtWidgets.QTableWidgetItem(str(self.procesoActual.numLote)))
                    
                    if banderaError:
                        self.ui.tableWidget_3.setItem(self.ui.tableWidget_3.rowCount()-1, 2, QtWidgets.QTableWidgetItem("¡Error!"))
                        banderaError = False
                    else:                                         
                        self.ui.tableWidget_3.setItem(self.ui.tableWidget_3.rowCount()-1, 2, QtWidgets.QTableWidgetItem(str(self.procesoActual.resultado)))
                    banderaTerminado = False                                                    
                    terminados += 1
                    self.ui.label_4.setText(f"Terminados: {terminados}")
                else:
                    loteEjecucion.append(self.procesoActual)
                
                self.ui.tableWidget_2.setRowCount(0)
    
            if pendientes != 0:
                pendientes -= 1
                self.ui.label.setText(f"Lotes pendientes: {pendientes}")
            else:
                self.ui.estado.setText("Finalizado")#Label de estado
                self.ui.estado.setStyleSheet("background-color: Blue;")
                msj = QMessageBox.information(self,"Aviso", 
                              "Lotes terminados con éxito",
                              QMessageBox.Ok)
                self.ui.label_2.setText("Lote en ejecución: 0")


if __name__=="__main__":
   application = QtCore.QCoreApplication.instance()
   if application is None:
       application=QtWidgets.QApplication(sys.argv)
   application.setQuitOnLastWindowClosed(True)
   GUI = appCaptura()
   GUI.show()
   sys.exit(application.exec_())