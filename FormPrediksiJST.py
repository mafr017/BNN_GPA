import sys
import time
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QMessageBox, QTableWidgetItem, QDialog, QFileDialog
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtWidgets
from JST import *
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar2QT)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

class FormPrediksiJST(QMainWindow):

    #variabel global untuk menentukan jumlah data latih dan jumlah data uji
    n_datalatih = 100
    n_datauji = 21

    #menciptakan objek dari kelas JST
    jst = JaringanSyarafTiruan()
    pre = DPreparation()
    tra = DTransformation()

    #pendefinisian init self
    def __init__(self):
        QMainWindow.__init__(self)
        loadUi ("gui/gui_jst.ui", self) #memanggil file gui_jst.ui
        self.setWindowTitle("Prediksi IPK Mahasiswa Sistem Komputer S1 - JST BACKPROPAGATION")
        self.pbBaca.clicked.connect(self.BacaData)
        self.pbBaca_2.clicked.connect(self.BacaData_2)
        self.pbBobot.clicked.connect(self.BacaBobot)
    
    #pendefinisian proses mulai normalisasi
    def Pronor(self, data):
        #mengakses data berdasarkan kolom/parameter
        key = data[:, 0]
        x1  = data[:, 1]
        x2  = data[:, 2]
        x3  = data[:, 3]
        x4  = data[:, 4]
        x5  = data[:, 5]
        x6  = data[:, 6]
        x7  = data[:, 7]
        x8  = data[:, 8]
        x9  = data[:, 9]
        x10 = data[:, 10]
        x11 = data[:, 11]
        x12 = data[:, 12]
        x13 = data[:, 13]
        x14 = data[:, 14]
        x15 = data[:, 15]
        x16 = data[:, 16]
        x17 = data[:, 17]
        x18 = data[:, 18]
        ipk = data[:, 19]

        #normalisasi data menggunakan fungsi Normalisasi kelas JST
        x1  = self.tra.Normalisasi(x1)
        x2  = self.tra.Normalisasi(x2)
        x3  = self.tra.Normalisasi(x3)
        x4  = self.tra.Normalisasi(x4)
        x5  = self.tra.Normalisasi(x5)
        x6  = self.tra.Normalisasi(x6)
        x7  = self.tra.Normalisasi(x7)
        x8  = self.tra.Normalisasi(x8)
        x9  = self.tra.Normalisasi(x9)
        x10 = self.tra.Normalisasi(x10)
        x11 = self.tra.Normalisasi(x11)
        x12 = self.tra.Normalisasi(x12)
        x13 = self.tra.Normalisasi(x13)
        x14 = self.tra.Normalisasi(x14)
        x15 = self.tra.Normalisasi(x15)
        x16 = self.tra.Normalisasi(x16)
        x17 = self.tra.Normalisasi(x17)
        x18 = self.tra.Normalisasi(x18)
        ipk = self.tra.Normalisasi(ipk)

        #menggabungkan data-data normalisasi menjadi dataset
        data_normalisasi = np.concatenate((x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, ipk), axis=1)
                
        return data_normalisasi, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, ipk

    #mendefinisikan fungsi untuk melakukan pembacaan data latih
    def BacaData(self):
        try:
            path = QFileDialog.getOpenFileName(self, 'Silahkan pilih file data pelatihan', '', "CSV files (*.csv)")
            namafile = path[0]
            np.set_printoptions(suppress=True, linewidth=np.inf)
            data_latih = pd.read_csv(namafile, sep=',')
            data_latih = np.array(data_latih)

            #menentukan jumlah data latih
            total_data  = len(data_latih)
            n_datalatih = total_data

            #menjalankan fungsi normalisasi data
            data = data_latih
            data_normalisasi, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, ipk = self.Pronor(data)
            
            #menentukan data latih dan target output
            input_latih = data_normalisasi[:, 0:18]
            target_output = data_normalisasi[:, 18]
            
            #menampilkan data latih pada tabel
            self.tbDataLat.setRowCount(n_datalatih)
            for i in range(n_datalatih):
                self.tbDataLat.setItem(i,0,QTableWidgetItem(str(int(data[i,0])))) #membaca parameter NIM
                for j in range(18):
                    k = j + 1
                    self.tbDataLat.setItem(i,k,QTableWidgetItem(str(input_latih[i,j]))) #membaca paramater input latih x1-x18
                self.tbDataLat.setItem(i,19,QTableWidgetItem(str(target_output[i]))) #membaca parameter target(IPK)

            #menampilkan total data latih
            self.eTotalDLatih.setText(str(n_datalatih))

            #menyimpan data latih ke dalam variabel global
            self.n_datalatih = n_datalatih
            self.data_latih = data_latih
            self.input_latih = input_latih
            self.target_output = target_output

        except:
            print('Terjadi kesalahan pada proses pembacaan data',sys.exc_info())

    #mendefinisikan fungsi untuk melakukan pembacaan data uji
    def BacaData_2(self):
        try:
            path = QFileDialog.getOpenFileName(self, 'Silahkan pilih file data pengujian', '', "CSV files (*.csv)")
            namafile = path[0]
            np.set_printoptions(suppress=True, linewidth=np.inf)
            data_uji = pd.read_csv(namafile, sep=',')
            data_uji = np.array(data_uji)

            data = np.concatenate((self.data_latih, data_uji))

            #menentukan jumlah data uji
            total_data  = len(data_uji)
            n_datauji = total_data

            #menjalankan fungsi normalisasi data
            datauji_normalisasi, x1u, x2u, x3u, x4u, x5u, x6u, x7u, x8u, x9u, x10u, x11u, x12u, x13u, x14u, x15u, x16u, x17u, x18u, ipku = self.Pronor(data)
            
            #menentukan data uji dan target output
            input_uji = datauji_normalisasi[self.n_datalatih:, 0:18]
            output_sebenarnya = datauji_normalisasi[self.n_datalatih:, 18]
            
            #menampilkan data uji pada tabel
            self.tbDataUji.setRowCount(n_datauji)

            for i in range(n_datauji):
                self.tbDataUji.setItem(i,0,QTableWidgetItem(str(int(data_uji[i,0])))) #membaca parameter NIM
                for j in range(18):
                    k = j + 1
                    self.tbDataUji.setItem(i,k,QTableWidgetItem(str(input_uji[i,j]))) #membaca paramater input latih x1-x18
                self.tbDataUji.setItem(i,19,QTableWidgetItem(str(output_sebenarnya[i]))) #membaca parameter target(IPK)

            #menampilkan total data latih dan total data uji
            self.eTotalDUji.setText(str(n_datauji))

            #menyimpan data latih dan data uji ke dalam variabel global
            self.data = data
            self.data_uji = data_uji
            self.input_uji = input_uji
            self.n_datauji = n_datauji
            self.output_sebenarnya = output_sebenarnya

        except:
            print('Terjadi kesalahan pada proses pembacaan data',sys.exc_info())

#menjalankan program
if __name__=="__main__":
    app = QApplication(sys.argv)
    w = FormPrediksiJST()
    w.show()
    sys.exit(app.exec_())