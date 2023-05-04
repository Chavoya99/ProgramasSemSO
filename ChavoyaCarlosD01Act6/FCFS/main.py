# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 15:48:57 2023

@author: Chavoya
"""
from ventana1 import *
from ventana2 import *
from ventana3 import *
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
        self.TTB = 0
        self.TLlegada = 0
        self.TFinal = 0
        self.TRetorno = 0
        self.TRespuesta = 0
        self.TEspera = 0
        self.TServicio = 0
        self.resultado = 0
        self.primera = True
        self.estado = "Nuevo"
        

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
        self.ventana2.listaProcesos = self.procesos.copy()
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
        self.ventana3 = appResumen()
        self.ui.setupUi(self)
        self.listaProcesos = []
        self.aux = []
        self.procesoActual = None
        self.ui.pushButton.clicked.connect(self.iniciarProcesos)
        self.teclaPresionada = None
        self.listaTerminados = []
    
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
        pendientes = len(self.listaProcesos)
        totales = len(self.listaProcesos)
        listos = []
        bloqueados = []
        terminados = 0
        contador = 0
        banderaInicio = True
        banderaError = False
        banderaNULO = False
        memoria = 0
        
        self.ui.estado.setText("Ejecución")#Label de estado
        self.ui.estado.setStyleSheet("background-color: #66FF00;")
        self.ui.label_4.setText(f"Terminados: {terminados}")
        self.ui.label.setText(f"Procesos nuevos: {pendientes}")
        self.ui.label_5.setText(f"Bloqueados: {len(bloqueados)}")
        while(terminados != totales):
            while(memoria < 4):
                if len(self.listaProcesos) == 0:
                    break 
                aux = self.listaProcesos.pop(0)
                aux.TLlegada = contador
                aux.estado = "Listo"
                listos.append(aux)
                memoria += 1
                    
                    
            pendientes = len(self.listaProcesos)
            self.ui.label.setText(f"Procesos nuevos: {pendientes}")
            self.ui.label_2.setText(f"Listos: {len(listos)}") 
            
            if len(listos) != 0:
                self.procesoActual = listos.pop(0)
                self.procesoActual.estado = "Ejecucion"
                if self.procesoActual.primera:
                    self.procesoActual.TRespuesta = contador #Asigna tiempo de respuesta
                    self.procesoActual.primera = False #bandera para primer entrada al sistema
            else:
                self.procesoActual = proceso()
                self.procesoActual.ID = -1
                self.procesoActual.operacion = "NULO"
                self.procesoActual.TME = 1
                banderaNULO = True
                
            self.ui.tableWidget_2.setRowCount(1)
            #Tabla De Ejecución
            self.ui.tableWidget_2.setItem(0,0,QtWidgets.QTableWidgetItem(str(self.procesoActual.ID)))
            self.ui.tableWidget_2.setItem(0,1,QtWidgets.QTableWidgetItem(self.procesoActual.operacion))
            self.ui.tableWidget_2.setItem(0,2,QtWidgets.QTableWidgetItem(str(self.procesoActual.TME)))
            self.ui.tableWidget_2.setItem(0,3,QtWidgets.QTableWidgetItem(str(self.procesoActual.TT)))
            self.ui.tableWidget_2.setItem(0,4,QtWidgets.QTableWidgetItem(str(self.procesoActual.TR)))

            x = 0                    
            tableRow = 0
            self.ui.tableWidget.setRowCount(len(listos))
            while(x < len(listos)):
            #Tabla de procesos en espera
                self.ui.tableWidget.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(listos[x].ID)))
                self.ui.tableWidget.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(listos[x].TME)))
                self.ui.tableWidget.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(listos[x].TT)))
                tableRow+=1
                x+=1
 
            
            #Sección de proceso en ejecucion
           
            escuchador = kb.Listener(self.pulsa) #Keyboard listener para detectar pulsación de teclas
            escuchador.start()
            banderaTerminado = True
            banderaBloqueado = False
            
            self.ui.label_2.setText(f"Listos: {len(listos)}")     
            while(self.procesoActual.TT < self.procesoActual.TME):
                
                for i in range(len(bloqueados)):
                    if bloqueados[i].TTB == 8:
                        sale = bloqueados[i]
                        listos.append(sale)
                self.ui.label_2.setText(f"Listos: {len(listos)}")
                y = 0
                while(y < len(bloqueados)):
                   if bloqueados[y].TTB == 8:
                       bloqueados.pop(y)
                       y = 0
                   else:
                       y+=1  
                if banderaNULO:
                    banderaTerminado = False
                    self.procesoActual.TT += 1
                    self.procesoActual.TME += 1
                    if self.teclaPresionada == kb.KeyCode.from_char('p'):
                      self.pausa()
                    self.ui.tableWidget_2.setItem(0,3,QtWidgets.QTableWidgetItem(str(self.procesoActual.TT)))
                    self.ui.tableWidget_2.setItem(0,4,QtWidgets.QTableWidgetItem(str(self.procesoActual.TR)))
                    
                    if len(listos) > 0:    
                        banderaNULO = False
                        break
                    
                else:
                    if self.teclaPresionada == kb.KeyCode.from_char('e'):
                        banderaError = True
                        banderaTerminado = True
                        break
                    elif self.teclaPresionada == kb.KeyCode.from_char('p'):
                        self.pausa()
                    elif self.teclaPresionada == kb.KeyCode.from_char('i'):
                        banderaTerminado = False
                        banderaBloqueado = True
                        break
                        
                    #Actualizando datos de ejecucion
                    self.procesoActual.TT +=1
                    self.procesoActual.TR -=1
                    self.ui.tableWidget_2.setItem(0,3,QtWidgets.QTableWidgetItem(str(self.procesoActual.TT)))
                    self.ui.tableWidget_2.setItem(0,4,QtWidgets.QTableWidgetItem(str(self.procesoActual.TR)))   
                    
     
                x = 0
                tableRow = 0
                self.ui.label_5.setText(f"Bloqueados: {len(bloqueados)}")
                self.ui.tableWidget_4.setRowCount(len(bloqueados))
                while(x < len(bloqueados)):
                    self.ui.tableWidget_4.setRowCount(len(bloqueados))
                    bloqueados[x].TTB += 1
                    self.ui.tableWidget_4.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(bloqueados[x].ID)))
                    self.ui.tableWidget_4.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(bloqueados[x].TTB)))
                    tableRow+=1
                    x+=1
                
                x = 0                    
                tableRow = 0
                self.ui.tableWidget.setRowCount(len(listos))
                while(x < len(listos)):
                #Tabla de procesos en espera
                    self.ui.tableWidget.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(listos[x].ID)))
                    self.ui.tableWidget.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(listos[x].TME)))
                    self.ui.tableWidget.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(listos[x].TT)))
                    tableRow+=1
                    x+=1
                    
                QtTest.QTest.qWait(1000)#Contador 1 segundo
                
    
                
                contador+=1#Contador global
                self.ui.contador.setText(str(contador))
                
                
                
            escuchador.stop()
            self.teclaPresionada = None
                   
            #Tabla de procesos terminados
            if banderaTerminado:
                self.ui.tableWidget_3.insertRow(self.ui.tableWidget_3.rowCount()) 
            
                self.ui.tableWidget_3.setItem(self.ui.tableWidget_3.rowCount()-1, 0, QtWidgets.QTableWidgetItem(str(self.procesoActual.ID)))
                                          
                self.ui.tableWidget_3.setItem(self.ui.tableWidget_3.rowCount()-1, 1, QtWidgets.QTableWidgetItem(self.procesoActual.operacion))
                
                
                if banderaError:
                    self.ui.tableWidget_3.setItem(self.ui.tableWidget_3.rowCount()-1, 2, QtWidgets.QTableWidgetItem("¡Error!"))
                    self.procesoActual.resultado = "¡Error!"
                    banderaError = False
                else:                                         
                    self.ui.tableWidget_3.setItem(self.ui.tableWidget_3.rowCount()-1, 2, QtWidgets.QTableWidgetItem(str(self.procesoActual.resultado)))
                banderaTerminado = False                                                    
                terminados += 1
                self.ui.label_4.setText(f"Terminados: {terminados}")
                self.procesoActual.estado = "Terminado"
                self.procesoActual.TFinal = contador
                self.listaTerminados.append(self.procesoActual)
                memoria -= 1
                
            elif banderaBloqueado:
                self.procesoActual.TTB = 0
                bloqueados.append(self.procesoActual)
                banderaBloqueado = False


        if pendientes > 1:
            pendientes -= 1
            self.ui.label.setText(f"Procesos nuevos: {pendientes}")

        else:
            self.ui.tableWidget_2.setRowCount(0)
            self.ui.estado.setText("Finalizado")#Label de estado
            self.ui.estado.setStyleSheet("background-color: Blue;")
            msj = QMessageBox.information(self,"Aviso", 
                          "Procesos terminados con éxito",
                          QMessageBox.Ok)
            self.ui.label_2.setText("Listos: 0")
            self.ventana3.copiarLista(self.listaTerminados)
            self.ventana3.cargarDatosFinales()
            self.ventana3.show()
            self.close()

class appResumen(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow3()
        self.ui.setupUi(self)
        self.listaTerminados = []
    def copiarLista(self, lista):
        self.listaTerminados = lista.copy()
    def cargarDatosFinales(self):
        self.ui.tableWidget.setRowCount(len(self.listaTerminados))
        tableRow = 0
        for elemento in self.listaTerminados:
            elemento.TServicio = elemento.TT
            elemento.TRetorno = elemento.TFinal - elemento.TLlegada
            elemento.TEspera = elemento.TRetorno - elemento.TServicio
            elemento.TRespuesta -= elemento.TLlegada
            self.ui.tableWidget.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(elemento.ID)))
            self.ui.tableWidget.setItem(tableRow,1,QtWidgets.QTableWidgetItem(elemento.operacion))
            self.ui.tableWidget.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(elemento.resultado)))
            self.ui.tableWidget.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(elemento.TME)))
            self.ui.tableWidget.setItem(tableRow,4,QtWidgets.QTableWidgetItem(str(elemento.TT)))
            self.ui.tableWidget.setItem(tableRow,5,QtWidgets.QTableWidgetItem(elemento.estado))
            self.ui.tableWidget.setItem(tableRow,6,QtWidgets.QTableWidgetItem(str(elemento.TLlegada)))
            self.ui.tableWidget.setItem(tableRow,7,QtWidgets.QTableWidgetItem(str(elemento.TFinal)))
            self.ui.tableWidget.setItem(tableRow,8,QtWidgets.QTableWidgetItem(str(elemento.TRetorno)))
            self.ui.tableWidget.setItem(tableRow,9,QtWidgets.QTableWidgetItem(str(elemento.TRespuesta)))
            self.ui.tableWidget.setItem(tableRow,10,QtWidgets.QTableWidgetItem(str(elemento.TEspera)))
            self.ui.tableWidget.setItem(tableRow,11,QtWidgets.QTableWidgetItem(str(elemento.TServicio)))
            tableRow+=1
            

            

if __name__=="__main__":
   application = QtCore.QCoreApplication.instance()
   if application is None:
       application=QtWidgets.QApplication(sys.argv)
   application.setQuitOnLastWindowClosed(True)
   GUI = appCaptura()
   GUI.show()
   sys.exit(application.exec_())