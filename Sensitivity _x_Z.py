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

        data['SSA_' + str(k + 1) + '_exp_' + str(i)] = np.array(df)


Bmin_ref = np.zeros(11)
SN_min = np.zeros(11)
peak = np.zeros(11)
#ind_max = np.zeros(11)

for k in range(11):
    SNR = []
    mean = np.mean(data['SSA_' + str(k + 1) + '_exp_0'][350:440, 1])
    for row in range(751):
        c = float(data['SSA_' + str(k + 1) + '_exp_1'][row, 1]) - mean
        SNR.append(c)

    data['SNR' + str(k + 1)] = np.array(SNR)
    peak[k] = (data['SNR' + str(k + 1)][350:440] + mean).max()
    SN_min = math.pow(10, (data['SNR' + str(k + 1)][350:440].max())/10)
    ind_max = np.where(data['SNR' + str(k + 1)] == peak[k])
    Bmin_ref[k] = np.divide(B, (np.sqrt(SN_min*RBW)))
    data['SNR' + str(k + 1)] = np.power(10, np.divide(data['SNR' + str(k + 1)], 10))
print(peak)


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
for k in range(11):
    Bmin = []
    S21_Snn_ref_ratio[k] = data['TRACE' + str(k + 1)][375, 1]/data['TRACE11'][375, 1]

    for row in range(751):
        c = np.multiply(np.sqrt(np.multiply(np.divide(data['TRACE11'][row, 1],
                        data['TRACE' + str(k + 1)][row, 1]), S21_Snn_ref_ratio[k])), Bmin_ref[k])
        Bmin.append(c)

    for j in range(len(Bmin)):
        Bmin[j] = np.float(Bmin[j])

    data['Bmin' + str(k)] = np.asarray(Bmin)

    data['Bmin_omega' + str(k)] = np.multiply(np.divide(data['Bmin' + str(k)], 1e-12), Bmin_ref[k])

    Bmin_min[k] = np.divide(data['Bmin' + str(k)].min(), 1e-9)

'''Calculus following James matlab program'''
# for k in range(11):
#     data['TRACE' + str(k + 1)][:, 1] = np.power(10, np.divide(data['TRACE' + str(k + 1)][:, 1], 10))
#     data['TRACE' + str(k + 1)][:, 1] = np.divide(data['TRACE' + str(k + 1)][:, 1], data['TRACE' + str(k + 1)][575, 1])
#     data['SSA_' + str(k + 1) + '_exp_0'][:, 1] = np.power(10, np.divide(data['SSA_' + str(k + 1) + '_exp_0'][:, 1], 10))
#     data['SSA_' + str(k + 1) + '_exp_0'][:, 1] = np.divide(data['SSA_' + str(k + 1) + '_exp_0'][:, 1], data['SSA_' + str(k + 1) + '_exp_0'][575, 1])
#
#     S21_Snn_ref_ratio[k] = data['TRACE' + str(k + 1)][375, 1] / data['TRACE11'][375, 1]
#     # print(data['TRACE' + str(k + 1)][375, 1])
#     # print(data['TRACE11'])
#
#     data['Bmin' + str(k + 1)] = np.divide(data['SSA_' + str(k + 1) + '_exp_0'][:, 1], data['TRACE' + str(k + 1)][:, 1])
#     data['Bmin' + str(k + 1)] = np.multiply(data['Bmin' + str(k + 1)], S21_Snn_ref_ratio[k])*0.000234
#     Bmin_min[k] = np.divide(data['Bmin' + str(k + 1)].min(), 1e-9)


height = [20, 50, 80, 110, 140, 200, 260, 360, 500, 1000]
height = np.array(height)

axes = plt.gca()
xmin = data['TRACE1'][:, 0].min()
xmax = data['TRACE1'][:, 0].max()
ymin = data['TRACE1'][:, 1].min()
ymax = data['TRACE10'][:, 1].max()
plt.figure(1)
for k in range(9):
    plt.plot(data['TRACE' + str(k + 1)][:, 0], data['Bmin_omega' + str(k + 1)], label='$\Delta$z = ' + str(height[k]))
    #plt.plot(data['TRACE' + str(k + 1)][:, 0], data['Bmin' + str(k + 1)], label='$\Delta$z = ' + str(height[k]))
plt.xlabel('Frequency (Hz)')
plt.ylabel('Sensitivity ($nT$/$\sqrt{Hz}$)')
axes.set_xlim([(xmin-10000), xmax])
#axes.set_ylim([(ymin), ymax])


plt.figure(2)
plt.plot(height, Bmin_min[:10], 'ro')
plt.yscale('log')
plt.xlabel(r'$\Delta$z ($\mu$m)')
plt.ylabel('Best sensitivity ($nT$/$\sqrt{Hz}$)')

final = time.time()
print('\n' + str(final - initial) + ' seconds')

plt.show()