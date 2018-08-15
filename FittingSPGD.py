# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 16:17:52 2018

@author: Jacob Miske
"""
#         -._.-"""-.-"""-..-"""-.-"""-.-"""-.-"""-.-"""-.-"""-._.-"-'
#         =. _'.    '.    '.     '.    '.    '.    '.    '.    '. -'_
#        .-'.-. \ M   \ I   \  S   \ K   \ E   \     \     \     \'-_.
#         .-'-__.'.___.'.___.'.____.'.___.'.___.'.___.'.___.'.___.'._-.

###

#GENERAL NOTES
#TP4 cut from 11am to 1pm
#Make 7 segments in plot
#4 detectors
#considerer smoothing at first
#3rd order fitting, linear along 10 min gaps
#Maybe fifth order

import numpy as np
import pandas as pd
import scipy
from scipy import signal
import matplotlib
import matplotlib.pyplot as plt
import csv

##################
###For INL Data###
##################

###CSV to TXT###
csv_file = "TREAT2 INL SPDs.csv"
txt_file = "INL SPDs.txt"


text_list = []
with open(csv_file, "r") as my_input_file:
    for line in my_input_file:
        line = line.split(",", 2)
        text_list.append(" ".join(line))

with open(txt_file, "w") as my_output_file:
    my_output_file.write("#1\n")
    my_output_file.write("double({},{})\n".format(len(text_list), 2))
    for line in text_list:
        my_output_file.write("  " + line)
    print('File Successfully written.')


#Reading txt files
CEA_txt_file = r"TP420180124CEA.txt"
INL_txt_file = r"INL SPDs.txt"

#Running read commands on txt files
CEA_txt = open(CEA_txt_file, "r")
INL_txt = open(INL_txt_file, "r")

CEA_file_string = CEA_txt.read()
INL_file_string = INL_txt.read()

CEA_file_list = CEA_file_string.split(' ')
INL_file_list = INL_file_string.split(',')
INL_file_list = INL_file_list[8:]



#Create empty lists to later be populated with str of raw data
CEA_SPGD_1=[]
CEA_SPGD_2=[]

INL_SPGD_1=[]
INL_SPGD_2=[]



#################
######INL DATA###
#################
#looking back, this is fairly inefficient code that could be quickly cleaned up with list trimming
INL_SPGD_1a=[]
INL_SPGD_1b=[]
INL_SPGD_2a=[]
INL_SPGD_2b=[]


counter=0
for i in INL_file_list:
    counter+=1
    if counter%3==0:
        INL_SPGD_1a.insert(counter, i)
    if counter%2==0:
        INL_SPGD_1b.insert(counter, i)

INL_SPGD_2a = INL_file_list[4::6]
INL_SPGD_2b = INL_SPGD_1b[2::3]
#Trimmed to right set
INL_SPGD_1a = INL_SPGD_1a[0::2]
INL_SPGD_1b = INL_SPGD_1b[1::3]
#Remove Dates, curses special character ":"
listCounter=0
for j in INL_SPGD_2b:
    INL_SPGD_2b[listCounter] = j[:-41]
    listCounter+=1
    #print(j)

INL_SPGD_1a.pop()
INL_SPGD_1b.pop()
INL_SPGD_2a.pop()
INL_SPGD_2b.pop()


###Floating Point INL Data
normINL=[]
fINL_SPGD_1a=[]
fINL_SPGD_2a=[]
fINL_SPGD_1b=[]
fINL_SPGD_2b=[]


for i in range(86400):
    #f stands for float
    fINL_SPGD_1a.insert(i, float(INL_SPGD_1a[i]))
    fINL_SPGD_2a.insert(i, float(INL_SPGD_2a[i]))
    fINL_SPGD_1b.insert(i, float(INL_SPGD_1b[i]))
    fINL_SPGD_2b.insert(i, float(INL_SPGD_2b[i]))

fINL_SPGD_1=[]
fINL_SPGD_2=[]
for i in range(86400):
    fINL_SPGD_1.insert(i, abs(fINL_SPGD_1b[i] - fINL_SPGD_1a[i]))
    fINL_SPGD_2.insert(i, abs(fINL_SPGD_2b[i] - fINL_SPGD_2a[i]))

'''
for i in range(86400):
    mean = (fINL_SPGD_1[i]+fINL_SPGD_2[i])/2.0
    normINL.insert(i, mean)
'''

fINL_badItem_1=[]
fINL_badItem_2=[]
for i in range(86400):
    if fINL_SPGD_1[i] >=0.1:
        fINL_badItem_1.append(i)
    if fINL_SPGD_2[i] >=0.1:
        fINL_badItem_2.append(i)

#Removes total outliers     
FixfINL_SPGD_1 = [i for i in fINL_SPGD_1 if i <= 1]
FixfINL_SPGD_2 = [i for i in fINL_SPGD_2 if i <= 1]



###Plotting fINL Fixed, Raw Data###
xAxisINL1 = range(86178)
xAxisINL2 = range(86078)

plt.plot(xAxisINL1, FixfINL_SPGD_1, color='green')
plt.plot(xAxisINL2, FixfINL_SPGD_2, color='blue')
plt.savefig("INL Detector Raw test.svg")
plt.savefig("INL Detector Raw test.png")
plt.title('INL Fixed, Raw SPGDs')
plt.xlabel('seconds')
plt.show()

#Setting active range (time wise)
FixfINL_SPGD_1 = FixfINL_SPGD_1[27122:-40056]
FixfINL_SPGD_2 = FixfINL_SPGD_2[27022:-40056]
#DONT CHANGE, vital for making data line up properly
#This part expands INL detector lists artificially to work well with CEA
ExpdINL1=[]
ExpdINL2=[]
for i in range(19000):
    for j in range(5):
        ExpdINL1.append(FixfINL_SPGD_1)
    for j in range(5):
        ExpdINL2.append(FixfINL_SPGD_2)

xAxisINL1 = range(19000)
xAxisINL2 = range(19000)

plt.plot(xAxisINL1, FixfINL_SPGD_1, color='green')
plt.plot(xAxisINL2, FixfINL_SPGD_2, color='blue')
plt.savefig("INL Detector Raw test.svg")
plt.savefig("INL Detector Raw test.png")
plt.title('INL Fixed, Raw SPGDs 2')
plt.xlabel('seconds')
plt.show()





#################
######CEA DATA###
#################
#Yields CEA SPGD1 data pieces 
#Input is CEA_SPGD_1 empty list, output is populated list
counter=0
for i in CEA_file_list:
    counter+=1
    if counter%3==0:
        CEA_SPGD_1.insert(counter, i)   
#print(CEA_SPGD_1)
 
#Yields CEA SPGD2 data pieces
listCounter=0
for i in CEA_file_list:
    if listCounter%3==0:
        CEA_SPGD_2.insert(listCounter, i)
    listCounter+=1

#Remove Dates, curses special character ":"
listCounter=0
for j in CEA_SPGD_2:
    CEA_SPGD_2[listCounter] = j[:-8]
    listCounter+=1
    #print(j)

#Eliminating bad items in list 2
bad_item = 0
for i in CEA_SPGD_2:
    try: 
        float(i)
    except:
        del CEA_SPGD_2[CEA_SPGD_2.index(i)]

##Final product
CEA2 = CEA_SPGD_2[10:-10]
CEA1 = CEA_SPGD_1[10:-10]

#Provides graph of yielding detector
#Input is CEA_SPGD(s)
#reminder len(CEA1) and len(CEA2) are 102489
xAxisCEA = []
for j in range(102489):
    xAxisCEA.insert(j,j)

#plot CEA_SPGD_1 items
try:
    plt.plot(xAxisCEA, CEA1, color='green')
except:
    print('error')
#plot CEA_SPGD_2
try:
    plt.plot(xAxisCEA, CEA2, color='blue')
except:
    print('error')

plt.ylabel('Detector Output')
plt.title('CEA SPGDs')
plt.show()

###Normalization###
normCEA=[]
fCEA1=[]
fCEA2=[]
for i in range(102489):
    #f stands for float
    fCEA1.insert(i, float(CEA1[i]))
    fCEA2.insert(i, float(CEA2[i]))
for i in range(102489):
    mean = (fCEA1[i]+fCEA2[i])/2.0
    normCEA.insert(i, mean)
    
plt.plot(xAxisCEA, normCEA, color='red')
#n stands for normalized
normCEA1 = []
normCEA2 = []
for i in range(102489):
    normCEA1.insert(i, fCEA1[i] -normCEA[i])
    normCEA2.insert(i, (normCEA[i] - fCEA2[i]))

plt.plot(xAxisCEA, normCEA1, color='black')
#plt.plot(xAxisCEA, normCEA2, color='yellow')
plt.show()




#Taking normCEA1 and normCEA2 and using them to change 
#CEA1 and CEA2
newCEA1=[]
newCEA2=[]
for i in range(102489):
    newCEA1.insert(i, -(normCEA1[i]- fCEA1[i]))
    newCEA2.insert(i, (fCEA2[i] - normCEA2[i]))

plt.plot(xAxisCEA, newCEA1, color='green')
plt.plot(xAxisCEA, newCEA2, color='blue')
plt.savefig("CEA Detector Raw test.svg")
plt.savefig("CEA Detector Raw test.png")
plt.show()





###Moving Average###
#Examing number before and after
MVW = 0.8 #moving average weighting
normfCEA1 = []
normfCEA2 = []
for i in range(102487):
    normfCEA1.insert(i+1, (fCEA1[i]*MVW+fCEA1[i+1]+fCEA1[i+2]*MVW)/(1+2*MVW))
    normfCEA2.insert(i+1, (fCEA2[i]*MVW+fCEA2[i+1]+fCEA2[i+2]*MVW)/(1+2*MVW))
NormxAxisCEA = range(102487)



'''
###Various CEA Plots
plt.plot(xAxisCEA, fCEA1, color='orange')
plt.plot(NormxAxisCEA, normfCEA1, color='teal')
plt.xlabel('seconds')
plt.title('Moving Average Weighted Method Differece')
plt.savefig("Moving Weighted Average.png")
plt.show()

savGolfCEA1 = scipy.signal.savgol_filter(normfCEA1, 13, 4)
savGolfCEA2 = scipy.signal.savgol_filter(normfCEA2, 13, 4)
###Graph Savitzky-Golay###
plt.plot(NormxAxisCEA, savGolfCEA1, color='teal')
plt.plot(NormxAxisCEA, savGolfCEA2, color='blue')
plt.xlabel('seconds')
plt.title('Weak Savitzky-Golay Method CEA test')
plt.savefig("SavitzkyGolayGraph.svg")
plt.savefig("SavitzkyGolayGraph.png")
plt.show()

###Moving Average Graph###
plt.plot(NormxAxisCEA, normfCEA1, color='green')
plt.plot(NormxAxisCEA, normfCEA2, color='purple')
plt.xlabel('seconds')
plt.title('Moving Average test')
plt.savefig("MovingAverageGraph.svg")
plt.savefig("MovingAverageGraph.png")
plt.show()

###Exponential Smoothing###
#take fCEA1 and fCEA2 as input, output exponentially smooth 
#versions of each and plot
a = 0.6#eval(input('Enter Exponential Smoothing Variable (between 0 and 1)  ')); #Exponential smoothing factor, 0 < a < 1 by def
ExpSfCEA1 = []
ExpSfCEA2 = []
for i in range(102489):
    if i == 0:
        ExpSfCEA1.insert(i, fCEA1[i])
        ExpSfCEA2.insert(i, fCEA2[i])
    ExpSfCEA1.insert(i, (a*fCEA1[i-1]+(1-a)*fCEA1[i]))
    ExpSfCEA2.insert(i, (a*fCEA2[i-1]+(1-a)*fCEA2[i]))
    
###Exponential Smoothing Graph###
plt.plot(range(102490), ExpSfCEA1, color='black')
plt.plot(range(102490), ExpSfCEA2, color='brown')
plt.xlabel('seconds')
plt.title('Exp Smooth test')
plt.savefig("Exp Smooth Graph.svg")
plt.savefig("Exp Smooth Graph.png")
plt.show()

###Double Exponential Smoothing###
a = 0.6 #eval(input('Enter Double Exp Alpha Variable  '))
b = 0.6 #eval(input('Enter Double Exp Trend Variable  '))
CEA1_A_t = []
CEA1_B_t = []
CEA2_A_t = []
CEA2_B_t = []
DExSfCEA1 = []
DExSfCEA2 = []
for i in range(102489):
    if i == 0:
        DExSfCEA1.insert(i, fCEA1[i])
        DExSfCEA2.insert(i, fCEA2[i])
        CEA1_A_t.insert(i, fCEA1[i])
        CEA2_A_t.insert(i, fCEA2[i])
        CEA1_B_t.insert(i, fCEA1[i])
        CEA2_B_t.insert(i, fCEA2[i])
    CEA1_A_t.insert(i, a*fCEA1[i]+(1-a)*fCEA1[i-1])
    CEA2_A_t.insert(i, a*fCEA2[i]+(1-a)*fCEA2[i-1])
    CEA1_B_t.insert(i, b*(CEA1_A_t[i] - CEA1_A_t[i-1])+(1-b)*fCEA1[i-1])
    CEA2_B_t.insert(i, b*(CEA1_A_t[i] - CEA1_A_t[i-1])+(1-b)*fCEA2[i-1])
    DExSfCEA1.insert(i, CEA1_A_t[i]+CEA1_B_t[i])
    DExSfCEA2.insert(i, CEA2_A_t[i]+CEA2_B_t[i])

###Double Exponential Smoothing Graph###
plt.plot(range(102490), DExSfCEA1, color='black')
plt.plot(range(102490), DExSfCEA2, color='brown')
plt.xlabel('seconds')
plt.title('Double Exp Smooth test')
plt.savefig("Double Exp Smooth Graph.svg")
plt.savefig("Double Exp Smooth Graph.png")
plt.show()
'''

##################################
######CEA & INL DATA###TOGETHER###
##################################

#Idea to trim CEA lists to 19000 items, so same 'n' for all
#Initially, fCEAx is 102489
FixfCEA1=[]
FixfCEA2=[]

counter=0
for i in range(102489):
    if counter==5:
        FixfCEA1.append(fCEA1[i])
        FixfCEA2.append(fCEA2[i])
        counter=0
    counter+=1
FixfCEA1 = FixfCEA1[0:-1497]
FixfCEA2 = FixfCEA2[0:-1497]

#Time to plot them on each other to figure where they are
xAxis=range(19000)
'''
plt.plot(xAxis, FixfCEA1, color='red')
plt.plot(xAxis, FixfCEA2, color='orange')
plt.plot(xAxis, FixfINL_SPGD_1, color='teal')
plt.plot(xAxis, FixfINL_SPGD_2, color='purple')
plt.title('Four Detectors')
plt.xlabel('seconds')
plt.ylabel('Four Detector Output Raw')
plt.show()
'''

###Normalization of all detectors
#Just a guess that gets them close enough to make predictions and analysis on the graphs
multNorm = 2.2
for i in range(19000):
    FixfINL_SPGD_1[i]=FixfINL_SPGD_1[i]*multNorm
    FixfINL_SPGD_2[i]=FixfINL_SPGD_2[i]*multNorm

#Simple name for INL
FixfINL1 = FixfINL_SPGD_1
FixfINL2 = FixfINL_SPGD_2

##Ploting normalization
#plt.plot(xAxis, FixfCEA1, color='red')
#plt.plot(xAxis, FixfCEA2, color='orange')
#plt.plot(xAxis, FixfINL_SPGD_1, color='teal')
#plt.plot(xAxis, FixfINL_SPGD_2, color='purple')
#plt.title('Four Detectors Normalized')
#plt.xlabel('seconds')
#plt.ylabel('Detector Output ')
#plt.show()

###Filtering all detectors
#Savitzky-Golay
savGolfINL1 = scipy.signal.savgol_filter(FixfINL_SPGD_1, 23, 6)
savGolfINL2 = scipy.signal.savgol_filter(FixfINL_SPGD_2, 23, 6)
savGolfCEA1 = scipy.signal.savgol_filter(FixfCEA1, 23, 4)
savGolfCEA2 = scipy.signal.savgol_filter(FixfCEA2, 23, 4)


#plt.plot(xAxis, savGolfCEA1, color='red')
#plt.plot(xAxis, savGolfCEA2, color='orange')
#plt.plot(xAxis, savGolfINL1, color='teal')
#plt.plot(xAxis, savGolfINL2, color='purple')
#plt.title('Savitzky-Golay, Four Detectors Normalized')
#plt.xlabel('seconds')
#plt.ylabel('Detector Output ')
#plt.savefig("Savitzky-Golay, four detectors normalized.svg")
#plt.savefig("Savitzky-Golay, four detectors normalized.png")
#plt.show()


##################################
######CEA & INL DATA###Sectioned###
##################################
FixfCEA1_1=FixfCEA1[2500:5000]
FixfCEA1_2=FixfCEA1[5000:7500]
FixfCEA1_3=FixfCEA1[7500:10000]
FixfCEA1_4=FixfCEA1[10000:12500]
FixfCEA1_5=FixfCEA1[12500:15000]
FixfCEA1_6=FixfCEA1[15000:17500]

FixfCEA1_7=FixfCEA1[17500:19000]


FixfCEA2_1=FixfCEA2[2500:5000]
FixfCEA2_2=FixfCEA2[5000:7500]
FixfCEA2_3=FixfCEA2[7500:10000]
FixfCEA2_4=FixfCEA2[10000:12500]
FixfCEA2_5=FixfCEA2[12500:15000]
FixfCEA2_6=FixfCEA2[15000:17500]

FixfCEA2_7=FixfCEA2[17500:19000]


FixfINL1_1=FixfINL1[2500:5000]
FixfINL1_2=FixfINL1[5000:7500]
FixfINL1_3=FixfINL1[7500:10000]
FixfINL1_4=FixfINL1[10000:12500]
FixfINL1_5=FixfINL1[12500:15000]
FixfINL1_6=FixfINL1[15000:17500]

FixfINL1_7=FixfINL1[17500:19000]


FixfINL2_1=FixfINL2[2500:5000]
FixfINL2_2=FixfINL2[5000:7500]
FixfINL2_3=FixfINL2[7500:10000]
FixfINL2_4=FixfINL2[10000:12500]
FixfINL2_5=FixfINL2[12500:15000]
FixfINL2_6=FixfINL2[15000:17500]

FixfINL2_7=FixfINL2[17500:19000]


###Plotting sections
xAxis2500=range(2500)


#Section 1
plt.plot(xAxis2500, FixfCEA1_1, color='red')
plt.plot(xAxis2500, FixfCEA2_1, color='orange')
plt.plot(xAxis2500, FixfINL1_1, color='teal')
plt.plot(xAxis2500, FixfINL2_1, color='purple')
plt.title('S1, four detectors raw')
plt.xlabel('seconds')
plt.ylabel('Detector Output ')
plt.savefig("S1, raw data.svg")
plt.savefig("S1, raw data.png")
plt.show()

#Section 2
plt.plot(xAxis2500, FixfCEA1_2, color='red')
plt.plot(xAxis2500, FixfCEA2_2, color='orange')
plt.plot(xAxis2500, FixfINL1_2, color='teal')
plt.plot(xAxis2500, FixfINL2_2, color='purple')
plt.title('S2, four detectors raw')
plt.xlabel('seconds')
plt.ylabel('Detector Output ')
plt.savefig("S2, raw data.svg")
plt.savefig("S2, raw data.png")
plt.show()

#Section 3
plt.plot(xAxis2500, FixfCEA1_3, color='red')
plt.plot(xAxis2500, FixfCEA2_3, color='orange')
plt.plot(xAxis2500, FixfINL1_3, color='teal')
plt.plot(xAxis2500, FixfINL2_3, color='purple')
plt.title('S3, four detectors raw')
plt.xlabel('seconds')
plt.ylabel('Detector Output ')
plt.savefig("S3, raw data.svg")
plt.savefig("S3, raw data.png")
plt.show()

#Section 4
plt.plot(xAxis2500, FixfCEA1_4, color='red')
plt.plot(xAxis2500, FixfCEA2_4, color='orange')
plt.plot(xAxis2500, FixfINL1_4, color='teal')
plt.plot(xAxis2500, FixfINL2_4, color='purple')
plt.title('S4, four detectors raw')
plt.xlabel('seconds')
plt.ylabel('Detector Output ')
plt.savefig("S4, raw data.svg")
plt.savefig("S4, raw data.png")
plt.show()

#Section 5
plt.plot(xAxis2500, FixfCEA1_5, color='red')
plt.plot(xAxis2500, FixfCEA2_5, color='orange')
plt.plot(xAxis2500, FixfINL1_5, color='teal')
plt.plot(xAxis2500, FixfINL2_5, color='purple')
plt.title('S5, four detectors raw')
plt.xlabel('seconds')
plt.ylabel('Detector Output ')
plt.savefig("S5, raw data.svg")
plt.savefig("S5, raw data.png")
plt.show()

#Section 6
plt.plot(xAxis2500, FixfCEA1_6, color='red')
plt.plot(xAxis2500, FixfCEA2_6, color='orange')
plt.plot(xAxis2500, FixfINL1_6, color='teal')
plt.plot(xAxis2500, FixfINL2_6, color='purple')
plt.title('S6, four detectors raw')
plt.xlabel('seconds')
plt.ylabel('Detector Output ')
plt.savefig("S6, raw data.svg")
plt.savefig("S6, raw data.png")
plt.show()

###Plotting sav-gol sections for comparison

#Section 1
savGolfINL1_1 = scipy.signal.savgol_filter(FixfINL1_1, 23, 6)
savGolfINL2_1 = scipy.signal.savgol_filter(FixfINL2_1, 23, 6)
savGolfCEA1_1 = scipy.signal.savgol_filter(FixfCEA1_1, 23, 6)
savGolfCEA2_1 = scipy.signal.savgol_filter(FixfCEA2_1, 23, 6)
plt.plot(xAxis2500, savGolfCEA1_1, color='red', label='CEA1')
plt.plot(xAxis2500, savGolfCEA2_1, color='orange', label='CEA2')
plt.plot(xAxis2500, savGolfINL1_1, color='teal', label='INL1')
plt.plot(xAxis2500, savGolfINL2_1, color='purple', label='INL2')
plt.title('Section 1, SG, Four Detectors Normalized')
plt.xlabel('seconds')
plt.ylabel('Detector Output ')
plt.savefig("S1, SG, four detectors normalized.svg")
plt.savefig("S1, SG, four detectors normalized.png")
plt.legend(loc='upper left')
plt.show()

#Section 2
savGolfINL1_2 = scipy.signal.savgol_filter(FixfINL1_2, 23, 6)
savGolfINL2_2 = scipy.signal.savgol_filter(FixfINL2_2, 23, 6)
savGolfCEA1_2 = scipy.signal.savgol_filter(FixfCEA1_2, 23, 6)
savGolfCEA2_2 = scipy.signal.savgol_filter(FixfCEA2_2, 23, 6)
plt.plot(xAxis2500, savGolfCEA1_2, color='red', label='CEA1')
plt.plot(xAxis2500, savGolfCEA2_2, color='orange', label='CEA2')
plt.plot(xAxis2500, savGolfINL1_2, color='teal', label='INL1')
plt.plot(xAxis2500, savGolfINL2_2, color='purple', label='INL2')
plt.title('Section 2, SG, Four Detectors Normalized')
plt.xlabel('seconds')
plt.ylabel('Detector Output ')
plt.savefig("S2, SG, four detectors normalized.svg")
plt.savefig("S2, SG, four detectors normalized.png")
plt.legend(loc='upper left')
plt.show()

#Section 3
savGolfINL1_3 = scipy.signal.savgol_filter(FixfINL1_3, 23, 6)
savGolfINL2_3 = scipy.signal.savgol_filter(FixfINL2_3, 23, 6)
savGolfCEA1_3 = scipy.signal.savgol_filter(FixfCEA1_3, 23, 6)
savGolfCEA2_3 = scipy.signal.savgol_filter(FixfCEA2_3, 23, 6)
plt.plot(xAxis2500, savGolfCEA1_3, color='red', label='CEA1')
plt.plot(xAxis2500, savGolfCEA2_3, color='orange', label='CEA2')
plt.plot(xAxis2500, savGolfINL1_3, color='teal', label='INL1')
plt.plot(xAxis2500, savGolfINL2_3, color='purple', label='INL2')
plt.title('Section 3, SG, Four Detectors Normalized')
plt.xlabel('seconds')
plt.ylabel('Detector Output ')
plt.savefig("S3, SG, four detectors normalized.svg")
plt.savefig("S3, SG, four detectors normalized.png")
plt.legend(loc='upper left')
plt.show()

#Section 4
savGolfINL1_4 = scipy.signal.savgol_filter(FixfINL1_4, 23, 6)
savGolfINL2_4 = scipy.signal.savgol_filter(FixfINL2_4, 23, 6)
savGolfCEA1_4 = scipy.signal.savgol_filter(FixfCEA1_4, 23, 6)
savGolfCEA2_4 = scipy.signal.savgol_filter(FixfCEA2_4, 23, 6)
plt.plot(xAxis2500, savGolfCEA1_4, color='red', label='CEA1')
plt.plot(xAxis2500, savGolfCEA2_4, color='orange', label='CEA2')
plt.plot(xAxis2500, savGolfINL1_4, color='teal', label='INL1')
plt.plot(xAxis2500, savGolfINL2_4, color='purple', label='INL2')
plt.title('Section 4, SG, Four Detectors Normalized')
plt.xlabel('seconds')
plt.ylabel('Detector Output ')
plt.savefig("S4, SG, four detectors normalized.svg")
plt.savefig("S4, SG, four detectors normalized.png")
plt.legend(loc='upper left')
plt.show()

#Section 5
savGolfINL1_5 = scipy.signal.savgol_filter(FixfINL1_5, 23, 6)
savGolfINL2_5 = scipy.signal.savgol_filter(FixfINL2_5, 23, 6)
savGolfCEA1_5 = scipy.signal.savgol_filter(FixfCEA1_5, 23, 6)
savGolfCEA2_5 = scipy.signal.savgol_filter(FixfCEA2_5, 23, 6)
plt.plot(xAxis2500, savGolfCEA1_5, color='red', label='CEA1')
plt.plot(xAxis2500, savGolfCEA2_5, color='orange', label='CEA2')
plt.plot(xAxis2500, savGolfINL1_5, color='teal', label='INL1')
plt.plot(xAxis2500, savGolfINL2_5, color='purple', label='INL2')
plt.title('Section 5, SG, Four Detectors Normalized')
plt.xlabel('seconds')
plt.ylabel('Detector Output ')
plt.savefig("S5, SG, four detectors normalized.svg")
plt.savefig("S5, SG, four detectors normalized.png")
plt.legend(loc='upper left')
plt.show()

#Section 6
savGolfINL1_6 = scipy.signal.savgol_filter(FixfINL1_6, 23, 6)
savGolfINL2_6 = scipy.signal.savgol_filter(FixfINL2_6, 23, 6)
savGolfCEA1_6 = scipy.signal.savgol_filter(FixfCEA1_6, 23, 6)
savGolfCEA2_6 = scipy.signal.savgol_filter(FixfCEA2_6, 23, 6)
plt.plot(xAxis2500, savGolfCEA1_6, color='red', label='CEA1')
plt.plot(xAxis2500, savGolfCEA2_6, color='orange', label='CEA2')
plt.plot(xAxis2500, savGolfINL1_6, color='teal', label='INL1')
plt.plot(xAxis2500, savGolfINL2_6, color='purple', label='INL2')
plt.title('Section 6, SG, Four Detectors Normalized')
plt.xlabel('seconds')
plt.ylabel('Detector Output ')
plt.savefig("S6, SG, four detectors normalized.svg")
plt.savefig("S6, SG, four detectors normalized.png")
plt.legend(loc='upper left')
plt.show()



######
###Plot for arbitrary unit of 'Reactor Power' ###Interesting Bit
######
#Very peak power is 60kW, ~2.2e-9 on CEA detectors == 20 kW


C1 = FixfCEA1
C2 = FixfCEA2
I1 = FixfINL1
I2 = FixfINL2

#Plot simplied lists
plt.plot(xAxis, C1, color='red')
plt.plot(xAxis, C2, color='orange')
plt.plot(xAxis, I1, color='teal')
plt.plot(xAxis, I2, color='purple')
plt.title(' Four Detectors ')
plt.xlabel('seconds')
plt.ylabel('Detector Output ')
plt.savefig("Four Detectors.svg")
plt.savefig("Four Detectors.png")
plt.show()

#Getting far values of C and I
maxC1=max(C1)
maxC2=max(C2)
maxI1=max(I1)
maxI2=max(I2)

minC1=min(C1)
minC2=min(C2)
minI1=min(I1)
minI2=min(I2)

print('maxC1 ' + str(maxC1))
print('maxC2 ' + str(maxC2))
print('maxI1 ' + str(maxI1))
print('maxI2 ' + str(maxI2))

#Useful for taking picoampere measures from SPGD to power measures
def SPGDmapper(i, List):
    ListMax = max(List)
    #ListMedian = (max(List)+min(List))/2
    ##60kW at Max, ~20kW at Median
    return i*(60/ListMax)
    
PowerC1 = map(SPGDmapper, C1)
    

###Citations###
# https://www.solver.com/smoothing-techniques

