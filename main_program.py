import sys
import time
import numpy as np
import pandas as pd
import random
import string
import mysql.connector as mycon

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import *
from PyQt5 import *
from JST import *

from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar2QT)
from matplotlib.backends.backend_qt5agg import FigureCanvas

from mysql.connector import *

import gui.gui_about as gui_about
import gui.gui_kelola as gui_kelola 
import gui.gui_login as gui_login
import gui.gui_lupa as gui_lupa
import gui.gui_main as gui_main
import gui.gui_pelatihan as gui_pelatihan
import gui.gui_petunjuk as gui_petunjuk
import gui.gui_prediksi as gui_prediksi
import gui.gui_register as gui_register

class kontrolDB:
    def __init__(self):
        self.konek()

    def konek(self):
        try:
            madb = mycon.connect(host="localhost", user="root", password="", database="gpa_bnn")
            self.madb = madb
            if madb.is_connected():
                db_info = madb.get_server_info()
                self.statSer = f"Connected to Server MySQL v.{db_info}"
        except Error as error:
            self.statSer = f"Failed Connect to Server MySQL error({error})"

class FormMain(QMainWindow):
    
    def __init__(self):
        QMainWindow.__init__(self)

        #membuat window form
        self.sgui = gui_main.Ui_MainWindow()
        self.sgui.setupUi(self)

        kontrolDB.konek(self) #panggil fungsi koneksi server

        #setup status bar
        self.sgui.statusbarr = QStatusBar()
        self.setStatusBar(self.sgui.statusbarr)
        self.sgui.statusbarr.setStyleSheet('background-color: #FFFFFF;')

        self.sgui.lstatus = QLabel()
        self.sgui.lstatus.setText(self.statSer)
        
        self.sgui.statusbarr.addWidget(self.sgui.lstatus)

        #mendefinisikan fungsi pada
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
        
        kontrolDB.konek(self)

        self.sgui.pbLogin.clicked.connect(self.Login)
        self.sgui.pbLupa.clicked.connect(self.tampilLupa)
        self.sgui.pbRegister.clicked.connect(self.tampilRegister)
        self.sgui.pbPetunjuk.clicked.connect(self.tampilPetunjuk)
        self.sgui.pbKembali.clicked.connect(self.Kembali)
        self.show()
    
    def Login(self):
        idAdmin = str(self.sgui.leId.displayText())
        passAdmin = str(self.sgui.lePass.text())
        cur = self.madb.cursor()
        cur.execute("SELECT id, password, nama FROM tb_admin WHERE id = %s AND password = %s",(idAdmin, passAdmin,))
        idd = cur.fetchall()
        idds = len(idd)
        cur.close()
        if idds > 0:
            print("berhasil login")
            for row in idd:
                namaAdmin = row[2]
            msg = QMessageBox()
            msg.setWindowTitle("Login Berhasil!")
            msg.setText("Login Berhasil!")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
            self.tampilForm = FormPelatihanJST(namaAdmin)
            self.close()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Login Gagal!")
            msg.setText("Id atau Password Salah!")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
            self.sgui.leId.setText("")
            self.sgui.lePass.setText("")
            print("gagal login")

    def tampilRegister(self):
        self.tampilForm = FormRegister()
        self.close()
    
    def tampilLupa(self):
        self.tampilForm = FormLupa()
        self.close()
    
    def tampilPetunjuk(self):
        petunjuk = 2
        self.tampilForm = FormPetunjuk(petunjuk)

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

        kontrolDB.konek(self)

        self.sgui.pbRegister.clicked.connect(self.Registerr)
        self.sgui.pbKembali.clicked.connect(self.Kembali)
        self.show()

    def Registerr(self):
        statada = ""
        stattoken = ""
        cur = self.madb.cursor()

        leuniqe = str(self.sgui.leNama_2.displayText())
        lenama = str(self.sgui.leNama.displayText())
        leemail = str(self.sgui.leEmail.displayText())
        leid = str(self.sgui.leId.displayText())
        lepass = str(self.sgui.lePass.text())

        cuniqe = cur.execute("SELECT uniqe_key FROM tb_admin WHERE uniqe_key = %s",(leuniqe,))
        ccuniqe = cur.fetchall()
        ccuniqe = len(ccuniqe)
        
        cuniqe2 = cur.execute("SELECT uniqe_key FROM tb_uniqekey WHERE uniqe_key = %s",(leuniqe,))
        ccuniqe2 = cur.fetchall()
        ccuniqe2 = len(ccuniqe2)
        if ccuniqe > 0:
            print("Uniqe Key sudah dipakai")
            statada += "Uniqe Key, " 
            stata = 1
        elif ccuniqe2 < 1:
            print("Token Uniqe Key Tidak Ada")
            stattoken += "Token Uniqe Key Tidak Ada!" 
            stata = 2
        else:
            stata = 0

        cnama = cur.execute("SELECT nama FROM tb_admin WHERE nama = %s",(lenama,))
        ccnama = cur.fetchall()
        ccnama = len(ccnama)
        if ccnama > 0:
            print("Nama sudah dipakai")
            statada += "Nama, " 
            statb = 1
        else:
            statb = 0

        cemail = cur.execute("SELECT email FROM tb_admin WHERE email = %s",(leemail,))
        ccemail = cur.fetchall()
        ccemail = len(ccemail)
        if ccemail > 0:
            print("Email sudah dipakai")
            statada += "E-mail, " 
            statc = 1
        else:
            statc = 0

        cid = cur.execute("SELECT id FROM tb_admin WHERE id = %s",(leid,))
        ccid = cur.fetchall()
        ccid = len(ccid)
        if ccid > 0:
            print("Id sudah dipakai")
            statada += "Id, " 
            statd = 1
        else:
            statd = 0

        if stata == 1 or statb == 1 or statc == 1 or statd == 1 or stata == 2:
            print()
            print("Registrasi Gagal!")
            msg = QMessageBox()
            msg.setWindowTitle("Registrasi Gagal!")
            if stata == 2 and (statb == 0 and statc == 0 and statd == 0):
                msg.setText(f"{stattoken}")
            elif stata == 2 and (statb == 1 or statc == 1 or statd == 1):
                msg.setText(f"{statada}Sudah Dipakai! & {stattoken}")
            else:
                msg.setText(f"{statada}Sudah Dipakai!")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
            self.sgui.leNama_2.setText("")
            self.sgui.leNama.setText("")
            self.sgui.leEmail.setText("")
            self.sgui.leId.setText("")
            self.sgui.lePass.setText("")
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Registrasi Berhasil!")
            msg.setText("Proses Regitrasi Berhasil, Silahkan Login!")
            msg.setIcon(QMessageBox.Information)
            msg.exec_()
            cur.execute("UPDATE tb_uniqekey SET id = %s WHERE uniqe_key = %s",(leid, leuniqe,))
            self.madb.commit()
            cur.execute("INSERT INTO tb_admin (uniqe_key, id, nama, email, password) VALUES (%s, %s, %s, %s, %s)",(leuniqe, leid, lenama, leemail, lepass,))
            self.madb.commit()
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

class FormPetunjuk(FormMain, QMainWindow):

    def __init__(self, petunjuk):
        QMainWindow.__init__(self)
        self.sgui = gui_petunjuk.Ui_MainWindow()
        self.sgui.setupUi(self)

        if petunjuk == 1:
            self.sgui.Judul.setText(f"Petunjuk Penggunaan Prediksi")
        elif petunjuk == 2:
            self.sgui.Judul.setText(f"Petunjuk Admin Penggunaan Pelatihan")
        else:
            print("Terjadi Kesalahan")

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
    def __init__(self, namaAdmin):
        QMainWindow.__init__(self)
        self.sgui = gui_pelatihan.Ui_MainMenu()
        self.sgui.setupUi(self)
        #loadUi ("D:\Learn programs\python\TA\gui\gui_jst_fix_no_bug.ui", self) # memanggil file gui_jst.ui
        self.setWindowTitle("Prediksi IPK Mahasiswa Sistem Komputer S1 - JST BACKPROPAGATION")
        
        kontrolDB.konek(self)

        #setup status bar
        self.sgui.statusbarr = QStatusBar()
        self.setStatusBar(self.sgui.statusbarr)
        self.sgui.statusbarr.setStyleSheet('background-color: #FFFFFF;')

        self.sgui.progressBar_2 = QProgressBar()
        self.sgui.progressBar_2.setValue(0)
        self.sgui.progressBar_2.setFixedSize(150, 21)

        self.sgui.lstatus = QLabel()
        self.sgui.lstatus.setText("Progres Pelatihan")

        self.sgui.lstatko = QLabel()
        self.sgui.lstatko.setText(self.statSer)
        
        self.sgui.statusbarr.addWidget(self.sgui.lstatus)
        self.sgui.statusbarr.addWidget(self.sgui.progressBar_2)
        self.sgui.statusbarr.addWidget(self.sgui.lstatko)
        self.sgui.lAdmin.setText(namaAdmin)
        self.adminnama= namaAdmin

        # memanggil fungsi-fungsi
        self.BacaData()
        self.BacaData_2()
        #self.sgui.pbBaca.clicked.connect(self.BacaData_2)
        self.sgui.pbBaca.setHidden(True)
        #self.sgui.pbBaca_2.clicked.connect(self.BacaData_2)
        self.sgui.pbBaca_2.setHidden(True)
        self.sgui.pbBobot.clicked.connect(self.BacaBobot)
        self.sgui.pbPelatihan.clicked.connect(self.ProPelatihan)
        self.sgui.pbDetailG.clicked.connect(self.DetailGrafik)
        self.sgui.pbPengujian.clicked.connect(self.ProPengujian)
        self.sgui.pbDetailG_2.clicked.connect(self.DetailGrafik_2)
        self.sgui.pbKelola.clicked.connect(self.tampilKelola)
        #self.sgui.pbCetak.clicked.connect(self.Cetak)
        self.sgui.pbTambah.clicked.connect(self.TambahAdmin)
        self.sgui.pbLogout.clicked.connect(self.LogOut)

        # menampilkan bias & bobot terakhir
        cur = self.madb.cursor()
        cur.execute("SELECT n1 FROM tb_bobotv")
        biasv = cur.fetchall()
        lbiasv = len(biasv)
        cur.execute("SELECT n1 FROM tb_bobotw")
        biasw = cur.fetchall()
        lbiasw = len(biasw)
        if lbiasv == 0 and lbiasw == 0 :
            biasv = ""
            print("Bobot Kosong")
        else:
            biasv = str(biasv[0][0])
            biasw = str(biasw[0][0])

            np.set_printoptions(suppress=True, linewidth=np.inf)
            cur.execute("SELECT * FROM tb_bobotv")
            aldatv = cur.fetchall()
            v = np.array(aldatv)
            cur.execute("SELECT * FROM tb_bobotw")
            aldatw = cur.fetchall()
            w = np.array(aldatw)

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
            self.v = v
            self.w = w
            self.staBaBot = 1

            cur.execute("SELECT * FROM tb_params")
            alda = cur.fetchall()
            qninput = alda[0][1]
            self.sgui.eNInp.setText(str(qninput))
            qnhidden = alda[0][2]
            self.sgui.eNHid.setText(str(qnhidden))
            qnoutput = alda[0][3]
            self.sgui.eNOut.setText(str(qnoutput))
            qalpha = alda[0][4]
            self.sgui.eAlpha.setText(str(qalpha))
            qminerr = alda[0][5]
            self.sgui.eMinE.setText(str(qminerr))
            qiterasi = alda[0][6]
            self.sgui.eIte.setText(str(qiterasi))
            cur.execute("SELECT mse FROM tb_mse")
            alda = cur.fetchall()
            itra = qiterasi - 1
            qmse = alda[itra][0]
            self.sgui.eMSE.setText(str(qmse))

            if biasv == 0.1 and biasw == 0.1 :
                self.sgui.BobotHasil.setTitle("Bias dan Bobot Awal")
            else:
                self.staPel = 1
                self.sgui.BobotHasil.setTitle("Bias dan Bobot Hasil")
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
            # membaca data pelatihan dari database
            np.set_printoptions(suppress=True, linewidth=np.inf)
            cur = self.madb.cursor()
            cur.execute("SELECT * FROM data_latih")
            alda = cur.fetchall()

            """ # membaca file CSV data input dari penyimpanan lokal
            path = QFileDialog.getOpenFileName(self, 'Silahkan pilih file data pelatihan', '', "XLSX files (*.xlsx)")
            namafile = path[0]
            np.set_printoptions(suppress=True, linewidth=np.inf)
            alda = pd.read_excel(namafile, header=1) """
            
            data_latih = np.array(alda) # simpan data kedalam bentuk list/array

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
            print(f'Terjadi kesalahan pada proses pembacaan data baris-{sys.exc_info()[-1].tb_lineno}:\n{sys.exc_info()}')

    # mendefinisikan fungsi untuk melakukan pembacaan data uji
    def BacaData_2(self):
        try:
            # mengambil variabel global
            staBaPel = self.staBaPel

            if staBaPel == 1:
                # membaca data pelatihan dari database
                np.set_printoptions(suppress=True, linewidth=np.inf)
                cur = self.madb.cursor()
                cur.execute("SELECT * FROM data_uji")
                alda = cur.fetchall()
                
                """ # membaca file CSV data input dari penyimpanan lokal
                path = QFileDialog.getOpenFileName(self, 'Silahkan pilih file data pelatihan', '', "XLSX files (*.xlsx)")
                namafile = path[0]
                np.set_printoptions(suppress=True, linewidth=np.inf)
                data_uji = pd.read_excel(namafile, header=1) """

                # simpan data kedalam bentuk list/array
                data_uji = np.array(alda)

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
                msg.setText("Lakukan Proses Pelatihan Terlebih Dahulu!")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()

        except:
            print(f'Terjadi kesalahan pada proses pembacaan data baris-{sys.exc_info()[-1].tb_lineno}:\n{sys.exc_info()}')

    # mendifinisikan fungsi untuk menampilkan bobot awal
    def BacaBobot(self):
        try:
            # mengambil variabel global
            n_input = int(self.sgui.eNInp.displayText())
            n_hidden = int(self.sgui.eNHid.displayText())
            n_output = int(self.sgui.eNOut.displayText())

            if n_hidden < 1:
                print("Error Tidak Bisa Generate Bobot & Bias!")
                msg = QMessageBox()
                msg.setWindowTitle("Proses Generate Bias & Bobot Awal Dibatalkan!")
                msg.setText("Error Tidak Bisa Generate Bobot & Bias Awal!")
                msg.setIcon(QMessageBox.Warning)
                x = msg.exec_()
            else:
                # inisialisasi awal bobot V dan bobot W              
                [v, w] = self.pre.Acakbobot(n_input, n_hidden, n_output)
                vlist = v.tolist()
                wlist = w.tolist()

                cur = self.madb.cursor()
                if n_hidden > 1 :
                    cur.execute("DROP TABLE tb_bobotv")
                    cur.execute("TRUNCATE TABLE tb_bobotw")
                    incol = "n1"
                    crecol = "n1 FLOAT NOT NULL"
                    inval = "%s"
                    for i in range(1, n_hidden):
                        i = i+1
                        colu = f", n{i}"
                        colval = ", %s"
                        colcre = f", n{i} FLOAT NOT NULL"
                        incol += colu
                        inval += colval
                        crecol += colcre
                    cur.execute(f"CREATE TABLE tb_bobotv ({crecol})")
                    sql = f"INSERT INTO tb_bobotv ({incol}) VALUES ({inval})"
                    cur.executemany(sql, vlist)
                    self.madb.commit()
                    sql = "INSERT INTO tb_bobotw (n1) VALUES (%s)"
                    cur.executemany(sql, wlist)
                    self.madb.commit()
                    print("sukses")
                    self.sgui.BobotHasil.setTitle("Bias dan Bobot Awal")
                elif n_hidden == 1:
                    cur.execute("DROP TABLE tb_bobotv")
                    cur.execute("TRUNCATE TABLE tb_bobotw")
                    incol = "n1"
                    crecol = "n1 FLOAT NOT NULL"
                    inval = f"%s"
                    print(incol,"\n")
                    print(inval,"\n")
                    print(crecol,"\n")
                    cur.execute(f"CREATE TABLE tb_bobotv ({crecol})")
                    sqll = f"INSERT INTO tb_bobotv ({incol}) VALUES ({inval})"
                    cur.executemany(sqll, vlist)
                    self.madb.commit()
                    sql = "INSERT INTO tb_bobotw (n1) VALUES (%s)"
                    cur.executemany(sql, wlist)
                    self.madb.commit()
                    print("sukses")
                    self.sgui.BobotHasil.setTitle("Bias dan Bobot Awal")
                else:
                    print("Error Tidak Bisa Generate Bobot!")

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
                cur.execute("UPDATE tb_params SET dincol = %s, dcrecol = %s, dinsval = %s, ninput = %s, nhidden = %s, noutput = %s WHERE id = 1",(incol, crecol, inval, n_input, n_hidden, n_output,))
                self.madb.commit()
                self.incol = incol
                self.crecol = crecol
                self.inval = inval
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

                # menampilkan waktu pelatihan dan nilai MSE
                time_stop = round((time.perf_counter() - time_start),2)
                self.sgui.eWaktu.setText(str(time_stop))
                self.sgui.eMSE.setText(str(mse[jml_iterasi-1, 0]))
                self.sgui.BobotHasil.setTitle("Bias dan Bobot Hasil")
                
                # menyimpan hasil bias & bobot ke database
                vlist = v.tolist()

                wlist = w.tolist()

                cur = self.madb.cursor()
                cur.execute("TRUNCATE TABLE tb_bobotv")
                cur.execute("TRUNCATE TABLE tb_bobotw")
                cur.execute("SELECT dincol, dcrecol, dinsval FROM tb_params WHERE id = 1")
                alda = cur.fetchall()
                sqll1 = f"INSERT INTO tb_bobotv ({alda[0][0]}) VALUES ({alda[0][2]})"
                cur.executemany(sqll1, vlist)
                self.madb.commit()
                sqll2 = "INSERT INTO tb_bobotw (n1) VALUES (%s)"
                cur.executemany(sqll2, wlist)
                self.madb.commit()

                smse = mse.tolist()
                cur.execute("TRUNCATE TABLE tb_mse")
                sqll = "INSERT INTO tb_mse (mse) VALUES (%s)"
                cur.executemany(sqll, smse)
                self.madb.commit()
                cur.execute(f"UPDATE tb_params SET alpha = {alpha}, minerr = {min_error},  iterasi = {iterasi} WHERE id = 1")
                self.madb.commit()

                # menyimpan data hasil bobot pelatihan ke dalam variabel global
                self.v = v
                self.w = w
                self.mse = mse
                self.iterasi = iterasi
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
                cur = self.madb.cursor()
                cur.execute("SELECT mse FROM tb_mse")
                alda = cur.fetchall()
                mse = np.array(alda)
                cur.execute("SELECT iterasi FROM tb_params")
                alda = cur.fetchone()[0]
                iterasi = alda
                
                # menampilkan detail grafik
                plt.figure()
                plt.plot(mse[0:iterasi, 0])
                plt.ylim(ymin=0)
                plt.xlabel('Iterasi ke-i, (0 < i < '+str(iterasi)+')')
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
                
                # menampilkan waktu pelatihan dan nilai MSE
                time_stop = (time.perf_counter() - time_start)
                time_stop = time_stop/60
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
        self.tampilForm = FormKelola(self.adminnama)
        self.close()
    
    def get_random_alphaNumeric_string(self, stringLength):
        lettersAndDigits = string.ascii_letters + string.digits
        return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))
    
    def TambahAdmin(self):
        cur = self.madb.cursor()
        i = 0
        while i < 100:
            uniqeKey = self.get_random_alphaNumeric_string(8)
            cur.execute("SELECT uniqe_key FROM tb_uniqekey WHERE uniqe_key = %s",(uniqeKey,))
            idd = cur.fetchall()
            idds = len(idd)
            if idds == 0:
                cur.execute("INSERT INTO tb_uniqekey (uniqe_key) VALUES (%s)",(uniqeKey,))
                self.madb.commit()
                print(uniqeKey)
                break
            i += 1

        unikKey = uniqeKey
        msg = QMessageBox()
        msg.setWindowTitle("Berhasil Menambah Admin!")
        msg.setText(f"<html><head/><body><p>Berhasil meng-generate Uniqe Key</p><p>Silahkan catat atau copy kode berikut: <span style=\" font-size:8pt; font-weight:600;\">{unikKey}</span></p></body></html>")
        msg.setDetailedText(f"{unikKey}")
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def LogOut(self):
        self.tampilForm = FormMain()
        self.close()

class FormKelola(QMainWindow):

    def __init__(self, namaAdmin):
    #def __init__(self):
        QMainWindow.__init__(self)
        self.sgui = gui_kelola.Ui_MainWindow()
        self.sgui.setupUi(self)
        self.namaAdmin = namaAdmin
        kontrolDB.konek(self) #panggil fungsi koneksi server

        self.sgui.pbLatih.clicked.connect(self.bacaDataLatih)
        self.sgui.pbLatih.animateClick()
        self.sgui.pbUji.clicked.connect(self.bacaDataUji)
        self.sgui.pbHapusAll.clicked.connect(self.hapusSemuaData)
        self.sgui.pbTambah.clicked.connect(self.tambahData)
        self.sgui.pbTmbFile.clicked.connect(self.tambahDataFile)
        self.sgui.pbKembali.clicked.connect(self.Kembali)
        self.show()

    def bacaDataLatih(self):
        try:
            self.sgui.pbLatih.setChecked(True)
            # membaca data latih dari database
            np.set_printoptions(suppress=True, linewidth=np.inf)
            cur = self.madb.cursor()
            cur.execute("SELECT * FROM data_latih")
            alda = cur.fetchall()
            data_latih = np.array(alda) # simpan data kedalam bentuk list/array
            n_datalatih = len(data_latih)

            # menampilkan data latih pada tabel
            self.sgui.tbDataPre.setRowCount(0)
            self.sgui.tbDataPre.setRowCount(n_datalatih)
            for i in range(n_datalatih):
                self.sgui.tbDataPre.setItem(i,0,QTableWidgetItem(str(int(data_latih[i,0])))) # membaca parameter NIM
                for j in range(18):
                    k = j + 1
                    self.sgui.tbDataPre.setItem(i,k,QTableWidgetItem(str(data_latih[i,k]))) # membaca paramater input latih x1-x18
                self.sgui.tbDataPre.setItem(i,19,QTableWidgetItem(str(data_latih[i,19]))) # membaca parameter target(IPK)
            self.statData = 1;
            self.sgui.pbUji.setChecked(False)
        except:
            print(f'Terjadi kesalahan pada proses pembacaan data baris-{sys.exc_info()[-1].tb_lineno}:\n{sys.exc_info()}')

    def bacaDataUji(self):
        try:
            self.sgui.pbUji.setChecked(True)
            # membaca data latih dari database
            np.set_printoptions(suppress=True, linewidth=np.inf)
            cur = self.madb.cursor()
            cur.execute("SELECT * FROM data_uji")
            alda = cur.fetchall()
            data_uji = np.array(alda) # simpan data kedalam bentuk list/array
            n_datauji = len(data_uji)

            # menampilkan data latih pada tabel
            self.sgui.tbDataPre.setRowCount(0)
            self.sgui.tbDataPre.setRowCount(n_datauji)
            for i in range(n_datauji):
                self.sgui.tbDataPre.setItem(i,0,QTableWidgetItem(str(int(data_uji[i,0])))) # membaca parameter NIM
                for j in range(18):
                    k = j + 1
                    self.sgui.tbDataPre.setItem(i,k,QTableWidgetItem(str(data_uji[i,k]))) # membaca paramater input latih x1-x18
                self.sgui.tbDataPre.setItem(i,19,QTableWidgetItem(str(data_uji[i,19]))) # membaca parameter target(IPK)
            self.statData = 2;
            self.sgui.pbLatih.setChecked(False)
        except:
            print(f'Terjadi kesalahan pada proses pembacaan data baris-{sys.exc_info()[-1].tb_lineno}:\n{sys.exc_info()}')

    def tambahData(self):
        try:
            statData = self.statData
            print(statData)

            lnim = self.sgui.leNIM.text()
            lx1 = self.sgui.leX1.text()
            lx2 = self.sgui.leX2.text()
            lx3 = self.sgui.leX3.text()
            lx4 = self.sgui.leX4.text()
            lx5 = self.sgui.leX5.text()
            lx6 = self.sgui.leX6.text()
            lx7 = self.sgui.leX7.text()
            lx8 = self.sgui.leX8.text()
            lx9 = self.sgui.leX9.text()
            lx10 = self.sgui.leX10.text()
            lx11 = self.sgui.leX11.text()
            lx12 = self.sgui.leX12.text()
            lx13 = self.sgui.leX13.text()
            lx14 = self.sgui.leX14.text()
            lx15 = self.sgui.leX15.text()
            lx16 = self.sgui.leX16.text()
            lx17 = self.sgui.leX17.text()
            lx18 = self.sgui.leX18.text()
            lipk = self.sgui.leIPK.text()

            if lnim != "" and lx1 != "" and lx2 != "" and lx3 != "" and lx4 != "" and lx5 != "" and lx6 != "" and lx7 != "" and lx8 != "" and lx9 != "" and lx10 != "" and lx11 != "" and lx12 != "" and lx13 != "" and lx14 != "" and lx15 != "" and lx16 != "" and lx17 != "" and lx18 != "" and lipk != "" :
                if statData == 1:
                    cur = self.madb.cursor()
                    cur.execute("INSERT INTO data_latih (NIM, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, ipk) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(lnim, lx1, lx2, lx3, lx4, lx5, lx6, lx7, lx8, lx9, lx10, lx11, lx12, lx13, lx14, lx15, lx16, lx17, lx18, lipk,))
                    self.madb.commit()
                    print(f"Berhasil Menambahkan data latih {lnim}")
                    self.bacaDataLatih()
                elif statData == 2:
                    cur = self.madb.cursor()
                    cur.execute("INSERT INTO data_uji (NIM, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, ipk) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(lnim, lx1, lx2, lx3, lx4, lx5, lx6, lx7, lx8, lx9, lx10, lx11, lx12, lx13, lx14, lx15, lx16, lx17, lx18, lipk,))
                    self.madb.commit()
                    print(f"Berhasil Menambahkan data uji {lnim}")
                    self.bacaDataUji()
                else:
                    print("Error")
            else:
                print("Error")
            
            self.sgui.leNIM.setText("")
            self.sgui.leX1.setText("")
            self.sgui.leX2.setText("")
            self.sgui.leX3.setText("")
            self.sgui.leX4.setText("")
            self.sgui.leX5.setText("")
            self.sgui.leX6.setText("")
            self.sgui.leX7.setText("")
            self.sgui.leX8.setText("")
            self.sgui.leX9.setText("")
            self.sgui.leX10.setText("")
            self.sgui.leX11.setText("")
            self.sgui.leX12.setText("")
            self.sgui.leX13.setText("")
            self.sgui.leX14.setText("")
            self.sgui.leX15.setText("")
            self.sgui.leX16.setText("")
            self.sgui.leX17.setText("")
            self.sgui.leX18.setText("")
            self.sgui.leIPK.setText("")
            
            lnim = None
            lx1 = None
            lx2 = None
            lx3 = None
            lx4 = None
            lx5 = None
            lx6 = None
            lx7 = None
            lx8 = None
            lx9 = None
            lx10 = None
            lx11 = None
            lx12 = None
            lx13 = None
            lx14 = None
            lx15 = None
            lx16 = None
            lx17 = None
            lx18 = None
            lipk = None

        except:
            print(f'Terjadi kesalahan pada proses pembacaan data baris-{sys.exc_info()[-1].tb_lineno}:\n{sys.exc_info()}')

    def tambahDataFile(self):
        try:
            statData = self.statData
            print(statData)
            
            if statData == 1:
                teks = "latih"
                tb = "data_latih"
            elif statData == 2:
                teks = "uji"
                tb = "data_uji"
            else:
                print("Error")
            
            # membaca file CSV data input dari penyimpanan lokal
            path = QFileDialog.getOpenFileName(self, f'Silahkan pilih file data {teks}', '', "XLSX files (*.xlsx)")
            namafile = path[0]
            np.set_printoptions(suppress=True, linewidth=np.inf)
            data = pd.read_excel(namafile, header=1)
            data = np.array(data) # simpan data kedalam bentuk list/array
            dataa = np.around(data,2)
            in_data = data.tolist()

            cur = self.madb.cursor()
            sqll = f"INSERT INTO {tb} (NIM, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, ipk) VALUES "+"(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            vall = in_data
            cur.executemany(sqll, vall)
            self.madb.commit()
            print(cur.rowcount, f"Data berhasil menambahkan data {teks} dari file!")

            if statData == 1:
                self.bacaDataLatih()
            elif statData == 2:
                self.bacaDataUji()
            else:
                print("Error")
            
            path = None
            namafile = None
            data = None
            dataa = None
            in_data = None
            cur = None
            sqll = None
            vall = None

        except:
            print(f'Terjadi kesalahan pada proses pembacaan data baris-{sys.exc_info()[-1].tb_lineno}:\n{sys.exc_info()[1]}')

    def hapusSemuaData(self):
        try:
            statData = self.statData
            print(statData)
            
            if statData == 1:
                judul = "Latih"
                tb = "data_latih"
                self.bacaDataLatih()
            elif statData == 2:
                judul = "Uji"
                tb = "data_uji"
                self.bacaDataUji()
            else:
                print("Error")

            msg = QMessageBox()
            msg.setWindowTitle(f"Konfirmasi Penghapusan Semua Data {judul}")
            msg.setText(f"Apakah Anda Yakin Menghapus Semua Data {judul}?")
            msg.setStandardButtons(QMessageBox.Ok|QMessageBox.Cancel)
            msg.setIcon(QMessageBox.Information)
            msg.buttonClicked.connect(self.popupButton)
            x = msg.exec_()
            if self.statKonf == "OK":
                cura = self.madb.cursor()
                print(f"Berhasil Menghapus Semua Data {judul}")
                if tb == "data_latih":
                    cura.execute("DROP TABLE data_latih")
                    cura.execute("CREATE TABLE data_latih ( NIM INT NOT NULL ,  x1 FLOAT NOT NULL ,  x2 FLOAT NOT NULL ,  x3 FLOAT NOT NULL ,  x4 FLOAT NOT NULL ,  x5 FLOAT NOT NULL ,  x6 FLOAT NOT NULL ,  x7 FLOAT NOT NULL ,  x8 FLOAT NOT NULL ,  x9 FLOAT NOT NULL ,  x10 FLOAT NOT NULL ,  x11 FLOAT NOT NULL ,  x12 FLOAT NOT NULL ,  x13 FLOAT NOT NULL ,  x14 FLOAT NOT NULL ,  x15 FLOAT NOT NULL ,  x16 FLOAT NOT NULL ,  x17 FLOAT NOT NULL ,  x18 FLOAT NOT NULL ,  ipk FLOAT NOT NULL)")
                elif tb == "data_uji":
                    cura.execute("DROP TABLE data_uji")
                    cura.execute("CREATE TABLE data_uji ( NIM INT NOT NULL ,  x1 FLOAT NOT NULL ,  x2 FLOAT NOT NULL ,  x3 FLOAT NOT NULL ,  x4 FLOAT NOT NULL ,  x5 FLOAT NOT NULL ,  x6 FLOAT NOT NULL ,  x7 FLOAT NOT NULL ,  x8 FLOAT NOT NULL ,  x9 FLOAT NOT NULL ,  x10 FLOAT NOT NULL ,  x11 FLOAT NOT NULL ,  x12 FLOAT NOT NULL ,  x13 FLOAT NOT NULL ,  x14 FLOAT NOT NULL ,  x15 FLOAT NOT NULL ,  x16 FLOAT NOT NULL ,  x17 FLOAT NOT NULL ,  x18 FLOAT NOT NULL ,  ipk FLOAT NOT NULL)")
                else:
                    print("error")

                if statData == 1:
                    self.bacaDataLatih()
                elif statData == 2:
                    self.bacaDataUji()
                else:
                    print("Error")
            else:
                print("Tidak Jadi Menghapus Semua Data")
            
            judul = None
            tb = None

        except:
            print(f'Terjadi kesalahan pada proses pembacaan data baris-{sys.exc_info()[-1].tb_lineno}:\n{sys.exc_info()}')
    
    def popupButton(self, i):
        self.statKonf = i.text()
        print(i.text())

    def Kembali(self):
        adminnama = self.namaAdmin
        self.tampilForm = FormPelatihanJST(adminnama)
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
    #w = FormKelola()
    sys.exit(app.exec_())
