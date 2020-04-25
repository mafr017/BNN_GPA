import numpy as np
from JST import JaringanSyarafTiruan, DPreparation, DTransformation
from matplotlib import pyplot as plt
import pandas as pd
np.set_printoptions(suppress=True, linewidth=np.inf)

#menciptakan objek dari kelas JST
jst = JaringanSyarafTiruan()
pre = DPreparation()
tra = DTransformation()

#pendefinisian proses mulai normalisasi
def Pronor(data):
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
  x1  = tra.Normalisasi(x1)
  x2  = tra.Normalisasi(x2)
  x3  = tra.Normalisasi(x3)
  x4  = tra.Normalisasi(x4)
  x5  = tra.Normalisasi(x5)
  x6  = tra.Normalisasi(x6)
  x7  = tra.Normalisasi(x7)
  x8  = tra.Normalisasi(x8)
  x9  = tra.Normalisasi(x9)
  x10 = tra.Normalisasi(x10)
  x11 = tra.Normalisasi(x11)
  x12 = tra.Normalisasi(x12)
  x13 = tra.Normalisasi(x13)
  x14 = tra.Normalisasi(x14)
  x15 = tra.Normalisasi(x15)
  x16 = tra.Normalisasi(x16)
  x17 = tra.Normalisasi(x17)
  x18 = tra.Normalisasi(x18)
  ipk = tra.Normalisasi(ipk)

  #menggabungkan data-data normalisasi menjadi dataset
  data_normalisasi = np.concatenate((x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, ipk), axis=1)
        
  return data_normalisasi, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, ipk

#inisialisasi parameter-parameter JST
n_input   = 18
n_hidden  = 15
n_output  = 1
alpha     = 0.5
min_error = 0.0001
iterasi   = 1

#import data latih dan data training
np.set_printoptions(suppress=True, linewidth=np.inf) #agar nilai tidak bernotasi scientific
data_latih = pd.read_csv('dataset/DataLat.csv', sep=',') #membaca data dari file csv
data_latih = np.array(data_latih) #mengubah menjadi array
"""
#inisialisasi data latih
data_latih = np.array([
[10200011,  2.37,   2.25,   1.85,   2.47,   1,  2,  2,  2,  3,  2,  2,  3,  2,  2,  2,  2,  4,  2,  2.34],
[10200015,  2.68,   2.1,    2.5,    2.53,   1,  3,  1,  2,  2,  3,  2,  2,  3,  3,  3,  2,  2,  2,  2.65],
[10200016,  2.32,   1.85,   2.5,    2.32,   2,  1,  1,  1,  1,  2,  2,  4,  2,  2,  2,  2,  3,  2,  2.41],
[10200017,  2.53,   2.11,   1.84,   1.89,   1,  2,  2,  2,  3,  2,  1,  2,  2,  1,  2,  2,  2,  3,  2.47],
[10200027,  2.63,   2.05,   2.05,   2.16,   2,  2,  2,  1,  2,  2,  2,  2,  2,  2,  2,  2,  3,  2,  2.37],
[10200030,  3.00,   3.56,   3.32,   3.37,   2,  3,  4,  3,  3,  3,  4,  4,  3,  3,  4,  3,  4,  4,  3.4],
[10200033,  3.32,   3.28,   3.68,   4,      2,  3,  4,  3,  4,  4,  4,  4,  4,  4,  4,  2,  4,  4,  3.55],
[10200044,  2.58,   2.45,   2.4,    2.11,   2,  2,  2,  2,  3,  2,  3,  4,  1,  2,  2,  2,  3,  2,  2.31],
[10200054,  2.79,   2.85,   3.6,    3.53,   2,  2,  4,  2,  3,  4,  4,  4,  4,  4,  3,  2,  4,  3,  3.12],
[10200070,  2.79,   2.39,   2.37,   2.89,   2,  3,  3,  2,  2,  3,  2,  2,  4,  3,  3,  3,  4,  2,  2.75]])
"""
data = data_latih

#inisialisasi awal bobot V dan bobot W
v = np.array([
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

w = np.array([[0.3], [0.2], [-0.3], [-0.4], [0.3], [0.2], [0.1], [-0.2], [0.3], [0.4], [-0.3], [-0.2], [0.1], [0.2], [0.3], [-0.4]])

#menentukan jumlah data latih dan data uji
total_data  = len(data)
n_datalatih = total_data

#menentukan data latih dan target output
data_normalisasi, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, x14, x15, x16, x17, x18, ipk = Pronor(data)

input_latih       = data_normalisasi[:, 0:18]
target_output     = data_normalisasi[:, 18]


#program dimulai
print ('------------------------------------------------------------------------------------------------------------')
print ('                                Parameter JST Backpropagation                                               ')
print ('------------------------------------------------------------------------------------------------------------')
print ()
print (f"Neuron Input                : {n_input}")
print (f"Neuron Hidden               : {n_hidden}")
print (f"Neuron Output               : {n_output}")
print (f"Laju Pembelajaran (alpha)   : {alpha}")
print (f"Minimum Error               : {min_error:6f}")
print (f"Iterasi                     : {iterasi}")
print()
print ('Data Latih : ')
print (input_latih)
print()
""" print ('Target Output : ')
print (target_output)
print() """
print ('Bobot V : ')
print (v)
print()
print ('Bobot W : ')
print (w)
print()

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
print ('------------------------------------------------------------------------------------------------------------')
print ('                                PROSES PELATIHAN                                                            ')
error = np.zeros((n_datalatih,1))
mse = np.zeros((iterasi,1))
jml_iterasi = 0

for i in range (iterasi):
    print ('Iterasi ke-', (i+1))
    for j in range(n_datalatih):
      #  print ('data ke-',j+1)
        [z, y] = jst.Feedforward(input_latih[j,:], v, w, n_hidden, n_output)
        [w, v] = jst.Backpropagation(target_output[j], y, input_latih[j,:], alpha, z, w, v)
        error[j,0] = (target_output[j]-y[0,0])**2
      #  print ('target  : ', target_output[j])

      #  print ('Z :')
      #  print (z)
      #  print ('Y       :',y)
      #  print ('error   : {0:0.8f}'.format(float(error[j,0])))
      #  print ()
      #  print ('Bobot W Baru :')
      #  print (w)
      #  print ()
      #  print ('Bobot V Baru :')
      #  print (v)
      #  print ()

    mse[i,0] = round(sum(error[:, 0])/n_datalatih, 7)
    print (f"MSE : {mse[i,0]:0.7f}")

    if mse[i,0] <= min_error:
        jml_iterasi = i+1
        break
    jml_iterasi = i+1

#menampilkan grafik konvergensi proses pelatihan
plt.figure()
plt.plot(mse[0:jml_iterasi, 0])
plt.xlabel('Iterasi ke-i, (0 < i < '+str(jml_iterasi)+')')
plt.ylabel('MSE')
plt.title('Grafik Konvergensi Proses Pelatihan')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------
print()
print ('------------------------------------------------------------------------------------------------------------')
print ('                                PROSES PENGUJIAN                                                            ')
"""
#data pengujian
data_uji = np.array([
[10200085,  3.11,   3.1,    3.18,   2.81,   2,  2,  3,  2,  4,  3,  3,  3,  2,  2,  2,  4,  4,  3,  3.18],
[10200086,  2.84,   2.82,   2.68,   2.42,   2,  2,  3,  2,  3,  3,  2,  3,  2,  2,  2,  4,  4,  2,  2.79],
[10200089,  2.79,   2.35,   2.63,   2.74,   2,  2,  3,  2,  3,  2,  2,  4,  2,  3,  2,  2,  4,  3,  2.73],
[10200093,  3.26,   2.72,   3.21,   3.47,   4,  3,  4,  2,  3,  3,  2,  4,  4,  3,  2,  3,  3,  4,  3.15]])
"""
np.set_printoptions(suppress=True, linewidth=np.inf) #agar nilai tidak bernotasi scientific
data_uji = pd.read_csv('dataset/DataVal.csv', sep=',') #membaca data dari file csv
data_uji = np.array(data_uji) #mengubah menjadi array
print ("Data pengujian :")
print (data_uji)
print()

#mengabungkan data latih dengan data uji
data = np.concatenate((data, data_uji))

#total data pengujian
total_datauji = len(data_uji)
n_datauji = total_datauji

#normalisasi data uji
datauji_normalisasi, x1u, x2u, x3u, x4u, x5u, x6u, x7u, x8u, x9u, x10u, x11u, x12u, x13u, x14u, x15u, x16u, x17u, x18u, ipku = Pronor(data)

input_uji = datauji_normalisasi[n_datalatih:, 0:18]
""" print ("ini input uji:")
print (input_uji) """
output_sebenarnya = datauji_normalisasi[n_datalatih:, 18]

#memetakan array/matriks
hasil_prediksi = np.zeros((n_datauji, 1))
kum_error = np.zeros((n_datauji, 1))

#melakukan proses feedforward atau prediksi
for j in range(n_datauji):
  [z, y] = jst.Feedforward(input_uji[j,:], v, w, n_hidden, n_output)
  hasil_prediksi[j,0] = y[0,0]
""" print ("hasil prediksi :")
print (hasil_prediksi)
print() """

#melakukan denormalisasi hasil prediksi dan data sebenarnya
ipkuji = data[:, 19]
datamax = max(ipkuji)
datamin = min(ipkuji)
""" print ("datamax :")
print (datamax)
print ("datamin :")
print (datamin)
print() """

#memetakan array/matriks
hslprediksi_denormalisasi = np.zeros((n_datauji,1))
outsebenarnya_denormalisasi = np.zeros((n_datauji,1))

#proses denormalisasi
for i in range(n_datauji):
  hslprediksi_denormalisasi[i,0] = tra.Denormalisasi(hasil_prediksi[i,0], datamin, datamax)
  outsebenarnya_denormalisasi[i,0] = tra.Denormalisasi(output_sebenarnya[i], datamin, datamax)

#menampilkan hasil prediksi
print ("Data ke- \t X1 \t X2 \t\t X3 \t\t X4 \t\t X5 \t\t X6 \t X7 \t\t X8 \t X9 \t X10 \t X11 \t X12 \t X13 \t X14 \t X15 \t X16 \t X17 \t X18 \t OutputJST \t Output Sebenarnya \t Error")
for i in range(n_datauji):
  hasiljst = hslprediksi_denormalisasi[i,0]
  datasebenarnya = outsebenarnya_denormalisasi[i,0]
  errorhasil = abs(datasebenarnya-hasiljst)
  errorhasil = round(errorhasil, 6)
  kum_error[i,0] = abs((datasebenarnya-hasiljst)/datasebenarnya)

  print ((i+1), "\t\t", input_uji[i,0], "\t", input_uji[i,1], "\t", input_uji[i,2], "\t", input_uji[i,3], "\t", input_uji[i,4], "\t", input_uji[i,5], "\t", input_uji[i,6], "\t", input_uji[i,7],
    "\t", input_uji[i,8], "\t", input_uji[i,9], "\t", input_uji[i,10], "\t", input_uji[i,11], "\t", input_uji[i,12], "\t", input_uji[i,13], "\t", input_uji[i,14], "\t", input_uji[i,15], "\t",
    input_uji[i,16], "\t", input_uji[i,17], "\t", hasiljst, "\t", datasebenarnya, "\t", errorhasil)

print()

akurasi = 100 - ((sum(kum_error)/n_datauji) * 100) #menghitung MAPE / akurasi
akurasi = float(akurasi[0])
""" print ("kumulasi error :")
print (kum_error) """
print (f"Akurasi prediksi : {akurasi:0.2f} %")

#menampilkan grafik konvergensi proses pengujian
y1 = hslprediksi_denormalisasi
y2 = outsebenarnya_denormalisasi
x_tmp = list(range(1, n_datauji+1))
x = np.array([x_tmp]).transpose()

plt.figure()
plt.plot(x, y1, 'r', x, y2, 'g')
plt.xlabel('Data Uji Ke-i, (0 < i < '+str(n_datauji)+')')
plt.ylabel('Hasil Prediksi')
plt.title('Grafik Perbandingan Hasil Prediksi JST dan Data Sebenarnya')
plt.legend(('Hasil Prediksi JST', 'Data Sebenarnya'), loc='upper right')
#plt.show()