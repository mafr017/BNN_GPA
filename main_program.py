import sys
import time
import numpy as np
import pandas as pd

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import *
from PyQt5 import *
from JST import *

from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar2QT)
from matplotlib.backends.backend_qt5agg import FigureCanvas

import gui.gui_about as gui_about
import gui.gui_kelola as gui_kelola 
import gui.gui_login as gui_login
import gui.gui_lupa as gui_lupa
import gui.gui_main as gui_main
import gui.gui_pelatihan as gui_pelatihan
import gui.gui_petunjuk as gui_petunjuk
import gui.gui_prediksi as gui_prediksi
import gui.gui_register as gui_register

class FormMain(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.sgui = gui_main.Ui_MainWindow()
        self.sgui.setupUi(self)

        self.sgui.pbAboutMe.clicked.connect(self.tampilAbout)
        self.sgui.pbPetunjuk.clicked.connect(self.tampilPetunjuk)
        self.sgui.pbLogin.clicked.connect(self.tampilLogin)
        self.sgui.pbMulaiPre.clicked.connect(self.tampilPrediksi)
        self.sgui.pbRegister.clicked.connect(self.tampilRegister)
        self.show()
   
    def tampilAbout(self):
        self.tampilForm = FormAbout()

    def tampilPetunjuk(self):
        petunjuk = 1
        self.tampilForm = FormPetunjuk(petunjuk)

    def tampilLogin(self):
        self.tampilForm = FormLogin()
        self.close()

    def tampilPrediksi(self):
        self.tampilForm = FormPrediksi()
        self.close()

    def tampilRegister(self):
        self.tampilForm = FormRegister()
        self.close()

class FormLogin(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.sgui = gui_login.Ui_MainWindow()
        self.sgui.setupUi(self)

        self.sgui.pbLogin.clicked.connect(self.Login)
        self.sgui.pbLupa.clicked.connect(self.tampilLupa)
        self.sgui.pbRegister.clicked.connect(self.tampilRegister)
        self.sgui.pbKembali.clicked.connect(self.Kembali)
        self.show()
    
    def Login(self):
        msg = QMessageBox()
        msg.setWindowTitle("Login Berhasil!")
        msg.setText("Login Berhasil!")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
        self.tampilForm = FormPelatihanJST()
        self.close()

    def tampilRegister(self):
        self.tampilForm = FormRegister()
        self.close()
    
    def tampilLupa(self):
        self.tampilForm = FormLupa()
        self.close()
    
    def Kembali(self):
        self.tampilForm = FormMain()
        self.close()

class FormLupa(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.sgui = gui_lupa.Ui_MainWindow()
        self.sgui.setupUi(self)

        self.sgui.pbKirim.clicked.connect(self.Kirim)
        self.sgui.pbKembali.clicked.connect(self.Kembali)
        self.show()
    
    def Kirim(self):
        msg = QMessageBox()
        msg.setWindowTitle("Mengirim Bantuan Berhasil!")
        msg.setText("Bantuan berhasil dikirim ke e-mail anda!")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def Kembali(self):
        self.tampilForm = FormLogin()
        self.close()

class FormRegister(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.sgui = gui_register.Ui_MainWindow()
        self.sgui.setupUi(self)

        self.sgui.pbRegister.clicked.connect(self.Registerr)
        self.sgui.pbKembali.clicked.connect(self.Kembali)
        self.show()

    def Registerr(self):
        msg = QMessageBox()
        msg.setWindowTitle("Regristrasi Berhasil!")
        msg.setText("Proses Regristrasi Berhasil, silahkan login!")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()
        self.tampilForm = FormLogin()
        self.close()

    def Kembali(self):
        self.tampilForm = FormMain()
        self.close()
        
class FormAbout(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.sgui = gui_about.Ui_MainWindow()
        self.sgui.setupUi(self)

        self.sgui.pbOk.clicked.connect(self.keluar)
        self.show()
    
    def keluar(self):
        self.close()

class FormPetunjuk(QMainWindow):

    def __init__(self, petunjuk):
        QMainWindow.__init__(self)
        self.sgui = gui_petunjuk.Ui_MainWindow()
        self.sgui.setupUi(self)

        if petunjuk == 1:
            self.sgui.Judul.setText("Petunjuk Penggunaan Prediksi")

        self.sgui.pbOk.clicked.connect(self.keluar)
        self.show()
    
    def keluar(self):
        self.close()

class FormPelatihanJST(QMainWindow):

    # deklarasi variabel global
    n_datalatih = 0
    n_datauji = 0
    staBaPel = 0
    staBaBot = 0
    staPel = 0
    staBaUji = 0
    staUji = 0
    mse = []
    jml_iterasi = 0

    # menciptakan objek dari kelas JST
    jst = JaringanSyarafTiruan()
    pre = DPreparation()
    tra = DTransformation()

    # pendefinisian init self
    def __init__(self):
        QMainWindow.__init__(self)
        self.sgui = gui_pelatihan.Ui_MainMenu()
        self.sgui.setupUi(self)
        #loadUi ("D:\Learn programs\python\TA\gui\gui_jst_fix_no_bug.ui", self) # memanggil file gui_jst.ui
        self.setWindowTitle("Prediksi IPK Mahasiswa Sistem Komputer S1 - JST BACKPROPAGATION")

        #setup status bar
        self.sgui.statusbarr = QStatusBar()
        self.setStatusBar(self.sgui.statusbarr)
        self.sgui.statusbarr.setStyleSheet('background-color: #FFFFFF;')

        self.sgui.progressBar_2 = QProgressBar()
        self.sgui.progressBar_2.setValue(0)
        self.sgui.progressBar_2.setFixedSize(150, 21)

        self.sgui.lstatus = QLabel()
        self.sgui.lstatus.setText("Progres Pelatihan")
        
        self.sgui.statusbarr.addWidget(self.sgui.lstatus)
        self.sgui.statusbarr.addWidget(self.sgui.progressBar_2)

        # memanggil fungsi-fungsi
        self.sgui.pbBaca.clicked.connect(self.BacaData)
        self.sgui.pbBaca_2.clicked.connect(self.BacaData_2)
        self.sgui.pbBobot.clicked.connect(self.BacaBobot)
        self.sgui.pbPelatihan.clicked.connect(self.ProPelatihan)
        self.sgui.pbDetailG.clicked.connect(self.DetailGrafik)
        self.sgui.pbPengujian.clicked.connect(self.ProPengujian)
        self.sgui.pbDetailG_2.clicked.connect(self.DetailGrafik_2)
        self.sgui.pbKelola.clicked.connect(self.tampilKelola)
        #self.sgui.pbCetak.clicked.connect(self.Cetak)
        self.sgui.pbTambah.clicked.connect(self.TambahAdmin)
        self.sgui.pbLogout.clicked.connect(self.LogOut)
        self.show()
    
    # pendefinisian proses mulai normalisasi
    def Pronor(self, data):
        # mengakses data berdasarkan kolom/parameter
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

        # normalisasi data menggunakan fungsi Normalisasi kelas JST
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

        # menggabungkan data-data normalisasi menjadi dataset
        data_normalisasi = np.concatenate((x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, ipk), axis=1)
                
        return data_normalisasi, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, ipk

    # mendefinisikan fungsi untuk melakukan pembacaan data latih
    def BacaData(self):
        try:
            # membaca file CSV data input dari penyimpanan lokal
            path = QFileDialog.getOpenFileName(self, 'Silahkan pilih file data pelatihan', '', "XLSX files (*.xlsx)")
            namafile = path[0]
            np.set_printoptions(suppress=True, linewidth=np.inf)
            data_latih = pd.read_excel(namafile, header=1)
            data_latih = np.array(data_latih) # simpan data kedalam bentuk list/array

            # menentukan jumlah data latih
            total_data  = len(data_latih)
            n_datalatih = total_data

            # menjalankan fungsi normalisasi data
            data = data_latih
            data_normalisasi, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, ipk = self.Pronor(data)
            
            # menentukan data latih dan target output
            input_latih = data_normalisasi[:, 0:18]
            target_output = data_normalisasi[:, 18]
            
            # menampilkan data latih pada tabel
            self.sgui.tbDataLat.setRowCount(n_datalatih)
            for i in range(n_datalatih):
                self.sgui.tbDataLat.setItem(i,0,QTableWidgetItem(str(int(data[i,0])))) # membaca parameter NIM
                for j in range(18):
                    k = j + 1
                    self.sgui.tbDataLat.setItem(i,k,QTableWidgetItem(str(input_latih[i,j]))) # membaca paramater input latih x1-x18
                self.sgui.tbDataLat.setItem(i,19,QTableWidgetItem(str(target_output[i]))) # membaca parameter target(IPK)

            # menampilkan total data latih
            self.sgui.eTotalDLatih.setText(str(n_datalatih))

            # menyimpan data latih ke dalam variabel global
            self.n_datalatih = n_datalatih
            self.data_latih = data_latih
            self.input_latih = input_latih
            self.target_output = target_output
            self.staBaPel = 1

        except:
            print('Terjadi kesalahan pada proses pembacaan data {}'.format(sys.exc_info()[-1].tb_lineno))

    # mendefinisikan fungsi untuk melakukan pembacaan data uji
    def BacaData_2(self):
        try:
            # mengambil variabel global
            staBaPel = self.staBaPel

            if staBaPel == 1:
                # membaca file CSV data input dari penyimpanan lokal
                path = QFileDialog.getOpenFileName(self, 'Silahkan pilih file data pelatihan', '', "XLSX files (*.xlsx)")
                namafile = path[0]
                np.set_printoptions(suppress=True, linewidth=np.inf)
                data_uji = pd.read_excel(namafile, header=1)
                data_uji = np.array(data_uji) # simpan data kedalam bentuk list/array

                data = np.concatenate((self.data_latih, data_uji)) # menggabungkan data latih dengan data uji

                # menentukan jumlah data uji
                total_data  = len(data_uji)
                n_datauji = total_data

                # menjalankan fungsi normalisasi data
                datauji_normalisasi, x1u, x2u, x3u, x4u, x5u, x6u, x7u, x8u, x9u, x10u, x11u, x12u, x13u, x14u, x15u, x16u, x17u, x18u, ipku = self.Pronor(data)
                
                # menentukan data uji dan target output
                input_uji = datauji_normalisasi[self.n_datalatih:, 0:18]
                output_sebenarnya = datauji_normalisasi[self.n_datalatih:, 18]
                
                # menampilkan data uji pada tabel
                self.sgui.tbDataUji.setRowCount(n_datauji)

                for i in range(n_datauji):
                    self.sgui.tbDataUji.setItem(i,0,QTableWidgetItem(str(int(data_uji[i,0])))) # membaca parameter NIM
                    for j in range(18):
                        k = j + 1
                        self.sgui.tbDataUji.setItem(i,k,QTableWidgetItem(str(input_uji[i,j]))) # membaca paramater input latih x1-x18
                    self.sgui.tbDataUji.setItem(i,19,QTableWidgetItem(str(output_sebenarnya[i]))) # membaca parameter target(IPK)

                # menampilkan total data latih dan total data uji
                self.sgui.eTotalDUji.setText(str(n_datauji))

                # menyimpan data latih dan data uji ke dalam variabel global
                self.data = data
                self.data_uji = data_uji
                self.input_uji = input_uji
                self.n_datauji = n_datauji
                self.output_sebenarnya = output_sebenarnya
                self.staBaUji = 1

            else:
                # menampilkan pesan error
                msg = QMessageBox()
                msg.setWindowTitle("Proses Dibatalkan !")
                msg.setText("Lakukan Proses Baca Data Pelatihan Terlebih Dahulu!")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()

        except:
            print('Terjadi kesalahan pada proses pembacaan data',sys.exc_info())

    # mendifinisikan fungsi untuk menampilkan bobot awal
    def BacaBobot(self):
        try:
            # mengambil variabel global
            n_input = int(self.sgui.eNInp.displayText())
            n_hidden = int(self.sgui.eNHid.displayText())
            n_output = int(self.sgui.eNOut.displayText())

            # inisialisasi awal bobot V dan bobot W
            """ v = np.array([
                        [0.1, 0.2, 0.3, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3],
                        [0.1, 0.2, 0.3, 0.4, -0.3, -0.2, -0.1, 0.2, 0.3, 0.4, -0.3, -0.2, -0.1, 0.2, 0.3],
                        [-0.2, -0.1, -0.4, -0.3, -0.4, -0.1, -0.2, -0.1, -0.4, -0.3, 0.4, 0.1, 0.2, 0.1, 0.4],
                        [-0.3, -0.2, -0.3, -0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2, -0.3, -0.2, -0.3, -0.2, -0.3],
                        [0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.4, -0.3, -0.2, -0.1, 0.2, 0.3, 0.4, -0.3,  -0.2],
                        [0.3, 0.4, 0.1, 0.2, 0.1, 0.4, 0.3, 0.4, 0.1, 0.2, 0.1, 0.4, 0.3, 0.4, 0.1],
                        [0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2],
                        [-0.1, -0.2, -0.3, -0.4, -0.3, -0.2, -0.1, -0.2, -0.3, -0.4, -0.3, -0.2, -0.1, -0.2, -0.3],
                        [-0.2, -0.1, -0.4, -0.3, -0.4, -0.1, -0.2, -0.1, -0.4, -0.3, -0.4, -0.1, -0.2, -0.1, -0.4],
                        [0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3],
                        [-0.4, -0.3, -0.2, -0.1, -0.2, -0.3, -0.4, -0.3, -0.2, -0.1, -0.2, -0.3, -0.4, -0.3, -0.2],
                        [-0.3, -0.4, -0.1, -0.2, -0.1, -0.4, -0.3, -0.4, -0.1, -0.2, -0.1, -0.4, -0.3, -0.4, -0.1],
                        [0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2],
                        [0.1, 0.2, 0.3, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3],
                        [0.2, 0.1, 0.4, 0.3, 0.4, 0.1, 0.2, 0.1, 0.4, 0.3, 0.4, 0.1, 0.2, 0.1, 0.4],
                        [0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3],
                        [0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.4, 0.3, 0.2, 0.1, 0.2, 0.3, 0.4, 0.3, 0.2],
                        [-0.3, -0.4, -0.1, -0.2, -0.1, -0.4, -0.3, -0.4, -0.1, -0.2, -0.1, -0.4, -0.3, -0.4, -0.1],
                        [0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2, 0.3, 0.2]])
                
                w = np.array([[0.3], [0.2], [-0.3], [-0.4], [0.3], [0.2], [0.1], [-0.2], [0.3], [0.4], [-0.3], [-0.2], [0.1], [0.2], [0.3], [-0.4]]) """
            
            [v, w] = self.pre.Acakbobot(n_input, n_hidden, n_output)

            # menentukan jumlah bobot
            n_bobotv = len(v)
            n_bobotw = len(w)

            # menampilkan bobot v pada tabel
            baris, kolom = v.shape
            self.sgui.tbBobotV.setColumnCount(kolom)
            self.sgui.tbBobotV.setRowCount(baris)
            for i in range(baris):
                for j in range(kolom):
                    self.sgui.tbBobotV.setItem(i,j,QTableWidgetItem(str(round(v[i,j], 4))))

            # menampilkan bobot w pada tabel
            baris, kolom = w.shape
            self.sgui.tbBobotW.setColumnCount(kolom)
            self.sgui.tbBobotW.setRowCount(baris)
            for i in range(baris):
                for j in range(kolom):
                    self.sgui.tbBobotW.setItem(i,j,QTableWidgetItem(str(round(w[i,j], 4))))

            # menyimpan data bobot ke dalam variabel global
            self.n_bobotv = n_bobotv
            self.n_bobotw = n_bobotw
            self.v = v
            self.w = w
            self.staBaBot = 1

        except:
            print('Terjadi kesalahan pada proses pembacaan bobot {}'.format(sys.exc_info()[-1].tb_lineno))
    
    # mendifinisikan fungsi untuk melakukan proses pelatihan
    def ProPelatihan(self):
        try:
            # mengambil variabel global
            staBaPel = self.staBaPel
            staBaBot = self.staBaBot

            if staBaPel == 1 and staBaBot == 1:
                time_start = time.perf_counter() # memulai waktu proses

                msg = QMessageBox()
                msg.setStyleSheet("QLabel{min-width: 370px;}");
                msg.setWindowTitle("Proses Pelatihan Sedang Berjalan, Mohon Tunggu Beberapa Menit!")
                msg.show()

                # mengambil data variabel global
                n_input = int(self.sgui.eNInp.displayText())
                n_hidden = int(self.sgui.eNHid.displayText())
                n_output = int(self.sgui.eNOut.displayText())
                alpha = float(self.sgui.eAlpha.displayText())
                min_error = float(self.sgui.eMinE.displayText())
                iterasi = int(self.sgui.eIte.displayText())

                input_latih = self.input_latih
                target_output = self.target_output
                n_datalatih = self.n_datalatih

                v = self.v
                w = self.w

                # memetakan data error dan mse
                error = np.zeros((n_datalatih,1))
                mse = np.zeros((iterasi,1))
                
                jml_iterasi = 0
                coomplete = 0
                self.sgui.progressBar_2.setValue(coomplete)

                # proses pelatihan feedforward dan backpropagation
                for i in range (iterasi):
                    for j in range(n_datalatih):
                        [z, y] = self.jst.Feedforward(input_latih[j,:], v, w, n_hidden, n_output)
                        [w, v] = self.jst.Backpropagation(target_output[j], y, input_latih[j,:], alpha, z, w, v)
                        
                        error[j,0] = (target_output[j]-y[0,0])**2

                    mse[i,0] = round(sum(error[:, 0])/n_datalatih, 7)

                    if mse[i,0] <= min_error:
                        jml_iterasi = i+1
                        break
                    
                    jml_iterasi = i+1
                    
                    coomplete = ((jml_iterasi)/iterasi)*100
                    if coomplete >= 100:
                        coomplete = 100
                    self.sgui.progressBar_2.setValue(coomplete)
                    print ('Iterasi ke-', (i+1))
                    print (f"MSE : {mse[i,0]:0.7f}")

                # menampilkan hasil bobot v dan w ke dalam tabel
                baris, kolom = v.shape
                self.sgui.tbBobotV.setColumnCount(kolom)
                self.sgui.tbBobotV.setRowCount(baris)
                for i in range(baris):
                    for j in range(kolom):
                        self.sgui.tbBobotV.setItem(i,j,QTableWidgetItem(str(round(v[i, j], 3))))

                baris, kolom = w.shape
                self.sgui.tbBobotW.setColumnCount(kolom)
                self.sgui.tbBobotW.setRowCount(baris)
                for i in range(baris):
                    for j in range(kolom):
                        self.sgui.tbBobotW.setItem(i,j,QTableWidgetItem(str(round(w[i, j], 3))))

                """ gunakan gui_jst.ui untuk menggunakan fitur ini tetapi memiliki bug (grafik hanya bisa digunakan satu kali proses)
                    # menampilkan grafik konvergensi proses pelatihan
                    fig = plt.Figure(figsize=(10, 10))
                    ax = fig.add_subplot(1,1,1)
                    ax.plot(mse)
                    ax.set_ylim(ymin=0)
                    ax.set_ylabel('MSE')
                    fig.subplots_adjust(left=0.18, bottom=0.2, right=0.98, top=0.9)
                    fig.canvas.draw()
                    fig.canvas.flush_events()

                    plotWidget = FigureCanvas(fig)
                    lay = QtWidgets.QVBoxLayout(self.gGrafik)
                    lay.addWidget(plotWidget)"""

                # menampilkan waktu pelatihan dan nilai MSE
                time_stop = round((time.perf_counter() - time_start),2)
                self.sgui.eWaktu.setText(str(time_stop))
                self.sgui.eMSE.setText(str(mse[jml_iterasi-1, 0]))
                
                # menyimpan data hasil bobot pelatihan ke dalam variabel global
                self.v = v
                self.w = w
                self.mse = mse
                self.jml_iterasi = jml_iterasi
                self.staPel = 1
                
            else:
                # menampilkan pesan error
                msg = QMessageBox()
                msg.setWindowTitle("Proses Dibatalkan !")
                if staBaPel == 1:
                    msg.setText("Lakukan Proses Baca Bobot Awal Terlebih Dahulu!")
                else:
                    msg.setText("Lakukan Proses Baca Data Pelatihan Terlebih Dahulu!")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()

        except:
            print('Terjadi Kesalahan Pada Proses Pelatihan {}'.format(sys.exc_info()[-1].tb_lineno))
    
    # mendifinisikan fungsi detail grafik pelatihan
    def DetailGrafik(self):
        try:
            # mengambil variabel global
            staPel = self.staPel

            if staPel == 0:
                # menampilkan pesan error
                msg = QMessageBox()
                msg.setWindowTitle("Proses Dibatalkan !")
                msg.setText("Lakukan Proses Pelatihan Terlebih Dahulu!")
                msg.setIcon(QMessageBox.Warning)

                x = msg.exec_()
            else:
                # menampilkan detail grafik
                mse = self.mse
                jml_iterasi = self.jml_iterasi

                plt.figure()
                plt.plot(mse[0:jml_iterasi, 0])
                plt.ylim(ymin=0)
                plt.xlabel('Iterasi ke-i, (0 < i < '+str(jml_iterasi)+')')
                plt.ylabel('MSE')
                plt.title('Grafik Konvergensi Proses Pelatihan')
                plt.show()
        except:
            print('Terjadi Kesalahan {}'.format(sys.exc_info()[-1].tb_lineno))

    # mendifinisikan fungsi untuk melakukan proses pengujian
    def ProPengujian(self):
        try:
            # mengambil variabel global
            staBaUji = self.staBaUji
            staPel = self.staPel

            if staBaUji == 1 and staPel == 1:
                time_start = time.perf_counter() # memulai waktu proses

                # mengambil data variabel global
                n_hidden = int(self.sgui.eNHid.displayText())
                n_output = int(self.sgui.eNOut.displayText())

                data = self.data
                data_uji = self.data_uji
                input_uji = self.input_uji
                output_sebenarnya = self.output_sebenarnya
                n_datauji = self.n_datauji

                v = self.v
                w = self.w
                
                # melakukan denormalisasi hasil prediksi dan data sebenarnya
                ipkuji = data[:, 19]
                datamax = max(ipkuji)
                datamin = min(ipkuji)

                # memetakan array/matriks/list
                hasil_prediksi = np.zeros((n_datauji, 1))
                error = np.zeros((n_datauji, 1))
                mse = np.zeros((n_datauji, 1))
                kum_error = np.zeros((n_datauji, 1))
                hslprediksi_denormalisasi = np.zeros((n_datauji,1))
                outsebenarnya_denormalisasi = np.zeros((n_datauji,1))

                # melakukan proses feedforward atau prediksi
                for j in range(n_datauji):
                    [z, y] = self.jst.Feedforward(input_uji[j,:], v, w, n_hidden, n_output)
                    hasil_prediksi[j,0] = y[0,0]
                    error[j,0] = (output_sebenarnya[j]-y[0,0])**2
                
                mse = round(sum(error[:, 0])/n_datauji, 7)

                # proses denormalisasi
                for i in range(n_datauji):
                    hslprediksi_denormalisasi[i,0] = self.tra.Denormalisasi(hasil_prediksi[i,0], datamin, datamax)
                    outsebenarnya_denormalisasi[i,0] = self.tra.Denormalisasi(output_sebenarnya[i], datamin, datamax)

                # menampilkan hasil bobot v dan w ke dalam tabel
                self.sgui.tbHasilUji.setRowCount(n_datauji)
                for i in range(n_datauji):
                    hasiljst = hslprediksi_denormalisasi[i,0]
                    datasebenarnya = outsebenarnya_denormalisasi[i,0]
                    errorhasil = abs(datasebenarnya-hasiljst)
                    errorhasil = round(errorhasil, 6)
                    kum_error[i,0] = abs((datasebenarnya-hasiljst)/datasebenarnya)
                    akurasi = 100 - (kum_error[i,0] * 100)
                    akurasi = float(akurasi)

                    # menampilkan hasil ke dalam tabel
                    self.sgui.tbHasilUji.setItem(i,0,QTableWidgetItem(str(int(data_uji[i,0]))))
                    self.sgui.tbHasilUji.setItem(i,1,QTableWidgetItem(str(round(hasiljst, 2))))
                    self.sgui.tbHasilUji.setItem(i,2,QTableWidgetItem(str(round(datasebenarnya, 2))))
                    self.sgui.tbHasilUji.setItem(i,3,QTableWidgetItem(str(errorhasil)))
                    self.sgui.tbHasilUji.setItem(i,4,QTableWidgetItem(f"{akurasi:0.2f}"))

                rata2akurasi = 100 - ((sum(kum_error)/n_datauji) * 100) # menghitung MAPE / akurasi
                rata2akurasi = float(rata2akurasi[0])

                # menampilkan grafik konvergensi proses pengujian
                y1 = hslprediksi_denormalisasi
                y2 = outsebenarnya_denormalisasi
                x_tmp = list(range(1, n_datauji+1))
                x1 = np.array([x_tmp]).transpose()
                
                """ gunakan gui_jst.ui untuk menggunakan fitur ini tetapi memiliki bug (grafik hanya bisa digunakan satu kali proses)
                    fig = plt.Figure(figsize=(5, 5))
                    ax = fig.add_subplot(1,1,1)
                    ax.plot(x1, y1, 'r', x1, y2, 'g')
                    ax.set_xlabel('Data Uji Ke-i, (0 < i < '+str(n_datauji)+')')
                    ax.set_ylabel('Hasil Prediksi')
                    ax.legend(('Hasil Prediksi JST', 'Data Sebenarnya'), loc='upper right')
                    fig.subplots_adjust(left=0.15, bottom=0.3, right=0.98, top=0.9)
                    fig.canvas.draw()
                    fig.canvas.flush_events()

                    plotWidget = FigureCanvas(fig)
                    lay = QtWidgets.QVBoxLayout(self.gGrafik_2)
                    lay.setContentsMargins(0, 0, 0, 0)
                    lay.addWidget(plotWidget) """

                # menampilkan waktu pelatihan dan nilai MSE
                time_stop = (time.perf_counter() - time_start)
                self.sgui.eWaktu_2.setText(str(round(time_stop, 2)))
                self.sgui.eMSE_2.setText(str(mse))
                self.sgui.eAkurasi.setText(f"{rata2akurasi:0.2f}")
                
                # menyimpan data hasil bobot pelatihan ke dalam variabel global
                self.mseUji = mse
                self.hslprediksi_denormalisasi = hslprediksi_denormalisasi
                self.outsebenarnya_denormalisasi = outsebenarnya_denormalisasi
                self.errorhasil = errorhasil
                self.akurasi = akurasi
                self.rata2akurasi = rata2akurasi
                
                self.x1 = x1
                self.y1 = y1
                self.y2 = y2
                
                self.staUji = 1

            else:
                # menampilkan pesan error
                msg = QMessageBox()
                msg.setWindowTitle("Proses Dibatalkan !")
                if staPel == 1:
                    msg.setText("Lakukan Proses Baca Bobot Awal Terlebih Dahulu!")
                else:
                    msg.setText("Lakukan Proses Baca Data Pengujian Terlebih Dahulu!")
                msg.setIcon(QMessageBox.Warning)
                x = msg.exec_()

        except IndexError:
            print('Terjadi Kesalahan Pada Proses Pelatihan {}'.format(sys.exc_info()[-1].tb_lineno))
    
    # mendifinisikan fungsi detail grafik pengujian
    def DetailGrafik_2(self):
        try:
            # mengambil variabel global
            staUji = self.staUji

            if staUji == 0:
                # menampilkan pesan error
                msg = QMessageBox()
                msg.setWindowTitle("Proses Dibatalkan !")
                msg.setText("Lakukan Proses Pengujian Terlebih Dahulu!")
                msg.setIcon(QMessageBox.Warning)

                x = msg.exec_()
            else:
                # menampilkan detail grafik
                n_datauji = self.n_datauji
                x1 = self.x1
                y1 = self.y1
                y2 = self.y2
                
                plt.figure()
                plt.plot(x1, y1, 'r', x1, y2, 'g')
                plt.ylim(ymin=0)
                plt.xlabel('Data Uji Ke-i, (0 < i < '+str(n_datauji)+')')
                plt.ylabel('Hasil Prediksi')
                plt.title('Grafik Perbandingan Hasil Prediksi JST dan Data Sebenarnya')
                plt.legend(('Hasil Prediksi JST', 'Data Sebenarnya'), loc='lower right')
                plt.show()
        except:
            print('Terjadi Kesalahan',sys.exc_info())

    def tampilKelola(self):
        self.tampilForm = FormKelola()
        self.close()
    
    def TambahAdmin(self):
        uniqeKey = "asdjlk%*&saedlkjwqe"
        msg = QMessageBox()
        mafont = QtGui.QFont()
        mafont.setBold(True)
        msg.setWindowTitle("Berhasil Menambah Admin!")
        msg.setText(f"<html><head/><body><p>Berhasil meng-generate Uniqe Key</p><p>Silahkan catat atau copy kode berikut: <span style=\" font-size:8pt; font-weight:600;\">{uniqeKey}</span></p></body></html>")
        msg.setDetailedText(f"{uniqeKey}")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def LogOut(self):
        self.tampilForm = FormMain()
        self.close()

class FormKelola(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.sgui = gui_kelola.Ui_MainWindow()
        self.sgui.setupUi(self)

        self.sgui.pbKembali.clicked.connect(self.Kembali)
        self.show()
    
    def Kembali(self):
        self.tampilForm = FormPelatihanJST()
        self.close()

class FormPrediksi(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.sgui = gui_prediksi.Ui_MainWindow()
        self.sgui.setupUi(self)

        self.sgui.pbKembali.clicked.connect(self.Kembali)
        self.show()
    
    def Kembali(self):
        self.tampilForm = FormMain()
        self.close()

# menjalankan program
if __name__=="__main__":
    app = QApplication(sys.argv)
    w = FormMain()
    #w = FormPelatihanJST()
    sys.exit(app.exec_())