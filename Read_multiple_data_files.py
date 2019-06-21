import csv
import time
import numpy as np

initial = time.time()

B = 5e-3
RBW = 300

data = {}

for k in range(11):
    for i in range(3):
        with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity calculations\\Fernando\\254_4\\14stJun\\Spectrum_analyzer\\SSA_'
                  + str("{:02d}".format(k+1)) + '_' + str(i+1) + '.csv') as a:

            df = csv.reader(a, delimiter=',')
            df_temp = []
            for row in df:
                #print(row)
                df_temp.append(row)
            df = df_temp[31:]

            for j in range(len(df)):
                df[j] = [np.float(df[j][0]), np.float(df[j][1])]

            data['SSA_' + str(k + 1) + '_exp_' + str(i + 1)] = np.reshape(np.array(df), (-1, 2))

        data['SSA_' + str(k+1) + '_exp_' + str(i+1)] = np.array(df)
data['SSA_2_exp_1'] = data['SSA_2_exp_1'][:, 0:2]
data['SSA_8_exp_1'] = data['SSA_8_exp_1'][:, 0:2]
#print(data)

Bmin_ref = np.zeros(11)


for k in range(11):
    SNR = []
    mean = np.mean(data['SSA_' + str(k + 1) + '_exp_3'][370:440, 1])
    for row in range(751):
        #c = float(data['SSA_' + str(k + 1) + '_exp_2'][row, 1]) - float(data['SSA_' + str(k + 1) + '_exp_3'][row, 1])
        c = float(data['SSA_' + str(k + 1) + '_exp_2'][row, 1]) - mean
        SNR.append(c)
    data['SNR' + str(k + 1)] = np.array(SNR)

    Bmin_ref[k] = np.divide(B,(np.sqrt(data['SNR' + str(k + 1)][370:440].max()*RBW)))

#print(Bmin_ref)

for k in range(13):
    with open('C:\\Users\\uqfgotar\\Documents\\Magnetometry\\Sensitivity calculations\\Fernando\\254_4\\14stJun\\Network_analyzer\\TRACE'
              + str("{:02d}".format(k+1)) + '.csv') as a:

        df = csv.reader(a, delimiter=',')
        df_temp = []

        for row in df:
            #print(row)
            df_temp.append(row)
        df = df_temp[3:]

        for j in range(len(df)):
            df[j] = [np.float(df[j][0]), np.float(df[j][1])]

        data['TRACE' + str(k + 1)] = np.reshape(np.array(df), (-1, 2))

Bmin = []

for k in range(13):

    for row in range(751):
        c = float(data['TRACE' + str(k + 1)][row, 1]) - float(data['TRACE13'][row, 1])
        #c = float(data['SSA_' + str(k + 1) + '_exp_2'][row, 1]) - mean
        SNR.append(c)
    data['SNR' + str(k + 1)] = np.array(SNR)

Bmin_ref[k] = np.divide(B, (np.sqrt(data['SNR' + str(k + 1)][370:440].max() * RBW)))

#print(data['TRACE1'].shape)


final = time.time()