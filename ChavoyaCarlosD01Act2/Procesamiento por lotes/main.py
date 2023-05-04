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
from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import  QMessageBox
from PyQt5.QtGui import *
from PyQt5.QtCore import *



class proceso:
    def __init__(self):
        self.nombre = ""
        self.operacion = ""
        self.op1 = 0
        self.op2 = 0
        self.TME = 0
        self.ID = 0
        self.resultado = 0
        self.numLote = 0

class appCaptura(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()  
        self.ui = Ui_MainWindow1()
        self.ui.setupUi(self)
        self.ventana2 = appProcesos()
        
        self.procesos = []
        self.listaID = []
        self.capturados = 0
        self.totalProcesos = 0
        
        #botones
        self.ui.pushButton_2.clicked.connect(self.activarCampos)
        self.ui.pushButton.clicked.connect(self.capturarDatos)
    
    def mostrarVentana2(self):
        self.ventana2.show()
        self.ventana2.partirEnLotes(self.procesos)
        self.close()
        
    def activarCampos(self):
        self.totalProcesos = self.ui.spinBox_5.value()
        if self.totalProcesos > 0:
            self.ui.spinBox_5.setEnabled(False)
            self.ui.pushButton_2.setEnabled(False)
            self.ui.spinBox_4.setEnabled(True)
            self.ui.lineEdit.setEnabled(True)
            self.ui.spinBox.setEnabled(True)
            self.ui.comboBox.setEnabled(True)
            self.ui.spinBox_2.setEnabled(True)
            self.ui.pushButton.setEnabled(True)
            self.ui.spinBox_3.setEnabled(True)
        else:
            msj = QMessageBox.warning(self,"Advertencia", 
                          "Introducir un número de procesos mayor a 0",
                          QMessageBox.Ok)
            
        
    def capturarDatos(self):
        
        banderaID = False
        banderaOp = False
        banderaTME = False
        nuevo = proceso()
        nuevo.nombre = self.ui.lineEdit.text()
        nuevo.ID = self.ui.spinBox_4.value()
        nuevo.op1 = self.ui.spinBox.value()
        nuevo.op2 = self.ui.spinBox_2.value()
        nuevo.operacion = str(nuevo.op1) +" "+ self.ui.comboBox.currentText()+" "+ str(nuevo.op2)
        
        if nuevo.ID not in self.listaID:
            banderaID = True
            
        else:
            msj = QMessageBox.warning(self,"Advertencia", 
                          "El ID ya existe",
                          QMessageBox.Ok)
        
        if self.ui.comboBox.currentIndex() == 0:
            nuevo.resultado = nuevo.op1 + nuevo.op2
            banderaOp = True
        elif self.ui.comboBox.currentIndex() == 1:
            nuevo.resultado = nuevo.op1 - nuevo.op2
            banderaOp = True
        elif self.ui.comboBox.currentIndex() == 2:
            nuevo.resultado = nuevo.op1 * nuevo.op2
            banderaOp = True
        elif self.ui.comboBox.currentIndex() == 3:
            if nuevo.op2 == 0:
                msj = QMessageBox.warning(self,"Advertencia", 
                              "División entre 0 inválida",
                              QMessageBox.Ok)
            else:
                 nuevo.resultado = nuevo.op1 / nuevo.op2
                 banderaOp = True
        elif self.ui.comboBox.currentIndex() == 4:
            if nuevo.op2 == 0:
                msj = QMessageBox.warning(self,"Advertencia", 
                              "Módulo entre 0 inválida",
                              QMessageBox.Ok)
            else:
                nuevo.resultado = nuevo.op1 % nuevo.op2
                banderaOp = True
            
        nuevo.TME = self.ui.spinBox_3.value()
        if nuevo.TME > 0:
            banderaTME = True
        else:
            msj = QMessageBox.warning(self,"Advertencia", 
                          "Tiempo máximo estimado menor o igual a 0",
                          QMessageBox.Ok)
        
        
            
        if banderaID and banderaOp and banderaTME:
            self.procesos.append(nuevo)
            self.listaID.append(nuevo.ID)
            banderaID = False
            banderaOp = False
            banderaTME = False
            self.limpiarCampos()
            self.ui.label_7.setText(f"Procesos capturados: {len(self.procesos)}")
        
        if len(self.procesos) == self.totalProcesos:
            self.mostrarVentana2()
            
    
    def limpiarCampos(self):
        self.ui.spinBox_4.setValue(0)
        self.ui.lineEdit.clear()
        self.ui.spinBox.setValue(0)
        self.ui.comboBox.setCurrentIndex(0)
        self.ui.spinBox_2.setValue(0)
        self.ui.spinBox_3.setValue(0)
        
        
        
class appProcesos(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow2()
        self.ui.setupUi(self)
        self.listaProcesos = []
        self.aux = []
        self.ui.pushButton.clicked.connect(self.iniciarProcesos)
        self.asignaLote()
        self.ui.progressBar.setStyleSheet("QProgressBar::chunk "
                          "{"
                          "background-color: DeepSkyBlue;"
                          "align: right"
                          "}")
        self.ui.progressBar.setAlignment(QtCore.Qt.AlignCenter)
          
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
        
    def iniciarProcesos(self):
        self.ui.pushButton.setEnabled(False)
        pendientes = len(self.listaProcesos)-1
        totales = len(self.listaProcesos)
        terminados = 0
        contador = 0
        banderaInicio = True
        
        
        self.ui.label_4.setText(f"Terminados: {terminados}")
        self.ui.label.setText(f"Lotes pendientes: {pendientes}")
         
        for i in range(totales):
            procesosLote = len(self.listaProcesos[i])
            self.ui.label_2.setText(f"Lote en ejecución: {i+1}")
            for j in range(len(self.listaProcesos[i])):
                self.ui.progressBar.setValue(0)
                self.ui.tableWidget_2.setRowCount(1)
                self.ui.tableWidget_2.setItem(0,0,QtWidgets.QTableWidgetItem(str(self.listaProcesos[i][j].ID)))
                self.ui.tableWidget_2.setItem(0,1,QtWidgets.QTableWidgetItem(self.listaProcesos[i][j].nombre))
                self.ui.tableWidget_2.setItem(0,2,QtWidgets.QTableWidgetItem(self.listaProcesos[i][j].operacion))
                self.ui.tableWidget_2.setItem(0,3,QtWidgets.QTableWidgetItem(str(self.listaProcesos[i][j].TME)))
                x=j+1
                tableRow = 0
                self.ui.tableWidget.setRowCount(len(self.listaProcesos[i])-x)
                while(x < len(self.listaProcesos[i])):
                    self.ui.tableWidget.setItem(tableRow,0,QtWidgets.QTableWidgetItem(self.listaProcesos[i][x].nombre))
                    self.ui.tableWidget.setItem(tableRow,1,QtWidgets.QTableWidgetItem(str(self.listaProcesos[i][x].TME)))
                    tableRow+=1
                    x+=1
                if banderaInicio:
                    banderaInicio = False
                    QtTest.QTest.qWait(800)
                tableRow = 0
                tiempoRestante = self.listaProcesos[i][j].TME
                progresoPorSegundo = 100//self.listaProcesos[i][j].TME
                progreso = 100%self.listaProcesos[i][j].TME
                while(tiempoRestante > 0):
                    progreso += progresoPorSegundo
                    self.ui.progressBar.setValue(progreso)
                    tiempoRestante -= 1
                    contador+=1
                    self.ui.contador.setText(str(contador))
                    QtTest.QTest.qWait(1000)
                    
                self.ui.tableWidget_3.insertRow(self.ui.tableWidget_3.rowCount()) 
                
                self.ui.tableWidget_3.setItem(self.ui.tableWidget_3.rowCount()-1, 0, QtWidgets.QTableWidgetItem(str(self.listaProcesos[i][j].ID)))
                                              
                self.ui.tableWidget_3.setItem(self.ui.tableWidget_3.rowCount()-1, 1, QtWidgets.QTableWidgetItem(self.listaProcesos[i][j].operacion))
                                                                         
                self.ui.tableWidget_3.setItem(self.ui.tableWidget_3.rowCount()-1, 2, QtWidgets.QTableWidgetItem(str(self.listaProcesos[i][j].resultado)))
                                                                         
                self.ui.tableWidget_3.setItem(self.ui.tableWidget_3.rowCount()-1, 3, QtWidgets.QTableWidgetItem(str(self.listaProcesos[i][j].numLote)))
                self.ui.tableWidget_2.setRowCount(0)
                
                terminados += 1
                self.ui.label_4.setText(f"Terminados: {terminados}")
                
                
            if pendientes != 0:
                pendientes -= 1
                self.ui.label.setText(f"Lotes pendientes: {pendientes}")
            else:
                msj = QMessageBox.information(self,"Aviso", 
                              "Lotes terminados con éxito",
                              QMessageBox.Ok)
                self.ui.label_2.setText("Lote en ejecución: 0")
                self.ui.progressBar.setValue(0)


if __name__=="__main__":
   application = QtCore.QCoreApplication.instance()
   if application is None:
       application=QtWidgets.QApplication(sys.argv)
   application.setQuitOnLastWindowClosed(True)
   GUI = appCaptura()
   GUI.show()
   sys.exit(application.exec_())