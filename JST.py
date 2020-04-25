import numpy as np
import sys
from math import *

class DPreparation:
    #pendefinisian fungsi untuk mengacak bobot awal
    def Acakbobot(self, n_input, n_hidden, n_output):
        try:
            '''membuat dimensi matriks bobot input ke hidden --- bobot hidden ke output'''
            bobot_v = np.zeros((n_input+1, n_hidden))
            bobot_w = np.zeros((n_hidden+1, n_output))

            '''membuat nilai random untuk bobot kecuali bias'''
            tmp_v = np.random.rand(n_input, n_hidden)
            tmp_w = np.random.rand(n_hidden, n_output)

            '''bias diberi niali 0,1'''
            bobot_v[0, :]=0.1
            bobot_w[0, :]=0.1

            '''memindahkan array nilai random dari temp ke array bobot'''
            bobot_v[1:n_input+1, :] = tmp_v
            bobot_w[1:n_hidden+1, :] = tmp_w

            return [bobot_v, bobot_w]
        except:
            print('Terjadi kesalahan pada proses pembuatan bobot awal',sys.exc_info()[0])

class DTransformation:
    #pendefinisian fungsi untuk melakukan normalisasi data
    def Normalisasi(self, data):
        try:
            n_data = data.shape[0] #mengetahui ukuran matriks/array
            datamaks = max(data)
            datamin = min(data)
            '''
            x = np.zeros((1, n_data))
            for i in range(n_data):
                x[0, i] = round((data[i]-datamin)/(datamaks-datamin),3)
            '''
            x = np.zeros((n_data, 1)) #memetakan matriks data yang akan digunakan
            for i in range(n_data): #menghitung nilai normalisasi setiap variabel/parameter
                x[i, 0] = round((data[i]-datamin)/(datamaks-datamin), 6)

            return x
        except:
            print ('Terjadi kesalahan pada proses normalisasi data',sys.exc_info()[0])

    #pendefinisian fungsi untuk melakukan denormalisasi data
    def Denormalisasi(self, data, datamin, datamax):
        try:
            x = round(((data*(datamax-datamin))+datamin), 6) #menghitung nilai denormalisasi dari data yang dihasilkan
            return x
        except:
            print('Terjadi kesalahan pada proses denormalisasi data',sys.exc_info()[0])

class JaringanSyarafTiruan:
    #pendefinisian fungsi untuk menghitung feedforward neuron hidden dari input layer
    def input_hidden(self, data, n_hidden, v):
        try:
            n_data = data.shape[0]
            z = np.zeros((1, n_hidden))
            

            for j in range(n_hidden):
                tmp = 0
                for i in range(n_data):
                    tmp = tmp + v[i+1, j]*data[i]
                
                tmp = v[0, j] + tmp
                z[0, j] = round(1/(1+np.exp(-tmp)), 6)

            return z
        except:
            print('Terjadi kesalahan pada proses menghitung feedforward (dari input ke hidden layer)',sys.exc_info()[0])

    #pendefinisian fungsi untuk menghitung feedforward neuron output dari hidden layer
    def hidden_output(self, z, n_output, w):
        try:
            [baris, kolom] = z.shape
            y = np.zeros((1, n_output))
            for k in range(n_output):
                tmp = 0
                for j in range(n_output):
                    tmp = tmp+w[j+1, k]*z[k, j]

                tmp = w[0, k] + tmp
                y[0, k] = round(1/(1+np.exp(-tmp)), 6)

            return y
        except:
            print('Terjadi kesalahan pada proses menghitung feedforward (dari hidden ke output layer)',sys.exc_info()[0])

    #pendefinisian fungsi untuk melakukan feedforward
    def Feedforward(self, data, v, w, n_hidden, n_output):
        try:
            z = self.input_hidden(data, n_hidden, v) #panggil fungsi untuk menghitung feedforward input-hidden
            y = self.hidden_output(z, n_output, w) #panggil fungsi untuk menghitung feedforward hidden-output

            return [z, y]
        except:
            print('Terjadi kesalahan pada proses feedforward',sys.exc_info()[0])
    
    #pendefinisian fungsi untuk menghitung backpropagation pembaruan bobot W
    def output_hidden(self, target_output, y, z, alpha, w):
        try:
            baris, kolom = y.shape
            tarOut = np.zeros((baris, kolom))

            for i in range(baris):
                for j in range(kolom):
                    tarOut[i, j] = (target_output-y[i, j])*y[i, j]*(1-y[i, j])

            baris, kolom = tarOut.shape
            baris1, kolom1 = z.shape
            deltaW = np.zeros((kolom1+1, kolom))

            for i in range(kolom):
                for j in range(kolom1):
                    deltaW[j+1, i] = round(alpha*tarOut[0, i]*z[i, j], 6)

                deltaW[0, i] = round(alpha*tarOut[0, i], 6)
            
            w_baru = w + deltaW

            return w_baru
        except:
            print('Terjadi kesalahan pada proses backpropagation (dari output ke hidden layer)',sys.exc_info()[0])
    
    #pendefinisian fungsi untuk menghitung backpropagation pembaruan bobot V
    def hidden_input(self, target_output, y, data, alpha, z, w, v):
        try:
            baris, kolom = y.shape
            tarOut = np.zeros((baris, kolom))

            for i in range(baris):
                for j in range(kolom):
                    tarOut[i, j] = (target_output-y[i, j])*y[i, j]*(1-y[i, j])

            baris1, kolom1 = w.shape
            baris2, kolom2 = z.shape
            tarOutW = np.zeros((baris2, kolom2))

            for i in range(kolom2):
                tmp = 0
                for j in range(kolom):
                    tmp = round(tmp+tarOut[0, j]*w[i+1, j], 6)

                tarOutW[0, i] = round(tmp*z[0, i]*(1-z[0, i]), 6)
            
            baris, kolom = tarOutW.shape            
            n_data = data.shape[0]
            m, n = v.shape
            deltaV = np.zeros((m, n))

            for j in range(kolom):
                for i in range(n_data):
                    deltaV[i+1, j] = round(alpha*tarOutW[0, j]*data[i], 6)
                
                deltaV[0, j] = round(alpha*tarOutW[0, j], 6)

            v_baru = np.round((v + deltaV), 6)

            return v_baru
        except:
            print('Terjadi kesalahan pada proses backpropagation (dari hidden ke input layer)',sys.exc_info()[0])
        
    #pendefinisian fungsi untuk melakukan backpropagation
    def Backpropagation(self, target_output, y, data, alpha, z, w, v):
        try:
            w_baru = self.output_hidden(target_output, y, z, alpha, w) #panggil fungsi untuk menghitung backpropagation output-hidden
            v_baru = self.hidden_input(target_output, y, data, alpha, z, w, v) #panggil fungsi untuk menghitung backpropagation hidden-input

            return [w_baru, v_baru]
        except:
            print('Terjadi kesalahan pada proses backpropagation',sys.exc_info()[0])