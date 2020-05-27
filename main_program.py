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

import sendEmail as sE

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
        self.setWindowTitle("(JST BACKPROPAGATION) Prediksi IPK Mahasiswa Sistem Komputer S1")
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
        self.madb.close()
        self.close()

    def tampilPrediksi(self):
        self.tampilForm = FormPrediksi()
        self.madb.close()
        self.close()

    def tampilRegister(self):
        self.tampilForm = FormRegister()
        self.madb.close()
        self.close()

class FormLogin(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.sgui = gui_login.Ui_MainWindow()
        self.sgui.setupUi(self)
        self.setWindowTitle("(JST BACKPROPAGATION) Prediksi IPK Mahasiswa Sistem Komputer S1 - Menu Login")
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
            self.madb.close()
            self.close()
        else:
            msg = QMessageBox()
            msg.setWindowTitle("Login Gagal!")
            msg.setText("Id atau Password Salah!")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
            self.sgui.leId.setText("")
            self.sgui.lePass.setText("")
            print("gagal login")

    def tampilRegister(self):
        self.tampilForm = FormRegister()
        self.madb.close()
        self.close()
    
    def tampilLupa(self):
        self.tampilForm = FormLupa()
        self.madb.close()
        self.close()
    
    def tampilPetunjuk(self):
        petunjuk = 2
        self.tampilForm = FormPetunjuk(petunjuk)

    def Kembali(self):
        self.tampilForm = FormMain()
        self.madb.close()
        self.close()

class FormLupa(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.sgui = gui_lupa.Ui_MainWindow()
        self.sgui.setupUi(self)
        self.setWindowTitle("(JST BACKPROPAGATION) Prediksi IPK Mahasiswa Sistem Komputer S1 - Menu Lupa Password atau Id")

        self.sgui.pbKirim.clicked.connect(self.Kirim)
        self.sgui.pbKembali.clicked.connect(self.Kembali)
        self.show()
    
    def Kirim(self):
        try:
            kontrolDB.konek(self)
            eemail = self.sgui.leEmail.text()
            cur = self.madb.cursor()
            cur.execute(f"SELECT id, nama, password FROM tb_admin WHERE email = '{eemail}'")
            alda = cur.fetchall()
            bada = len(alda)
            cur.close()
            if bada != 0 :
                idadmin = alda[0][0]
                namaAdmin = alda[0][1]
                pswd = alda[0][2]
                sE.kirimEmail(eemail, namaAdmin, idadmin, pswd)
                msg = QMessageBox()
                msg.setWindowTitle("Mengirim Bantuan Berhasil!")
                msg.setText("Bantuan berhasil dikirim ke e-mail anda!")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
                self.sgui.leEmail.setText("")
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Mengirim Bantuan Gagal!")
                msg.setText("Bantuan gagal dikirim! email yang anda masukan tidak terdaftar.")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
                self.sgui.leEmail.setText("")
            self.madb.close()
        except:
            print(f'Terjadi kesalahan pada proses pembacaan data baris-{sys.exc_info()[-1].tb_lineno}:\n{sys.exc_info()}')


    def Kembali(self):
        self.tampilForm = FormLogin()
        self.close()

class FormRegister(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.sgui = gui_register.Ui_MainWindow()
        self.sgui.setupUi(self)
        self.setWindowTitle("(JST BACKPROPAGATION) Prediksi IPK Mahasiswa Sistem Komputer S1 - Menu Registrasi")

        kontrolDB.konek(self)

        self.sgui.pbRegister.clicked.connect(self.Registerr)
        self.sgui.pbKembali.clicked.connect(self.Kembali)
        self.show()

    def Registerr(self):
        statada = ""
        stattoken = ""

        leuniqe = str(self.sgui.leNama_2.displayText())
        lenama = str(self.sgui.leNama.displayText())
        leemail = str(self.sgui.leEmail.displayText())
        leid = str(self.sgui.leId.displayText())
        lepass = str(self.sgui.lePass.text())

        cur = self.madb.cursor()
        cur = self.madb.cursor()
        cur.execute("SELECT uniqe_key FROM tb_admin WHERE uniqe_key = %s",(leuniqe,))
        ccuniqe = cur.fetchall()
        cur.close()
        ccuniqe = len(ccuniqe)
        
        cur = self.madb.cursor()
        cur.execute("SELECT uniqe_key FROM tb_uniqekey WHERE uniqe_key = %s",(leuniqe,))
        ccuniqe2 = cur.fetchall()
        cur.close()
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

        cur = self.madb.cursor()
        cur.execute("SELECT nama FROM tb_admin WHERE nama = %s",(lenama,))
        ccnama = cur.fetchall()
        cur.close()
        ccnama = len(ccnama)
        if ccnama > 0:
            print("Nama sudah dipakai")
            statada += "Nama, " 
            statb = 1
        else:
            statb = 0

        cur = self.madb.cursor()
        cur.execute("SELECT email FROM tb_admin WHERE email = %s",(leemail,))
        ccemail = cur.fetchall()
        cur.close()
        ccemail = len(ccemail)
        if ccemail > 0:
            print("Email sudah dipakai")
            statada += "E-mail, " 
            statc = 1
        else:
            statc = 0

        cur = self.madb.cursor()
        cur.execute("SELECT id FROM tb_admin WHERE id = %s",(leid,))
        ccid = cur.fetchall()
        cur.close()
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
            cur = self.madb.cursor()
            cur.execute("UPDATE tb_uniqekey SET id = %s WHERE uniqe_key = %s",(leid, leuniqe,))
            self.madb.commit()
            cur.close()
            cur = self.madb.cursor()
            cur.execute("INSERT INTO tb_admin (uniqe_key, id, nama, email, password) VALUES (%s, %s, %s, %s, %s)",(leuniqe, leid, lenama, leemail, lepass,))
            self.madb.commit()
            cur.close()
            self.tampilForm = FormLogin()
            self.madb.close()
            self.close()

    def Kembali(self):
        self.tampilForm = FormMain()
        self.madb.close()
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
        self.setWindowTitle("(JST BACKPROPAGATION) Prediksi IPK Mahasiswa Sistem Komputer S1 - Menu Petunjuk Penggunaan")

        self.petunjuk = petunjuk

        if petunjuk == 1:
            self.sgui.Judul.setText(f"Petunjuk Penggunaan Prediksi")
            self.sgui.Gambar.setPixmap(QtGui.QPixmap("gambar\Menu-9-prediksi.PNG"))
            self.sgui.idxGambar.setText("Petunjuk Penggunaan Proses Prediksi IPK Mahasiswa")
            self.sgui.pbNext.setHidden(True)
            self.sgui.pbPrevious.setHidden(True)
        elif petunjuk == 2:
            self.sgui.Judul.setText(f"Petunjuk Admin Penggunaan Pelatihan")
            self.sgui.Gambar.setPixmap(QtGui.QPixmap("gambar\Menu-2-login.PNG"))
            self.sgui.idxGambar.setText("Petunjuk admin proses login (1/5)")
            self.gmbrke = 1
        else:
            print("Terjadi Kesalahan")

        self.sgui.pbNext.clicked.connect(self.nextGambar)
        self.sgui.pbPrevious.clicked.connect(self.prevGambar)
        self.sgui.pbOk.clicked.connect(self.keluar)
        self.show()
    
    def nextGambar(self):
        try:
            petunjuk = self.petunjuk
            if petunjuk == 2:
                if self.gmbrke == 1:
                    self.sgui.Gambar.setPixmap(QtGui.QPixmap("gambar\Menu-3-register.PNG"))
                    self.sgui.idxGambar.setText("Petunjuk admin proses registrasi (2/5)")
                    self.gmbrke = 2
                elif self.gmbrke == 2:
                    self.sgui.Gambar.setPixmap(QtGui.QPixmap("gambar\Menu-4-lupa.PNG"))
                    self.sgui.idxGambar.setText("Petunjuk admin proses bantuan lupa password atau id (3/5)")
                    self.gmbrke = 3
                elif self.gmbrke == 3:
                    self.sgui.Gambar.setPixmap(QtGui.QPixmap("gambar\Menu-6-pelatihan.PNG"))
                    self.sgui.idxGambar.setText("Petunjuk admin proses pelatihan BNN (4/5)")
                    self.gmbrke = 4
                elif self.gmbrke == 4:
                    self.sgui.Gambar.setPixmap(QtGui.QPixmap("gambar\Menu-7-kelola.PNG"))
                    self.sgui.idxGambar.setText("Petunjuk admin proses kelola data pelatihan (5/5)")
                    self.gmbrke = 5
                elif self.gmbrke == 5:
                    self.sgui.Gambar.setPixmap(QtGui.QPixmap("gambar\Menu-2-login.PNG"))
                    self.sgui.idxGambar.setText("Petunjuk admin proses login (1/5)")
                    self.gmbrke = 1
                else:
                    self.sgui.Gambar.setText("Error")
            else:
                print("Terjadi Kesalahan")
            print(self.gmbrke)
        except:
            print(f'Terjadi kesalahan pada proses pembacaan data baris-{sys.exc_info()[-1].tb_lineno}:\n{sys.exc_info()}')
    
    def prevGambar(self):
        try:
            petunjuk = self.petunjuk
            if petunjuk == 2:
                if self.gmbrke == 1:
                    self.sgui.Gambar.setPixmap(QtGui.QPixmap("gambar\Menu-7-kelola.PNG"))
                    self.sgui.idxGambar.setText("Petunjuk admin proses kelola data pelatihan (5/5)")
                    self.gmbrke = 5
                elif self.gmbrke == 5:
                    self.sgui.Gambar.setPixmap(QtGui.QPixmap("gambar\Menu-6-pelatihan.PNG"))
                    self.sgui.idxGambar.setText("Petunjuk admin proses pelatihan BNN (4/5)")
                    self.gmbrke = 4
                elif self.gmbrke == 4:
                    self.sgui.Gambar.setPixmap(QtGui.QPixmap("gambar\Menu-4-lupa.PNG"))
                    self.sgui.idxGambar.setText("Petunjuk admin proses bantuan lupa password atau id (3/5)")
                    self.gmbrke = 3
                elif self.gmbrke == 3:
                    self.sgui.Gambar.setPixmap(QtGui.QPixmap("gambar\Menu-3-register.PNG"))
                    self.sgui.idxGambar.setText("Petunjuk admin proses registrasi (2/5)")
                    self.gmbrke = 2
                elif self.gmbrke == 2:
                    self.sgui.Gambar.setPixmap(QtGui.QPixmap("gambar\Menu-2-login.PNG"))
                    self.sgui.idxGambar.setText("Petunjuk admin proses login (1/5)")
                    self.gmbrke = 1
                else:
                    self.sgui.Gambar.setText("Error")
            else:
                print("Terjadi Kesalahan")
            print(self.gmbrke)
        except:
            print(f'Terjadi kesalahan pada proses pembacaan data baris-{sys.exc_info()[-1].tb_lineno}:\n{sys.exc_info()}')
    
    def keluar(self):
        self.close()

class FormPelatihanJST(QMainWindow):

    # deklarasi variabel parrent
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

    # pendefinisian inisialisasi kelas
    def __init__(self, namaAdmin):
        QMainWindow.__init__(self)
        self.sgui = gui_pelatihan.Ui_MainMenu()
        self.sgui.setupUi(self)
        self.setWindowTitle("(JST BACKPROPAGATION) Prediksi IPK Mahasiswa Sistem Komputer S1 - Menu Pelatihan")
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
        self.sgui.pbBaca.setHidden(True)
        self.sgui.pbBaca_2.setHidden(True)
        self.sgui.pbBobot.clicked.connect(self.BacaBobot)
        self.sgui.pbPelatihan.clicked.connect(self.ProPelatihan)
        self.sgui.pbDetailG.clicked.connect(self.DetailGrafik)
        self.sgui.pbPengujian.clicked.connect(self.ProPengujian)
        self.sgui.pbDetailG_2.clicked.connect(self.DetailGrafik_2)
        self.sgui.pbKelola.clicked.connect(self.tampilKelola)
        self.sgui.pbTambah.clicked.connect(self.TambahAdmin)
        self.sgui.pbLogout.clicked.connect(self.LogOut)

        # menampilkan bias & bobot terakhir
        cur = self.madb.cursor()
        cur.execute("SELECT n1 FROM tb_bobotv")
        biasv = cur.fetchall()
        cur.close()
        lbiasv = len(biasv)
        cur = self.madb.cursor()
        cur.execute("SELECT n1 FROM tb_bobotw")
        biasw = cur.fetchall()
        cur.close()
        lbiasw = len(biasw)
        if lbiasv == 0 and lbiasw == 0 :
            biasv = ""
            print("Bobot Kosong")
        else:
            biasv = str(biasv[0][0])
            biasw = str(biasw[0][0])

            np.set_printoptions(suppress=True, linewidth=np.inf)
            cur = self.madb.cursor()
            cur.execute("SELECT * FROM tb_bobotv")
            aldatv = cur.fetchall()
            cur.close()
            v = np.array(aldatv)
            cur = self.madb.cursor()
            cur.execute("SELECT * FROM tb_bobotw")
            aldatw = cur.fetchall()
            cur.close()
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

            # menyimpan data bobot ke dalam variabel parrent
            self.v = v
            self.w = w
            self.staBaBot = 1

            cur = self.madb.cursor()
            cur.execute("SELECT * FROM tb_params")
            alda = cur.fetchall()
            cur.close()
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
            cur = self.madb.cursor()
            cur.execute("SELECT mse FROM tb_mse")
            alda = cur.fetchall()
            cur.close()
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
            cur.close()
            
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

            # menyimpan data latih ke dalam variabel parrent
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
            # mengambil variabel parrent
            staBaPel = self.staBaPel

            if staBaPel == 1:
                # membaca data pelatihan dari database
                np.set_printoptions(suppress=True, linewidth=np.inf)
                cur = self.madb.cursor()
                cur.execute("SELECT * FROM data_uji")
                alda = cur.fetchall()
                cur.close()

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

                # menyimpan data latih dan data uji ke dalam variabel parrent
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
            # mengambil variabel parrent
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

                if n_hidden > 1 :
                    cur = self.madb.cursor()
                    cur.execute("DROP TABLE tb_bobotv")
                    cur.close()
                    cur = self.madb.cursor()
                    cur.execute("TRUNCATE TABLE tb_bobotw")
                    cur.close()
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
                    cur = self.madb.cursor()
                    cur.execute(f"CREATE TABLE tb_bobotv ({crecol})")
                    cur.close()
                    sql = f"INSERT INTO tb_bobotv ({incol}) VALUES ({inval})"
                    cur = self.madb.cursor()
                    cur.executemany(sql, vlist)
                    self.madb.commit()
                    cur.close()
                    cur = self.madb.cursor()
                    sql = "INSERT INTO tb_bobotw (n1) VALUES (%s)"
                    cur.executemany(sql, wlist)
                    self.madb.commit()
                    cur.close()
                    print("sukses")
                    self.sgui.BobotHasil.setTitle("Bias dan Bobot Awal")
                elif n_hidden == 1:
                    cur = self.madb.cursor()
                    cur.execute("DROP TABLE tb_bobotv")
                    cur.close()
                    cur = self.madb.cursor()
                    cur.execute("TRUNCATE TABLE tb_bobotw")
                    cur.close()
                    incol = "n1"
                    crecol = "n1 FLOAT NOT NULL"
                    inval = f"%s"
                    print(incol,"\n")
                    print(inval,"\n")
                    print(crecol,"\n")
                    cur = self.madb.cursor()
                    cur.execute(f"CREATE TABLE tb_bobotv ({crecol})")
                    cur.close()
                    sqll = f"INSERT INTO tb_bobotv ({incol}) VALUES ({inval})"
                    cur = self.madb.cursor()
                    cur.executemany(sqll, vlist)
                    self.madb.commit()
                    cur.close()
                    sql = "INSERT INTO tb_bobotw (n1) VALUES (%s)"
                    cur = self.madb.cursor()
                    cur.executemany(sql, wlist)
                    self.madb.commit()
                    cur.close()
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

                # menyimpan data bobot ke dalam variabel parrent
                cur = self.madb.cursor()
                cur.execute("UPDATE tb_params SET dincol = %s, dcrecol = %s, dinsval = %s, ninput = %s, nhidden = %s, noutput = %s WHERE id = 1",(incol, crecol, inval, n_input, n_hidden, n_output,))
                self.madb.commit()
                cur.close()
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
            # mengambil variabel parrent
            staBaPel = self.staBaPel
            staBaBot = self.staBaBot

            if staBaPel == 1 and staBaBot == 1:
                time_start = time.perf_counter() # memulai waktu proses

                msg = QMessageBox()
                msg.setStyleSheet("QLabel{min-width: 370px;}");
                msg.setWindowTitle("Proses Pelatihan Sedang Berjalan, Mohon Tunggu Beberapa Menit!")
                msg.show()

                # mengambil data variabel parrent
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
                cur.close()
                cur = self.madb.cursor()
                cur.execute("TRUNCATE TABLE tb_bobotw")
                cur.close()
                cur = self.madb.cursor()
                cur.execute("SELECT dincol, dcrecol, dinsval FROM tb_params WHERE id = 1")
                alda = cur.fetchall()
                cur.close()
                sqll1 = f"INSERT INTO tb_bobotv ({alda[0][0]}) VALUES ({alda[0][2]})"
                cur = self.madb.cursor()
                cur.executemany(sqll1, vlist)
                self.madb.commit()
                cur.close()
                sqll2 = "INSERT INTO tb_bobotw (n1) VALUES (%s)"
                cur = self.madb.cursor()
                cur.executemany(sqll2, wlist)
                self.madb.commit()
                cur.close()

                smse = mse.tolist()
                cur = self.madb.cursor()
                cur.execute("TRUNCATE TABLE tb_mse")
                cur.close()
                sqll = "INSERT INTO tb_mse (mse) VALUES (%s)"
                cur = self.madb.cursor()
                cur.executemany(sqll, smse)
                self.madb.commit()
                cur.close()
                cur = self.madb.cursor()
                cur.execute(f"UPDATE tb_params SET alpha = {alpha}, minerr = {min_error},  iterasi = {iterasi} WHERE id = 1")
                self.madb.commit()
                cur.close()

                # menyimpan data hasil bobot pelatihan ke dalam variabel parrent
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
            # mengambil variabel parrent
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
                cur.close()
                mse = np.array(alda)
                cur = self.madb.cursor()
                cur.execute("SELECT iterasi FROM tb_params")
                alda = cur.fetchone()[0]
                cur.close()
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
            # mengambil variabel parrent
            staBaUji = self.staBaUji
            staPel = self.staPel

            if staBaUji == 1 and staPel == 1:
                time_start = time.perf_counter() # memulai waktu proses

                # mengambil data variabel parrent
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

                # menampilkan hasil ke dalam tabel
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
                self.sgui.eWaktu_2.setText(str(round(time_stop, 2)))
                self.sgui.eMSE_2.setText(str(mse))
                self.sgui.eAkurasi.setText(f"{rata2akurasi:0.2f}")
                
                # menyimpan data hasil bobot pelatihan ke dalam variabel parrent
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

        except:
            print('Terjadi Kesalahan Pada Proses Pelatihan {}'.format(sys.exc_info()[-1].tb_lineno))
    
    # mendifinisikan fungsi detail grafik pengujian
    def DetailGrafik_2(self):
        try:
            # mengambil variabel parrent
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
        self.madb.close()
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
            cur.close()
            idds = len(idd)
            if idds == 0:
                cur = self.madb.cursor()
                cur.execute("INSERT INTO tb_uniqekey (uniqe_key) VALUES (%s)",(uniqeKey,))
                self.madb.commit()
                cur.close()
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
        self.madb.close()
        self.close()

class FormKelola(QMainWindow):

    def __init__(self, namaAdmin):
        QMainWindow.__init__(self)
        self.sgui = gui_kelola.Ui_MainWindow()
        self.sgui.setupUi(self)
        self.setWindowTitle("(JST BACKPROPAGATION) Prediksi IPK Mahasiswa Sistem Komputer S1 - Menu Kelola Data Pelatihan")
        self.namaAdmin = namaAdmin
        self.sgui.lAdmin.setText(str(namaAdmin))
        kontrolDB.konek(self) #panggil fungsi koneksi server

        #setup status bar
        self.sgui.statusbarr = QStatusBar()
        self.setStatusBar(self.sgui.statusbarr)
        self.sgui.statusbarr.setStyleSheet('background-color: #FFFFFF;')

        self.sgui.lstatus = QLabel()
        self.sgui.lbdata = QLabel()
        self.sgui.lstatus.setText(self.statSer)
        self.sgui.lbdata.setText(str(""))
        
        self.sgui.statusbarr.addWidget(self.sgui.lstatus)
        self.sgui.statusbarr.addWidget(self.sgui.lbdata)

        self.sgui.pbLatih.clicked.connect(self.bacaDataLatih)
        self.sgui.tbDataPre.cellClicked.connect(self.pilihData)
        self.sgui.pbLatih.animateClick()
        self.sgui.pbUji.clicked.connect(self.bacaDataUji)
        self.sgui.pbHapusOne.clicked.connect(self.hapusSatu)
        self.sgui.pbHapusAll.clicked.connect(self.hapusSemuaData)
        self.sgui.pbUpdate.clicked.connect(self.ubahData)
        self.sgui.pbTambah.clicked.connect(self.tambahData)
        self.sgui.pbClear.clicked.connect(self.bersihkanInputan)
        self.sgui.pbTmbFile.clicked.connect(self.tambahDataFile)
        self.sgui.pbSearch.clicked.connect(self.cariData)
        self.sgui.pbKembali.clicked.connect(self.Kembali)
        self.show()
    
    def cariData(self):
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
        
            if lnim != "" or lx1 != "" or lx2 != "" or lx3 != "" or lx4 != "" or lx5 != "" or lx6 != "" or lx7 != "" or lx8 != "" or lx9 != "" or lx10 != "" or lx11 != "" or lx12 != "" or lx13 != "" or lx14 != "" or lx15 != "" or lx16 != "" or lx17 != "" or lx18 != "" or lipk != "" :
                bSec = 0
                bSql = ""
                if lnim != "":
                    bSec += 1
                    bSql += f"nim LIKE '%{lnim}%'"
                else:
                    print("no nim")
                if lx1 != "":
                    if bSec != 0:
                        bSec += 1
                        bSql += f"and x1 LIKE '%{lx1}%'"
                    else:
                        bSec += 1
                        bSql += f"x1 LIKE '%{lx1}%'"
                else:
                    print("no lx1")
                if lx2 != "":
                    if bSec != 0:
                        bSec += 1
                        bSql += f"and x2 LIKE '%{lx2}%'"
                    else:
                        bSec += 1
                        bSql += f"x2 LIKE '%{lx2}%'"
                else:
                    print("no lx2")
                if lx3 != "":
                    if bSec != 0:
                        bSec += 1
                        bSql += f"and x3 LIKE '%{lx3}%'"
                    else:
                        bSec += 1
                        bSql += f"x3 LIKE '%{lx3}%'"
                else:
                    print("no lx3")
                if lx4 != "":
                    if bSec != 0:
                        bSec += 1
                        bSql += f"and x4 LIKE '%{lx4}%'"
                    else:
                        bSec += 1
                        bSql += f"x4 LIKE '%{lx4}%'"
                else:
                    print("no lx4")
                if lx5 != "":
                    if bSec != 0:
                        bSec += 1
                        bSql += f"and x5 = '{lx5}'"
                    else:
                        bSec += 1
                        bSql += f"x5 = '{lx5}'"
                else:
                    print("no lx5")
                if lx6 != "":
                    if bSec != 0:
                        bSec += 1
                        bSql += f"and x6 = '{lx6}'"
                    else:
                        bSec += 1
                        bSql += f"x6 = '{lx6}'"
                else:
                    print("no lx6")
                if lx7 != "":
                    if bSec != 0:
                        bSec += 1
                        bSql += f"and x7 = '{lx7}'"
                    else:
                        bSec += 1
                        bSql += f"x7 = '{lx7}'"
                else:
                    print("no lx7")
                if lx8 != "":
                    if bSec != 0:
                        bSec += 1
                        bSql += f"and x8 = '{lx8}'"
                    else:
                        bSec += 1
                        bSql += f"x8 = '{lx8}'"
                else:
                    print("no lx8")
                if lx9 != "":
                    if bSec != 0:
                        bSec += 1
                        bSql += f"and x9 = '{lx9}'"
                    else:
                        bSec += 1
                        bSql += f"x9 = '{lx9}'"
                else:
                    print("no lx9")
                if lx10 != "":
                    if bSec != 0:
                        bSec += 1
                        bSql += f"and x10 = '{lx10}'"
                    else:
                        bSec += 1
                        bSql += f"x10 = '{lx10}'"
                else:
                    print("no lx10")
                if lx11 != "":
                    if bSec != 0:
                        bSec += 1
                        bSql += f"and x11 = '{lx11}'"
                    else:
                        bSec += 1
                        bSql += f"x11 = '{lx11}'"
                else:
                    print("no lx11")
                if lx12 != "":
                    if bSec != 0:
                        bSec += 1
                        bSql += f"and x12 = '{lx12}'"
                    else:
                        bSec += 1
                        bSql += f"x12 = '{lx12}'"
                else:
                    print("no lx12")
                if lx13 != "":
                    if bSec != 0:
                        bSec += 1
                        bSql += f"and x13 = '{lx13}'"
                    else:
                        bSec += 1
                        bSql += f"x13 = '{lx13}'"
                else:
                    print("no lx13")
                if lx14 != "":
                    if bSec != 0:
                        bSec += 1
                        bSql += f"and x14 = '{lx14}'"
                    else:
                        bSec += 1
                        bSql += f"x14 = '{lx14}'"
                else:
                    print("no lx14")
                if lx15 != "":
                    if bSec != 0:
                        bSec += 1
                        bSql += f"and x15 = '{lx15}'"
                    else:
                        bSec += 1
                        bSql += f"x15 = '{lx15}'"
                else:
                    print("no lx15")
                if lx16 != "":
                    if bSec != 0:
                        bSec += 1
                        bSql += f"and x16 = '{lx16}'"
                    else:
                        bSec += 1
                        bSql += f"x16 = '{lx16}'"
                else:
                    print("no lx16")
                if lx17 != "":
                    if bSec != 0:
                        bSec += 1
                        bSql += f"and x17 = '{lx17}'"
                    else:
                        bSec += 1
                        bSql += f"x17 = '{lx17}'"
                else:
                    print("no lx17")
                if lx18 != "":
                    if bSec != 0:
                        bSec += 1
                        bSql += f"and x18 = '{lx18}'"
                    else:
                        bSec += 1
                        bSql += f"x18 = '{lx18}'"
                else:
                    print("no l1x8")
                if lipk != "":
                    if bSec != 0:
                        bSec += 1
                        bSql += f"and ipk LIKE '%{lipk}%'"
                    else:
                        bSec += 1
                        bSql += f"ipk LIKE '%{lipk}%'"
                else:
                    print("no lipk")
                
                print(f"jumlah filter ={bSec}")
                print(f"sql = {bSql}")

                if statData == 1:
                    cur = self.madb.cursor()
                    cur.execute(f"SELECT * FROM data_latih WHERE {bSql}")
                    idd = cur.fetchall()
                    cur.close()
                    data_latih = np.array(idd) # simpan data kedalam bentuk list/array
                    idds = len(idd)

                    # menampilkan data latih pada tabel
                    self.sgui.tbDataPre.setRowCount(0)
                    self.sgui.tbDataPre.setRowCount(idds)
                    for i in range(idds):
                        self.sgui.tbDataPre.setItem(i,0,QTableWidgetItem(str(int(data_latih[i,0])))) # membaca parameter NIM
                        for j in range(4):
                            k = j + 1
                            self.sgui.tbDataPre.setItem(i,k,QTableWidgetItem(str(data_latih[i,k]))) # membaca paramater input latih x1-x18
                        for l in range(4, 18):
                            k = l + 1
                            self.sgui.tbDataPre.setItem(i,k,QTableWidgetItem(str(int(data_latih[i,k])))) # membaca paramater input latih x1-x18
                        self.sgui.tbDataPre.setItem(i,19,QTableWidgetItem(str(data_latih[i,19]))) # membaca parameter target(IPK)
                    
                    print(f"Banyak data yang terfilter: {idds}")
                    print("Data yang terfilter:\n",idd)
                    bSql = ""
                elif statData == 2:
                    cur = self.madb.cursor()
                    cur.execute(f"SELECT * FROM data_uji WHERE {bSql}")
                    idd = cur.fetchall()
                    cur.close()
                    data_uji = np.array(idd) # simpan data kedalam bentuk list/array
                    idds = len(idd)

                    # menampilkan data latih pada tabel
                    self.sgui.tbDataPre.setRowCount(0)
                    self.sgui.tbDataPre.setRowCount(idds)
                    for i in range(idds):
                        self.sgui.tbDataPre.setItem(i,0,QTableWidgetItem(str(int(data_uji[i,0])))) # membaca parameter NIM
                        for j in range(4):
                            k = j + 1
                            self.sgui.tbDataPre.setItem(i,k,QTableWidgetItem(str(data_uji[i,k]))) # membaca paramater input latih x1-x18
                        for l in range(4,18):
                            k = l + 1
                            self.sgui.tbDataPre.setItem(i,k,QTableWidgetItem(str(int(data_uji[i,k])))) # membaca paramater input latih x1-x18
                        self.sgui.tbDataPre.setItem(i,19,QTableWidgetItem(str(data_uji[i,19]))) # membaca parameter target(IPK)

                    print(f"Banyak data yang terfilter: {idds}")
                    print("Data yang terfilter:\n",idd)
                    bSql = ""
                else:
                    print("Error")
            else:
                if statData == 1:
                    self.bacaDataLatih()
                elif statData == 2:
                    self.bacaDataUji()
                else:
                    print("Error")
        except:
            print(f'Terjadi kesalahan pada proses pembacaan data baris-{sys.exc_info()[-1].tb_lineno}:\n{sys.exc_info()}')

    def pilihData(self, row, column):
        item = self.sgui.tbDataPre.item(row, 0)
        self.ID = item.text()
        print(f"Baris {row} dan kolom {column} dipilih, NIM: {self.ID}")

        items = np.zeros((20,1))
        for i in range(20):
            item = self.sgui.tbDataPre.item(row, i)
            items[i,0] = item.text()
        self.sgui.leNIM.setText(str(int(items[0,0])))
        self.sgui.leX1.setText(str(float(items[1,0])))
        self.sgui.leX2.setText(str(float(items[2,0])))
        self.sgui.leX3.setText(str(float(items[3,0])))
        self.sgui.leX4.setText(str(float(items[4,0])))
        self.sgui.leX5.setText(str(int(items[5,0])))
        self.sgui.leX6.setText(str(int(items[6,0])))
        self.sgui.leX7.setText(str(int(items[7,0])))
        self.sgui.leX8.setText(str(int(items[8,0])))
        self.sgui.leX9.setText(str(int(items[9,0])))
        self.sgui.leX10.setText(str(int(items[10,0])))
        self.sgui.leX11.setText(str(int(items[11,0])))
        self.sgui.leX12.setText(str(int(items[12,0])))
        self.sgui.leX13.setText(str(int(items[13,0])))
        self.sgui.leX14.setText(str(int(items[14,0])))
        self.sgui.leX15.setText(str(int(items[15,0])))
        self.sgui.leX16.setText(str(int(items[16,0])))
        self.sgui.leX17.setText(str(int(items[17,0])))
        self.sgui.leX18.setText(str(int(items[18,0])))
        self.sgui.leIPK.setText(str(float(items[19,0])))

    def bacaDataLatih(self):
        try:
            self.sgui.pbLatih.setChecked(True)
            # membaca data latih dari database
            np.set_printoptions(suppress=True, linewidth=np.inf)
            cur = self.madb.cursor()
            cur.execute("SELECT * FROM data_latih")
            alda = cur.fetchall()
            cur.close()
            data_latih = np.array(alda) # simpan data kedalam bentuk list/array
            n_datalatih = len(data_latih)

            # menampilkan data latih pada tabel
            self.sgui.tbDataPre.setRowCount(0)
            self.sgui.tbDataPre.setRowCount(n_datalatih)
            for i in range(n_datalatih):
                self.sgui.tbDataPre.setItem(i,0,QTableWidgetItem(str(int(data_latih[i,0])))) # membaca parameter NIM
                for j in range(4):
                    k = j + 1
                    self.sgui.tbDataPre.setItem(i,k,QTableWidgetItem(str(data_latih[i,k]))) # membaca paramater input latih x1-x18
                for l in range(4, 18):
                    k = l + 1
                    self.sgui.tbDataPre.setItem(i,k,QTableWidgetItem(str(int(data_latih[i,k])))) # membaca paramater input latih x1-x18
                self.sgui.tbDataPre.setItem(i,19,QTableWidgetItem(str(data_latih[i,19]))) # membaca parameter target(IPK)
            self.statData = 1;
            self.sgui.pbUji.setChecked(False)
            self.sgui.glistdata.setTitle("Tabel Data Latih")

            self.sgui.lbdata.setText(str(f"Jumlah Data: {n_datalatih}"))
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
            cur.close()
            data_uji = np.array(alda) # simpan data kedalam bentuk list/array
            n_datauji = len(data_uji)

            # menampilkan data latih pada tabel
            self.sgui.tbDataPre.setRowCount(0)
            self.sgui.tbDataPre.setRowCount(n_datauji)
            for i in range(n_datauji):
                self.sgui.tbDataPre.setItem(i,0,QTableWidgetItem(str(int(data_uji[i,0])))) # membaca parameter NIM
                for j in range(4):
                    k = j + 1
                    self.sgui.tbDataPre.setItem(i,k,QTableWidgetItem(str(data_uji[i,k]))) # membaca paramater input latih x1-x18
                for l in range(4, 18):
                    k = l + 1
                    self.sgui.tbDataPre.setItem(i,k,QTableWidgetItem(str(int(data_uji[i,k])))) # membaca paramater input latih x1-x18
                self.sgui.tbDataPre.setItem(i,19,QTableWidgetItem(str(data_uji[i,19]))) # membaca parameter target(IPK)
            self.statData = 2;
            self.sgui.pbLatih.setChecked(False)
            self.sgui.glistdata.setTitle("Tabel Data Uji")

            self.sgui.lbdata.setText(str(f"Jumlah Data: {n_datauji}"))
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
                    cur.execute(f"SELECT * FROM data_latih WHERE NIM = {lnim}")
                    idd = cur.fetchall()
                    cur.close()
                    idds = len(idd)
                    if idds > 0:
                        print("NIM sudah ada di dalam database!")
                        msg = QMessageBox()
                        msg.setWindowTitle("Proses Dibatalakan!")
                        msg.setText("Proses tambah data dibatalkan, karena NIM sudah terdaftar di database!")
                        msg.setIcon(QMessageBox.Critical)
                        msg.exec_()
                    else:
                        cur = self.madb.cursor()
                        cur.execute("INSERT INTO data_latih (NIM, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, ipk) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(lnim, lx1, lx2, lx3, lx4, lx5, lx6, lx7, lx8, lx9, lx10, lx11, lx12, lx13, lx14, lx15, lx16, lx17, lx18, lipk,))
                        self.madb.commit()
                        cur.close()
                        print(f"Berhasil Menambahkan data latih {lnim}")
                        self.bacaDataLatih()
                elif statData == 2:
                    cur = self.madb.cursor()
                    cur.execute(f"SELECT * FROM data_uji WHERE NIM = {lnim}")
                    idd = cur.fetchall()
                    cur.close()
                    idds = len(idd)
                    if idds > 0:
                        print("NIM sudah ada di dalam database!")
                        msg = QMessageBox()
                        msg.setWindowTitle("Proses Dibatalakan!")
                        msg.setText("Proses tambah data dibatalkan, karena NIM sudah terdaftar di database!")
                        msg.setIcon(QMessageBox.Critical)
                        msg.exec_()
                    else:
                        cur = self.madb.cursor()
                        cur.execute("INSERT INTO data_uji (NIM, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, ipk) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",(lnim, lx1, lx2, lx3, lx4, lx5, lx6, lx7, lx8, lx9, lx10, lx11, lx12, lx13, lx14, lx15, lx16, lx17, lx18, lipk,))
                        self.madb.commit()
                        cur.close()
                        print(f"Berhasil Menambahkan data uji {lnim}")
                        self.bacaDataUji()
                else:
                    print("Error")
            else:
                print("Error")
                msg = QMessageBox()
                msg.setWindowTitle("Proses Dibatalakan!")
                msg.setText("Proses Tambah dibatalkan! Harap isi semua form input!")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
            
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
            
            lnim = lx1 = lx2 = lx3 = lx4 = lx5 = lx6 = lx7 = lx8 = lx9 = lx10 = lx11 = lx12 = lx13 = lx14 = lx15 = lx16 = lx17 = lx18 = lipk = None
        except:
            print(f'Terjadi kesalahan pada proses pembacaan data baris-{sys.exc_info()[-1].tb_lineno}:\n{sys.exc_info()}')

    def bersihkanInputan(self):
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
            cur.close()
            print(cur.rowcount, f"Data berhasil menambahkan data {teks} dari file!")

            if statData == 1:
                self.bacaDataLatih()
            elif statData == 2:
                self.bacaDataUji()
            else:
                print("Error")
            
            path = namafile = data = dataa = in_data = cur = sqll = vall = None

        except:
            print(f'Terjadi kesalahan pada proses pembacaan data baris-{sys.exc_info()[-1].tb_lineno}:\n{sys.exc_info()[1]}')

    def hapusSatu(self):
        try:
            statData = self.statData
            fnim = self.sgui.leNIM.text()
            if fnim != "":
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
                msg.setWindowTitle(f"Konfirmasi Penghapusan Data {fnim}")
                msg.setText(f"Apakah Anda Yakin Menghapus Data {fnim}?")
                msg.setStandardButtons(QMessageBox.Ok|QMessageBox.Cancel)
                msg.setIcon(QMessageBox.Information)
                msg.buttonClicked.connect(self.popupButton)
                x = msg.exec_()

                if self.statKonf == "OK":
                    print(f"Berhasil Menghapus Data {fnim}")
                    if tb == "data_latih":
                        cura = self.madb.cursor()
                        cura.execute(f"DELETE FROM data_latih WHERE NIM = {fnim}")
                        self.madb.commit()
                        cura.close()
                    elif tb == "data_uji":
                        cura = self.madb.cursor()
                        cura.execute(f"DELETE FROM data_uji WHERE NIM = {fnim}")
                        self.madb.commit()
                        cura.close()
                    else:
                        print("error")

                    if statData == 1:
                        self.bacaDataLatih()
                    elif statData == 2:
                        self.bacaDataUji()
                    else:
                        print("Error")
                else:
                    print(f"Tidak Jadi Menghapus Data {fnim}")
            else:
                msg = QMessageBox()
                msg.setWindowTitle("Proses Dibatalakan!")
                msg.setText("Proses hapus dibatalkan! Harap isi terlebih dahulu form NIM dengan data yang akan dihapus!")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
        except:
            print(f'Terjadi kesalahan pada proses pembacaan data baris-{sys.exc_info()[-1].tb_lineno}:\n{sys.exc_info()}')

    def ubahData(self):
        try:
            statData = self.statData
            fnim = self.sgui.leNIM.text()
            fx1 = self.sgui.leX1.text()
            fx2 = self.sgui.leX2.text()
            fx3 = self.sgui.leX3.text()
            fx4 = self.sgui.leX4.text()
            fx5 = self.sgui.leX5.text()
            fx6 = self.sgui.leX6.text()
            fx7 = self.sgui.leX7.text()
            fx8 = self.sgui.leX8.text()
            fx9 = self.sgui.leX9.text()
            fx10 = self.sgui.leX10.text()
            fx11 = self.sgui.leX11.text()
            fx12 = self.sgui.leX12.text()
            fx13 = self.sgui.leX13.text()
            fx14 = self.sgui.leX14.text()
            fx15 = self.sgui.leX15.text()
            fx16 = self.sgui.leX16.text()
            fx17 = self.sgui.leX17.text()
            fx18 = self.sgui.leX18.text()
            fipk = self.sgui.leIPK.text()
            
            if fnim != "":
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
                msg.setWindowTitle(f"Konfirmasi Pengubahan Data {fnim}")
                msg.setText(f"Apakah Anda Yakin Mengubah Data {fnim}?")
                msg.setStandardButtons(QMessageBox.Ok|QMessageBox.Cancel)
                msg.setIcon(QMessageBox.Information)
                msg.buttonClicked.connect(self.popupButton)
                x = msg.exec_()

                if self.statKonf == "OK":
                    print(f"Berhasil Mengubah Data {fnim}")
                    if tb == "data_latih":
                        cura = self.madb.cursor()
                        cura.execute(f"UPDATE data_latih set x1 = {fx1}, x2 = {fx2}, x3 = {fx3}, x4 = {fx4}, x5 = {fx5}, x6 = {fx6}, x7 = {fx7}, x8 = {fx8}, x9 = {fx9}, x10 = {fx10}, x11 = {fx11}, x12 = {fx12}, x13 = {fx13}, x14 = {fx14}, x15 = {fx15}, x16 = {fx16}, x17 = {fx17}, x18 = {fx18}, ipk = {fipk} WHERE NIM = {fnim}")
                        self.madb.commit()
                        cura.close()
                    elif tb == "data_uji":
                        cura = self.madb.cursor()
                        cura.execute(f"UPDATE data_uji set x1 = {fx1}, x2 = {fx2}, x3 = {fx3}, x4 = {fx4}, x5 = {fx5}, x6 = {fx6}, x7 = {fx7}, x8 = {fx8}, x9 = {fx9}, x10 = {fx10}, x11 = {fx11}, x12 = {fx12}, x13 = {fx13}, x14 = {fx14}, x15 = {fx15}, x16 = {fx16}, x17 = {fx17}, x18 = {fx18}, ipk = {fipk} WHERE NIM = {fnim}")
                        self.madb.commit()
                        cura.close()
                    else:
                        print("error")

                    if statData == 1:
                        self.bacaDataLatih()
                    elif statData == 2:
                        self.bacaDataUji()
                    else:
                        print("Error")
                else:
                    print(f"Tidak Jadi Mengubah Data {fnim}")

            else:
                msg = QMessageBox()
                msg.setWindowTitle("Proses Dibatalakan!")
                msg.setText("Proses hapus dibatalkan! Harap isi terlebih dahulu form NIM dengan data yang akan dihapus!")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()

            fnim = fx1 = fx2 = fx3 = fx4 = fx5 = fx6 = fx7 = fx8 = fx9 = fx10 = fx11 = fx12 = fx13 = fx14 = fx15 = fx16 = fx17 = fx18 = fipk = None
        except:
            print(f'Terjadi kesalahan pada proses pembacaan data baris-{sys.exc_info()[-1].tb_lineno}:\n{sys.exc_info()}')

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
                print(f"Berhasil Menghapus Semua Data {judul}")
                if tb == "data_latih":
                    cura = self.madb.cursor()
                    cura.execute("TRUNCATE TABLE data_latih")
                    cura.close()
                elif tb == "data_uji":
                    cura = self.madb.cursor()
                    cura.execute("TRUNCATE TABLE data_uji")
                    cura.close()
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
        self.madb.close()
        self.close()

class FormPrediksi(QMainWindow):

    # menciptakan objek dari kelas JST
    jst = JaringanSyarafTiruan()
    pre = DPreparation()
    tra = DTransformation()

    def __init__(self):
        QMainWindow.__init__(self)
        self.sgui = gui_prediksi.Ui_MainWindow()
        self.sgui.setupUi(self)
        self.setWindowTitle("(JST BACKPROPAGATION) Prediksi IPK Mahasiswa Sistem Komputer S1 - Menu Prediksi")
        kontrolDB.konek(self) #panggil fungsi koneksi server

        #setup status bar
        self.sgui.statusbarr = QStatusBar()
        self.setStatusBar(self.sgui.statusbarr)
        self.sgui.statusbarr.setStyleSheet('background-color: #FFFFFF;')

        self.sgui.lstatus = QLabel()
        self.sgui.lstatus.setText(self.statSer)
        
        self.sgui.statusbarr.addWidget(self.sgui.lstatus)

        self.madb.close()

        header = self.sgui.tbPrediksi.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)

        header2 = self.sgui.tbDataPre.horizontalHeader()
        for i in range(5):
            header2.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeToContents)
        for i in range(5, 19):
            header2.setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

        np.set_printoptions(suppress=True, linewidth=np.inf)
        self.bentukAwal = np.zeros((1,19))
        self.hasilArray = self.bentukAwal

        self.sgui.pbTambah.clicked.connect(self.tambahData)
        self.sgui.pbTmbFile.clicked.connect(self.tambahDataFile)
        self.sgui.pbHapus.clicked.connect(self.hapusSemuaData)
        self.sgui.pbProPre.clicked.connect(self.mulaiPrediksi)
        self.sgui.pbKembali.clicked.connect(self.Kembali)
        self.statData = 0
        self.show()
    
    
    def bacaData(self):
        try:
            dataPrediksi = self.hasilArray
            banyakData = len(dataPrediksi)
            
            self.sgui.tbDataPre.setRowCount(banyakData)
            for i in range(banyakData):
                self.sgui.tbDataPre.setItem(i,0,QTableWidgetItem(str(int(dataPrediksi[i,0])))) # membaca parameter NIM
                for j in range(4):
                    k = j + 1
                    self.sgui.tbDataPre.setItem(i,k,QTableWidgetItem(str(dataPrediksi[i,k]))) # membaca paramater input latih x1-x18
                for l in range(4, 18):
                    k = l + 1
                    self.sgui.tbDataPre.setItem(i,k,QTableWidgetItem(str(int(dataPrediksi[i,k])))) # membaca paramater input latih x1-x18
        except:
            print(f'Terjadi kesalahan pada proses pembacaan data baris-{sys.exc_info()[-1].tb_lineno}:\n{sys.exc_info()}')
    
    def tambahData(self):
        try:
            lnim = self.sgui.leKey.text()
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

            if lnim != "" and lx1 != "" and lx2 != "" and lx3 != "" and lx4 != "" and lx5 != "" and lx6 != "" and lx7 != "" and lx8 != "" and lx9 != "" and lx10 != "" and lx11 != "" and lx12 != "" and lx13 != "" and lx14 != "" and lx15 != "" and lx16 != "" and lx17 != "" and lx18 != "":
                tmbhArray = np.zeros((1,19))
                tempe = self.hasilArray

                tmbhArray[0,0] = int(lnim)
                tmbhArray[0,1] = lx1
                tmbhArray[0,2] = lx2
                tmbhArray[0,3] = lx3
                tmbhArray[0,4] = lx4
                tmbhArray[0,5] = lx5
                tmbhArray[0,6] = lx6
                tmbhArray[0,7] = lx7
                tmbhArray[0,8] = lx8
                tmbhArray[0,9] = lx9
                tmbhArray[0,10] = lx10
                tmbhArray[0,11] = lx11
                tmbhArray[0,12] = lx12
                tmbhArray[0,13] = lx13
                tmbhArray[0,14] = lx14
                tmbhArray[0,15] = lx15
                tmbhArray[0,16] = lx16
                tmbhArray[0,17] = lx17
                tmbhArray[0,18] = lx18

                if tempe[0,0] != 0 :
                    self.hasilArray = np.vstack((tempe, tmbhArray))
                    self.bacaData()
                else:
                    self.hasilArray = tmbhArray
                    self.bacaData()
            else:
                print("Error")
                msg = QMessageBox()
                msg.setWindowTitle("Proses Dibatalakan!")
                msg.setText("Proses Tambah dibatalkan! Harap isi semua form input!")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
            
            self.sgui.leKey.setText("")
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
            
            lnim = lx1 = lx2 = lx3 = lx4 = lx5 = lx6 = lx7 = lx8 = lx9 = lx10 = lx11 = lx12 = lx13 = lx14 = lx15 = lx16 = lx17 = lx18 = None
            self.statData = 1
        except:
            print(f'Terjadi kesalahan pada proses pembacaan data baris-{sys.exc_info()[-1].tb_lineno}:\n{sys.exc_info()}')

    def tambahDataFile(self):
        try:
            tempe = self.hasilArray
            path = QFileDialog.getOpenFileName(self, f'Silahkan pilih file data prediksi!', '', "XLSX files (*.xlsx)")
            namafile = path[0]
            data = pd.read_excel(namafile, header=1)
            dataA = np.array(data) # simpan data kedalam bentuk list/array
            dataPre = np.around(dataA,2)
            if tempe[0,0] != 0 :
                self.hasilArray = np.vstack((tempe, dataPre))
                self.bacaData()
            else:
                self.hasilArray = dataPre
                self.bacaData()
            self.statData = 1
        except:
            print(f'Terjadi kesalahan pada proses pembacaan data baris-{sys.exc_info()[-1].tb_lineno}:\n{sys.exc_info()}')

    def hapusSemuaData(self):
        try:
            msg = QMessageBox()
            msg.setWindowTitle(f"Konfirmasi Penghapusan Semua Data")
            msg.setText(f"Apakah Anda Yakin Menghapus Semua Data?")
            msg.setStandardButtons(QMessageBox.Ok|QMessageBox.Cancel)
            msg.setIcon(QMessageBox.Information)
            msg.buttonClicked.connect(self.popupButton)
            x = msg.exec_()
            if self.statKonf == "OK":
                banyakData = len(self.hasilArray)
                banyakData = banyakData - 1
                kosong = np.zeros((1,19))
                for i in range(banyakData, 0, -1):
                    self.hasilArray = np.delete(self.hasilArray, (i), axis=0)
                for i in range(19):
                    kosong[0,i] = 0
                self.hasilArray = kosong
                print(self.hasilArray)
                self.sgui.tbDataPre.setRowCount(0)
                self.sgui.tbPrediksi.setRowCount(0)
            else:
                print("Tidak Jadi Menghapus Semua Data")
        except:
            print(f'Terjadi kesalahan pada proses pembacaan data baris-{sys.exc_info()[-1].tb_lineno}:\n{sys.exc_info()}')

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

        # menggabungkan data-data normalisasi menjadi dataset
        data_normalisasi = np.concatenate((x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18), axis=1)
                
        return data_normalisasi

    def mulaiPrediksi(self):
        
        try:
            # mengambil variabel parrent
            statData = self.statData
            dataPrediksi = self.hasilArray

            if statData == 1:
                kontrolDB.konek(self)
                cur = self.madb.cursor()
                cur.execute("SELECT n1 FROM tb_bobotv")
                biasv = cur.fetchall()
                cur.close()
                lbiasv = len(biasv)
                cur = self.madb.cursor()
                cur.execute("SELECT n1 FROM tb_bobotw")
                biasw = cur.fetchall()
                cur.close()
                lbiasw = len(biasw)
                if lbiasv == 0 and lbiasw == 0 :
                    biasv = ""
                    biasw = ""
                    # menampilkan pesan error
                    msg = QMessageBox()
                    msg.setWindowTitle("Proses Dibatalkan")
                    msg.setText("Bobot di database kosong!")
                    msg.setIcon(QMessageBox.Warning)
                    x = msg.exec_()
                else:
                    cur = self.madb.cursor()
                    cur.execute("SELECT ninput, nhidden, noutput FROM tb_params WHERE id = '1'")
                    prm = cur.fetchall()
                    cur.close()
                    n_input = prm[0][0]
                    n_hidden = prm[0][1]
                    n_output = prm[0][2]
                    
                    cur = self.madb.cursor()
                    cur.execute("SELECT * FROM tb_bobotv")
                    aldav = cur.fetchall()
                    cur.close()
                    v = np.array(aldav)

                    cur = self.madb.cursor()
                    cur.execute("SELECT * FROM tb_bobotw")
                    aldaw = cur.fetchall()
                    cur.close()
                    w = np.array(aldaw)

                    cur = self.madb.cursor()
                    cur.execute("SELECT * FROM data_latih")
                    aldalatih = cur.fetchall()
                    cur.close()
                    data_latih = np.array(aldalatih)
                    #print(data_latih)
                    dataipk = data_latih[:,19]
                    datamax = max(dataipk)
                    datamin = min(dataipk)
                    data_latih = np.delete(data_latih, (19), axis=1)
                    badalatih = len(data_latih)
                    dataGabung = np.concatenate((data_latih, dataPrediksi))

                    totalDataPrediksi = len(dataPrediksi)
                    
                    dataGabung_normalisasi = self.Pronor(dataGabung)
                    dataUji_normalisasi = dataGabung_normalisasi[badalatih:,:]

                    # memetakan array/matriks/list
                    hasil_prediksi = np.zeros((totalDataPrediksi, 1))
                    hslprediksi_denormalisasi = np.zeros((totalDataPrediksi,1))

                    # melakukan proses feedforward atau prediksi
                    for j in range(totalDataPrediksi):
                        [z, y] = self.jst.Feedforward(dataUji_normalisasi[j,:], v, w, n_hidden, n_output)
                        hasil_prediksi[j,0] = y[0,0]
                    
                    # proses denormalisasi
                    for i in range(totalDataPrediksi):
                        hslprediksi_denormalisasi[i,0] = self.tra.Denormalisasi(hasil_prediksi[i,0], datamin, datamax)
                    
                    responsi = self.responsi(dataPrediksi, hslprediksi_denormalisasi)
                    self.sgui.tbPrediksi.setRowCount(totalDataPrediksi)
                    for i in range(totalDataPrediksi):
                        hasiljst = hslprediksi_denormalisasi[i,0]

                        # menampilkan hasil ke dalam tabel
                        self.sgui.tbPrediksi.setItem(i,0,QTableWidgetItem(str(int(dataPrediksi[i,0]))))
                        self.sgui.tbPrediksi.setItem(i,1,QTableWidgetItem(str(round(hasiljst, 2))))
                        self.sgui.tbPrediksi.setItem(i,2,QTableWidgetItem(str(responsi[i])))
                    self.statData = 2
                self.madb.close()
            else:
                # menampilkan pesan error
                msg = QMessageBox()
                msg.setWindowTitle("Proses Dibatalkan !")
                msg.setText("Masukan Data Input Terlebih Dahulu!")
                msg.setIcon(QMessageBox.Warning)
                x = msg.exec_()
        except:
            print(f'Terjadi kesalahan pada proses pembacaan data baris-{sys.exc_info()[-1].tb_lineno}:\n{sys.exc_info()}')

    def responsi(self, dataPrediksi, hslprediksi_denormalisasi):
        try:
            badata = len(dataPrediksi)
            print(badata)
            bapred = len(hslprediksi_denormalisasi)
            print(bapred)
            responsi = []
            for i in range(badata):
                rresp = "Berdasarkan hasil prediksi, "
                x1 = dataPrediksi[i,1]
                x2 = dataPrediksi[i,2]
                x3 = dataPrediksi[i,3]
                x4 = dataPrediksi[i,4]
                x5 = dataPrediksi[i,5]
                x6 = dataPrediksi[i,6]
                x7 = dataPrediksi[i,7]
                x8 = dataPrediksi[i,8]
                x9 = dataPrediksi[i,9]
                x10 = dataPrediksi[i,10]
                x11 = dataPrediksi[i,11]
                x12 = dataPrediksi[i,12]
                x13 = dataPrediksi[i,13]
                x14 = dataPrediksi[i,14]
                x15 = dataPrediksi[i,15]
                x16 = dataPrediksi[i,16]
                x17 = dataPrediksi[i,17]
                x18 = dataPrediksi[i,18]
                preIPK = hslprediksi_denormalisasi[i,0]
                if preIPK >= 2.75 :
                    if x1 >= 2.75 and x2 >= 2.75 and x3 >= 2.75 and x4 >= 2.75 :
                        if x5 <= 1 or x6 <= 1 or x7 <= 1 or x8 <= 1 or x9 <= 1 or x10 <= 1 or x11 <= 1 or x12 <= 1 or x13 <= 1 or x14 <= 1 or x15 <= 1 or x16 <= 1 or x17 <= 1 or x18 <= 1 :
                            rresp += "mahasiswa mengalami sedikit masalah akademik dan diharuskan untuk mengulang matakuliah "
                            rresp2 = self.listResp(x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18)
                            rresp += rresp2
                            rresp2 = ""
                            #print(rresp)
                        else:
                            rresp += "mahasiswa tidak mengalami masalah akademik."
                            #print(rresp)
                    else:
                        if x5 <= 1 or x6 <= 1 or x7 <= 1 or x8 <= 1 or x9 <= 1 or x10 <= 1 or x11 <= 1 or x12 <= 1 or x13 <= 1 or x14 <= 1 or x15 <= 1 or x16 <= 1 or x17 <= 1 or x18 <= 1 :
                            rresp += "mahasiswa mengalami masalah akademik dan diharuskan untuk mengulang matakuliah "
                            rresp2 = self.listResp(x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18)
                            rresp += rresp2
                            rresp2 = ""
                            #print(rresp)
                        else:
                            rresp += "mahasiswa sedikit mengalami masalah akademik."
                            #print(rresp)
                else:
                    if x5 <= 1 or x6 <= 1 or x7 <= 1 or x8 <= 1 or x9 <= 1 or x10 <= 1 or x11 <= 1 or x12 <= 1 or x13 <= 1 or x14 <= 1 or x15 <= 1 or x16 <= 1 or x17 <= 1 or x18 <= 1 :
                        rresp += "mahasiswa mengalami masalah akademik dan diharuskan untuk mengulang matakuliah "
                        rresp2 = self.listResp(x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18)
                        rresp += rresp2
                        rresp2 = ""
                        #print(rresp)
                    else:
                        rresp += "mahasiswa mengalami masalah akademik dan diharuskan untuk memperbaiki nilai matkuliah yang dirasa kurang."
                        #print(rresp)
                        
                responsi.append(rresp)
                rresp = ""
            print(responsi[18])
            return responsi
        except:
            print(f'Terjadi kesalahan pada proses pembacaan data baris-{sys.exc_info()[-1].tb_lineno}:\n{sys.exc_info()}')

    def listResp(self, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18):
        rresp = ""
        statt = 0
        if x5 <= 1 :
            rresp += "Fisika 1"
            statt = 1
        if x6 <= 1 :
            if statt == 1:
                rresp += ", Matematika 1"
                statt = 1
            else:
                rresp += "Matematika 1"
                statt = 1
        if x7 <= 1 :
            if statt == 1:
                rresp += ", Fisika 2"
                statt = 1
            else:
                rresp += "Fisika 2"
                statt = 1
        if x8 <= 1 :
            if statt == 1:
                rresp += ", Matematika 2"
                statt = 1
            else:
                rresp += "Matematika 2"
                statt = 1
        if x9 <= 1 :
            if statt == 1:
                rresp += ", Algoritma Pemograman"
                statt = 1
            else:
                rresp += "Algoritma Pemograman"
                statt = 1
        if x10 <= 1 :
            if statt == 1:
                rresp += ", Elektronika 1"
                statt = 1
            else:
                rresp += "Elektronika 1"
                statt = 1
        if x11 <= 1 :
            if statt == 1:
                rresp += ", Teori Sistem & Sinyal"
                statt = 1
            else:
                rresp += "Teori Sistem & Sinyal"
                statt = 1
        if x12 <= 1 :
            if statt == 1:
                rresp += ", Organisasi & Arsitektur Komputer 1"
                statt = 1
            else:
                rresp += "Organisasi & Arsitektur Komputer 1"
                statt = 1
        if x13 <= 1 :
            if statt == 1:
                rresp += ", Sistem Digital"
                statt = 1
            else:
                rresp += "Sistem Digital"
                statt = 1
        if x14 <= 1 :
            if statt == 1:
                rresp += ", Elektronika 2"
                statt = 1
            else:
                rresp += "Elektronika 2"
                statt = 1
        if x15 <= 1 :
            if statt == 1:
                rresp += ", Struktur Data"
                statt = 1
            else:
                rresp += "Struktur Data"
                statt = 1
        if x16 <= 1 :
            if statt == 1:
                rresp += ", Matematika Diskrit"
                statt = 1
            else:
                rresp += "Matematika Diskrit"
                statt = 1
        if x17 <= 1 :
            if statt == 1:
                rresp += ", Komunikasi Data"
                statt = 1
            else:
                rresp += "Komunikasi Data"
                statt = 1
        if x18 <= 1 :
            if statt == 1:
                rresp += ", Aljabar Linear"
            else:
                rresp += "Aljabar Linear"
        rresp += "."
        return rresp

    def popupButton(self, i):
        self.statKonf = i.text()
        print(i.text())

    def Kembali(self):
        self.tampilForm = FormMain()
        self.close()

# menjalankan program
if __name__=="__main__":
    app = QApplication(sys.argv)
    w = FormMain()
    sys.exit(app.exec_())
