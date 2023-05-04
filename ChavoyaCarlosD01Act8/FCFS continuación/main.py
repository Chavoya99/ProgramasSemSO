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
        self.TLlegada = "-"
        self.TFinal = "-"
        self.TRetorno = "-"
        self.TRespuesta = "-"
        self.TEspera = "-"
        self.TServicio = "-"
        self.resultado = 0
        self.primera = True
        self.estado = "Nuevo"
        self.TRCPU = "-"
        
class readOnlyDelegate(QStyledItemDelegate):
    def createEditor(self, parent, option, index):
        return


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
        self.idActual = None
        
        #Desabilitar edición en las tablas
        delegate = readOnlyDelegate(self.ui.tableWidget)
        self.ui.tableWidget.setItemDelegateForColumn(0,delegate)
        self.ui.tableWidget.setItemDelegateForColumn(1,delegate)
        self.ui.tableWidget.setItemDelegateForColumn(2,delegate)
        
        delegate2 = readOnlyDelegate(self.ui.tableWidget_2)
        self.ui.tableWidget_2.setItemDelegateForColumn(0,delegate2)
        self.ui.tableWidget_2.setItemDelegateForColumn(1,delegate2)
        self.ui.tableWidget_2.setItemDelegateForColumn(2,delegate2)
        self.ui.tableWidget_2.setItemDelegateForColumn(3,delegate2)
        self.ui.tableWidget_2.setItemDelegateForColumn(4,delegate2)
        
        delegate3 = readOnlyDelegate(self.ui.tableWidget_3)
        self.ui.tableWidget_3.setItemDelegateForColumn(0,delegate3)
        self.ui.tableWidget_3.setItemDelegateForColumn(1,delegate3)
        self.ui.tableWidget_3.setItemDelegateForColumn(2,delegate3)
        
        delegate4 = readOnlyDelegate(self.ui.tableWidget)
        self.ui.tableWidget_4.setItemDelegateForColumn(0,delegate4)
        self.ui.tableWidget_4.setItemDelegateForColumn(1,delegate4)
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
        self.ventana3.close()
        self._running = True
        self.ui.estado.setText("Ejecución")
        self.ui.estado.setStyleSheet("background-color: #66FF00;")
        
    def crearNuevoProceso(self):
        nuevo = proceso()
        operaciones = ["+","-","*","/","%"]
        nuevo.ID = self.idActual
        nuevo.op1 = random.randint(0, 100)
        operacion = operaciones[random.randint(0,4)]
        
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
        
        self.idActual += 1 #incremento automatico de ID actual para nuevos procesos
        return nuevo #Retorna el nuevo proceso
    
        
    def iniciarProcesos(self):
        self.ui.pushButton.setEnabled(False)
        pendientes = len(self.listaProcesos)
        self.idActual = len(self.listaProcesos)
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
                aux.TServicio = aux.TT
                aux.TRCPU = aux.TME #Cambiar aquí para el tiempo en CPU
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
                    self.procesoActual.TRespuesta -= self.procesoActual.TLlegada
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
                
                if self.teclaPresionada == kb.KeyCode.from_char('n'):
                    nuevo = self.crearNuevoProceso()
                    self.listaProcesos.append(nuevo)
                    pendientes += 1
                    totales += 1
                    if memoria < 4:
                        aux = self.listaProcesos.pop(0)
                        aux.TLlegada = contador
                        aux.TServicio = aux.TT
                        aux.estado = "Listo"
                        listos.append(aux)
                        pendientes -= 1
                        memoria += 1
                        self.ui.label_2.setText(f"Listos: {len(listos)}")
                    self.teclaPresionada = None
                    self.ui.label.setText(f"Procesos nuevos: {pendientes}")
                
                elif self.teclaPresionada == kb.KeyCode.from_char('t'):
                    if banderaNULO:
                        self.ventana3.cargarDatos(contador,self.listaProcesos,listos,bloqueados,self.listaTerminados)
                    else: 
                        self.ventana3.cargarDatos(contador,self.listaProcesos,listos,bloqueados,
                                             self.listaTerminados,self.procesoActual)
                    
                    self.ventana3.show()
                    self.pausa()
                    
                
                for i in range(len(bloqueados)):
                    if bloqueados[i].TTB == 8:
                        sale = bloqueados[i]
                        sale.estado = "Listo"
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
                    self.procesoActual.TServicio = self.procesoActual.TT
                    self.procesoActual.TR -=1
                    self.procesoActual.TRCPU = self.procesoActual.TR #Cambiar aquí para tiempo restante en CPU
                    self.ui.tableWidget_2.setItem(0,3,QtWidgets.QTableWidgetItem(str(self.procesoActual.TT)))
                    self.ui.tableWidget_2.setItem(0,4,QtWidgets.QTableWidgetItem(str(self.procesoActual.TR)))   
                
                #Modificacion para crear un nuevo proceso tecla n    
                
                if self.teclaPresionada == kb.KeyCode.from_char('n'):
                    nuevo = self.crearNuevoProceso()
                    self.listaProcesos.append(nuevo)
                    pendientes += 1
                    totales += 1
                    if memoria < 4:
                        aux = self.listaProcesos.pop(0)
                        aux.TLlegada = contador
                        aux.estado = "Listo"
                        aux.TRCPU = aux.TME
                        listos.append(aux)
                        pendientes -= 1
                        memoria += 1
                    self.teclaPresionada = None
                    self.ui.label.setText(f"Procesos nuevos: {pendientes}")
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
                self.procesoActual.TRCPU = "-"
                self.procesoActual.TServicio = self.procesoActual.TT
                self.procesoActual.TRetorno = self.procesoActual.TFinal - self.procesoActual.TLlegada
                self.procesoActual.TEspera = self.procesoActual.TRetorno - self.procesoActual.TServicio
                self.listaTerminados.append(self.procesoActual)
                memoria -= 1
                
            elif banderaBloqueado:
                self.procesoActual.TTB = 0
                self.procesoActual.estado = "Bloqueado"
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
        self.listaTemp = []
        
        delegate = readOnlyDelegate(self.ui.tableWidget)
        self.ui.tableWidget.setItemDelegateForColumn(0,delegate)
        self.ui.tableWidget.setItemDelegateForColumn(1,delegate)
        self.ui.tableWidget.setItemDelegateForColumn(2,delegate)
        self.ui.tableWidget.setItemDelegateForColumn(3,delegate)
        self.ui.tableWidget.setItemDelegateForColumn(4,delegate)
        self.ui.tableWidget.setItemDelegateForColumn(5,delegate)
        self.ui.tableWidget.setItemDelegateForColumn(6,delegate)
        self.ui.tableWidget.setItemDelegateForColumn(7,delegate)
        self.ui.tableWidget.setItemDelegateForColumn(8,delegate)
        self.ui.tableWidget.setItemDelegateForColumn(9,delegate)
        self.ui.tableWidget.setItemDelegateForColumn(10,delegate)
        self.ui.tableWidget.setItemDelegateForColumn(11,delegate)
        self.ui.tableWidget.setItemDelegateForColumn(12,delegate)

    def copiarLista(self, lista):
        self.listaTerminados = lista.copy()
    
    def cargarDatos(self,contador,nuevos,listos,bloqueados,terminados,ejecucion = None):
        self.listaTemp = []
        if ejecucion:
            ejecucion.TEspera = contador- ejecucion.TLlegada - ejecucion.TServicio
            self.listaTemp.append(ejecucion)
            
        self.listaTemp.extend(nuevos)
        
        for elemento in listos:
            elemento.TEspera = contador - elemento.TLlegada - elemento.TServicio
        self.listaTemp.extend(listos)
        
        for elemento in bloqueados:
            elemento.TEspera = contador - elemento.TLlegada - elemento.TServicio
        
        self.listaTemp.extend(bloqueados)
        self.listaTemp.extend(terminados)
        filasTotales = len(self.listaTemp)
        self.ui.tableWidget.setRowCount(filasTotales)
        tableRow = 0
        for elemento in self.listaTemp:
            self.ui.tableWidget.setItem(tableRow,0,QtWidgets.QTableWidgetItem(str(elemento.ID)))
            self.ui.tableWidget.setItem(tableRow,1,QtWidgets.QTableWidgetItem(elemento.operacion))
            if elemento.estado == "Terminado":
                self.ui.tableWidget.setItem(tableRow,2,QtWidgets.QTableWidgetItem(str(elemento.resultado)))
            else:
                self.ui.tableWidget.setItem(tableRow,2,QtWidgets.QTableWidgetItem("-"))
            self.ui.tableWidget.setItem(tableRow,3,QtWidgets.QTableWidgetItem(str(elemento.TME)))
            self.ui.tableWidget.setItem(tableRow,4,QtWidgets.QTableWidgetItem(str(elemento.TT)))
            self.ui.tableWidget.setItem(tableRow,5,QtWidgets.QTableWidgetItem(elemento.estado))
            self.ui.tableWidget.setItem(tableRow,6,QtWidgets.QTableWidgetItem(str(elemento.TLlegada)))
            self.ui.tableWidget.setItem(tableRow,7,QtWidgets.QTableWidgetItem(str(elemento.TFinal)))
            self.ui.tableWidget.setItem(tableRow,8,QtWidgets.QTableWidgetItem(str(elemento.TRetorno)))
            self.ui.tableWidget.setItem(tableRow,9,QtWidgets.QTableWidgetItem(str(elemento.TRespuesta)))
            self.ui.tableWidget.setItem(tableRow,10,QtWidgets.QTableWidgetItem(str(elemento.TEspera)))
            self.ui.tableWidget.setItem(tableRow,11,QtWidgets.QTableWidgetItem(str(elemento.TServicio)))
            self.ui.tableWidget.setItem(tableRow,12,QtWidgets.QTableWidgetItem(str(elemento.TRCPU)))
            tableRow+=1
        
        
        
        
    def cargarDatosFinales(self):
        self.ui.tableWidget.setRowCount(len(self.listaTerminados))
        tableRow = 0
        for elemento in self.listaTerminados:
            # elemento.TServicio = elemento.TT
            # elemento.TRetorno = elemento.TFinal - elemento.TLlegada
            # elemento.TEspera = elemento.TRetorno - elemento.TServicio
            # elemento.TRespuesta -= elemento.TLlegada
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
            self.ui.tableWidget.setItem(tableRow,12,QtWidgets.QTableWidgetItem(str(elemento.TRCPU)))
            tableRow+=1
            

            

if __name__=="__main__":
   application = QtCore.QCoreApplication.instance()
   if application is None:
       application=QtWidgets.QApplication(sys.argv)
   application.setQuitOnLastWindowClosed(True)
   GUI = appCaptura()
   GUI.show()
   sys.exit(application.exec_())