import csv
import time
import numpy as np

initial = time.time()

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
            data['SSA_' + str(k+1) + '_exp_' + str(i+1)] = np.array(df, dtype=object)
data['SSA_2_exp_1'] = data['SSA_2_exp_1'][:,0:2]
data['SSA_8_exp_1'] = data['SSA_8_exp_1'][:,0:2]

sum = []
for row in range(751):
    c = float(data['SSA_1_exp_1'][row,1]) + float(data['SSA_3_exp_1'][row,1])
    sum = np.insert(sum,row, c)
sum = sum.reshape(751,1)
#     print(c)
#print(sum)
final = time.time()