import sys
import time
import numpy as np
import pandas as pd
import mysql.connector as mycon
from mysql.connector import *

class CRUD:
    def __init__(self):
        self.konek()
        self.selectOne()
        #self.savee()
        #self.bacaSemua()

    def konek(self):
        try:
            madb = mycon.connect(host="localhost", user="root", password="", database="gpa_bnn")
            self.madbb = madb
            if madb.is_connected():
                db_info = madb.get_server_info()
                self.statSer = f"Connected to Server MySQL v.{db_info}"
        except Error as error:
            self.statSer = f"Failed Connect to Server MySQL error({error})"
        print(self.statSer)
    
    def savee(self):
        cur = self.madbb.cursor()
        
        np.set_printoptions(suppress=True, linewidth=np.inf) #agar nilai tidak bernotasi scientific
        data_latih = pd.read_excel("D:\Learn programs\python\TA\dataset\DataVal.xlsx") #membaca data dari file csv
        data_latih = np.array(data_latih) #mengubah menjadi array
        datallatih = data_latih.tolist()
        print(datallatih,"\n")
        dataLatih = np.asarray(datallatih)
        print(dataLatih,"\n")
        print(data_latih)
        dbs = len(data_latih)
        sqll = "INSERT INTO data_uji (NIM, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, ipk) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        vall = datallatih
        cur.executemany(sqll, vall)
        self.madbb.commit()
        print(cur.rowcount, "was inserted.")
    
    def selectOne(self):
        cur = self.madbb.cursor()
        cur.execute("SELECT n1 FROM tb_bobotv")
        ids = (cur.fetchone())
        print(ids)
        print()
    
    def bacaSemua(self):
        cur = self.madbb.cursor()
        cur.execute("SELECT * FROM data_latih")
        alda = cur.fetchall()
        np.set_printoptions(suppress=True, linewidth=np.inf)
        dataa = np.array(alda)
        print(dataa)

CRUD()