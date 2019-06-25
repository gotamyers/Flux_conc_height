import csv
import math
import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.ticker as mticker

initial = time.time()

B = 5e-4
RBW = 30

data = {}

for k in range(11):
    for i in range(2):
        with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\Fernando\\254_4\\25thJune_ZScan'
                  + '\\Spectrum_analyzer\\SSA_' + str("{:02d}".format(k+1)) + '_' + str(i) + '.csv') as a:

            df = csv.reader(a, delimiter=',')
            df_temp = []
            for row in df:
                df_temp.append(row)
            df = df_temp[31:]

            for j in range(len(df)):
                df[j] = [np.float(df[j][0]), np.float(df[j][1])]

            data['SSA_' + str(k + 1) + '_exp_' + str(i)] = np.reshape(np.array(df), (-1, 2))

        data['SSA_' + str(k+1) + '_exp_' + str(i)] = np.array(df)


Bmin_ref = np.zeros(11)
SN_min = np.zeros(11)

for k in range(11):
    SNR = []
    mean = np.mean(data['SSA_' + str(k + 1) + '_exp_0'][370:440, 1])
    for row in range(751):
        c = float(data['SSA_' + str(k + 1) + '_exp_1'][row, 1]) - mean
        SNR.append(c)

    data['SNR' + str(k + 1)] = np.array(SNR)
    SN_min = math.pow(10,(data['SNR' + str(k + 1)][370:440].max())/10)

    Bmin_ref[k] = np.divide(B, (np.sqrt(SN_min*RBW)))



for k in range(11):
    with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity_calculations\\Fernando\\254_4\\25thJune_ZScan'
              + '\\Network_analyzer\\TRACE' + str("{:02d}".format(k+1)) + '.csv') as a:

        df = csv.reader(a, delimiter=',')
        df_temp = []

        for row in df:
            df_temp.append(row)
        df = df_temp[3:]

        for j in range(len(df)):
            df[j] = [np.float(df[j][0]), np.float(df[j][1])]

        data['TRACE' + str(k + 1)] = np.reshape(np.array(df), (-1, 2))


S21_Snn_ref_ratio = np.zeros(11)
Bmin_min = np.zeros(11)
for k in range(10):
    Bmin = []
    S21_Snn_ref_ratio[k] = data['TRACE' + str(k + 1)][376, 1]/data['TRACE11'][376, 1]

    for row in range(751):
        c = np.multiply(np.sqrt(np.multiply(np.divide(data['TRACE11'][row, 1],
                        data['TRACE' + str(k + 1)][row, 1]), S21_Snn_ref_ratio[k])), Bmin_ref[k])
        Bmin.append(c)

    for j in range(len(Bmin)):
        Bmin[j] = np.float(Bmin[j])

    data['Bmin' + str(k)] = np.asarray(Bmin)

    data['Bmin_omega' + str(k)] = np.multiply(np.divide(data['Bmin' + str(k)], 1e-12), Bmin_ref[k])

    Bmin_min[k] = np.divide(data['Bmin' + str(k)].min(), 1e-6)

height = [30, 60, 90, 150, 210, 270, 470, 670, 1000, 2000, 2400]
height = np.array(height)

axes = plt.gca()
xmin = data['TRACE1'][:, 0].min()
xmax = data['TRACE1'][:, 0].max()
plt.figure(1)
for k in range(10):
    plt.plot(data['TRACE' + str(k + 1)][:,0], data['Bmin_omega' + str(k)], label='$\Delta$z = ' + str(height[k]))
plt.xlabel('Frequency (MHz)')
plt.ylabel('Sensitivity ($\mu$T/$\sqrt{Hz}$)')
axes.set_xlim([(xmin-50000), xmax])


plt.figure(2)
plt.plot(height, Bmin_min, 'ro')
plt.xscale('log')
plt.xlabel(r'$\Delta$z ($\mu$m)')
plt.ylabel('Best sensitivity ($\mu$T/$\sqrt{Hz}$)')

final = time.time()
print('\n' + str(final - initial) + ' seconds')

plt.show()