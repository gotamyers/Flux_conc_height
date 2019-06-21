import csv
import time
import numpy as np

initial = time.time()

data={}

#Obs: file 2_1 and 8_1 bugados
for k in range(11):
    for i in range(3):
        with open('C:\\Users\\Fernando\\Desktop\\14stJun\\SSA_' + str("{:02d}".format(k+1))+ '_' + str(i+1)+ '.csv') as a:
            if k+1!=8 and i+1!=1 or k+1!=2 and i+1!=1:

                df = csv.reader(a, delimiter=',')
                df_temp=[]
                for row in df:
                    df_temp.append(row)
                df=df_temp[31:]

                for j in range(len(df)):
                      df[j] = [np.float(df[j][0]), np.float(df[j][1])]

                data['Height_'+str(k+1)+'_exp_'+str(i+1)]=np.reshape(np.array(df),(-1,2))
            else:
                continue





final = time.time()
total = final - initial
print(total)