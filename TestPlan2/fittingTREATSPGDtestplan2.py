# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 19:36:15 2018

@author: Jacob Miske
"""


#Fitting Test Plan 2 SPGDs from TREAT nuclear reactor at Idaho National Labs

#necessary libraries
import numpy as np
#import pandas as pd
import scipy
from scipy import signal
#import matplotlib
import matplotlib.pyplot as plt

#read a txt
CEA_txt_file = r"Test_Plan_2_2018_1.txt"

#Running read commands on txt files
CEA_txt = open(CEA_txt_file, "r")

CEA_file_string = CEA_txt.read()
#create list of strings demarkated by commas
CEA_file_list = CEA_file_string.split(' ')


CEA1 = []; CEA2 = [];
#Pull CEA1 values
counter=0
for i in CEA_file_list:
    counter+=1
    if counter%3==0:
        CEA1.insert(counter, i)   
#Pull CEA2 values
listCounter=0
for i in CEA_file_list:
    if listCounter%3==0:
        CEA2.insert(listCounter, i)
    listCounter+=1
listCounter=0
for j in CEA2:
    CEA2[listCounter] = j[:-8]
    listCounter+=1
CEA2.pop(0); CEA2.pop(); CEA1.pop();        
CEA2 = CEA2[0:200000]; CEA1 = CEA1[0:200000]; #trim unnecessary data (500,000 pieces) of the end

print(len(CEA1))
ranger = len(CEA1)
xRange = range(ranger)

plt.plot(xRange, CEA1, 'red', label='CEA 1')
plt.plot(xRange, CEA2, 'orange', label='CEA 2')
plt.title('CEA SPGD Raw Detector Data Plan 2')
plt.xlabel('Data Points'); plt.ylabel('Picoamperes'); plt.legend()
plt.savefig('CEA TP2 Raw Data.svg')
plt.grid()
plt.show()



savGolCEA1 = scipy.signal.savgol_filter(CEA1, 31, 7)
savGolCEA2 = scipy.signal.savgol_filter(CEA2, 31, 7)

plt.plot(xRange, savGolCEA1, 'red', label='CEA 1')
plt.plot(xRange, savGolCEA2, 'orange', label='CEA 2')
plt.title('CEA SPGD Filtered Detector Data Plan 2')
plt.xlabel('Data Points'); plt.ylabel('Picoamperes'); plt.legend()
plt.savefig('CEA TP2 Filtered Data.svg')
plt.grid()
plt.show()




#Retain a version without mapping them to kilowatt values
picoampsC1 = CEA1
picoampsC2 = CEA2
#picoampsI1 = I1
#picoampsI2 = I2
#Get values for linear mapping functions
picoampsC1 = np.array(picoampsC1).astype(np.float)
picoampsC2 = np.array(picoampsC2).astype(np.float)
meanC120kW = np.mean(picoampsC1[3800:3900])
meanC220kW = np.mean(picoampsC2[3800:3900])
#meanI120kW = np.mean(picoampsI1[5500:5600])
#meanI220kW = np.mean(picoampsI2[5500:5600])
meanC160kW = np.mean(picoampsC1[9900:10000])
meanC260kW = np.mean(picoampsC2[9900:10000])
#meanI160kW = np.mean(picoampsI1[9800:9900])
#meanI260kW = np.mean(picoampsI2[9800:9900])
#meanAllFour20kW = np.mean([meanC120kW,meanC220kW,meanI120kW,meanI220kW] )
#meanAllFour60kW = np.mean([meanC160kW,meanC260kW,meanI160kW,meanI260kW] )

#### Try plot after picoamp means determined

### Lineup SPGD all together
nXaxis = range(1500)

##Plot out mapC1
plt.plot(nXaxis, picoampsC1[0:1500], color='red', label='CEA 1')
##Plot out mapC2
plt.plot(nXaxis, picoampsC2[0:1500], color='orange', label='CEA 2')
###Plot out mapI1
#plt.plot(nXaxis, picoampsI1[0:15000], color='teal')
###Plot out mapI2
#plt.plot(nXaxis, picoampsI2[0:15000], color='purple')
plt.title('SPGD Detectors TP2 Testing Lineup In PicoAmps ')
plt.xlabel('seconds')
plt.ylabel('Picoamps '); plt.legend()
plt.savefig("Rx Power TP2 Lineup SPGD In PicoAmps.svg")
plt.savefig("Rx Power TP2 Lineup SPGD In PicoAmps.png")
plt.grid()
plt.show()



#Useful for taking picoampere measures from SPGD to power measures
#for INL detectors, 60kW happans at max. INL1, 20kW, around 1.4e-9 and INL2, 20kW, around 6.77e-10
#For CEA1, 20kW around 2.18e-9. For CEA2, 20kW around 1.87e-9 
#def SPGDmapperINL1(List, minList, maxList):
#    for i in range(len(List)):
#        List[i] = ((List[i]-meanI120kW)*(60- 20)/(meanI160kW-(meanI120kW)))+20
#    return List
#def SPGDmapperINL2(List, minList, maxList):
#    for i in range(len(List)):
#        List[i] = ((List[i]-meanI220kW)*(60- 20)/(meanI260kW-(meanI220kW)))+20
#    return List
def SPGDmapperCEA1(List):
    for i in range(len(List)):
        List[i] = ((List[i]-meanC120kW)*(60- 20)/(meanC160kW-(meanC120kW)))+20
    return List
def SPGDmapperCEA2(List):
    for i in range(len(List)):
        List[i] = ((List[i]-meanC220kW)*(60- 20)/(meanC260kW-(meanC220kW)))+20
    return List




mapC1 = SPGDmapperCEA1(picoampsC1)    
mapC2 = SPGDmapperCEA2(picoampsC2)    



xAxis = range(20000)

##Plot out mapC1
plt.plot(xAxis, mapC1[0:20000], color='red', label='CEA 1')
##Plot out mapC2
plt.plot(xAxis, mapC2[0:20000], color='orange', label='CEA 2')
###Plot out mapI1
#plt.plot(xAxis, mapI1[0:19000], color='teal')
###Plot out mapI2
#plt.plot(xAxis, mapI2[0:19000], color='purple')
plt.title('SPGD Detectors TP2 Testing Lineup Post Map '); plt.legend()
plt.xlabel('seconds')
plt.ylabel('Kilowatts ')
plt.grid()
plt.savefig("Rx Power TP2 Lineup SPGD Post Map.svg")
plt.show()

xAxis2500 = range(3000)

### Sectioning on Proper Fitting
###Section 1
##Plot out mapC1
plt.plot(xAxis2500, mapC1[0:3000], color='red',linewidth=0.3)
##Plot out mapC2
plt.plot(xAxis2500, mapC2[0:3000], color='orange',linewidth=0.3)
###Plot out mapI1
#plt.plot(xAxis2500, mapI1[0:25000], color='teal',linewidth=0.3)
###Plot out mapI2
#plt.plot(xAxis2500, mapI2[0:25000], color='purple', linewidth=0.3)
plt.title('SPGD Detectors TP2 Testing S1 Lineup Post Map ')
plt.xlabel('seconds')
plt.ylabel('Kilowatts ')
plt.grid()
plt.savefig("Rx Power S1 TP2 Lineup SPGD Post Map.svg")
plt.show()
###Section 2
##Plot out mapC1
plt.plot(xAxis2500, mapC1[3000:6000], color='red',linewidth=0.3)
##Plot out mapC2
plt.plot(xAxis2500, mapC2[3000:6000], color='orange',linewidth=0.3)
###Plot out mapI1
#plt.plot(xAxis2500, mapI1[25000:50000], color='teal',linewidth=0.3)
###Plot out mapI2
#plt.plot(xAxis2500, mapI2[25000:50000], color='purple', linewidth=0.3)
plt.title('SPGD Detectors TP2 Testing S2 Lineup Post Map ')
plt.xlabel('seconds')
plt.ylabel('Kilowatts ')
plt.grid()
plt.savefig("Rx Power S2 TP2 Lineup SPGD Post Map.svg")
plt.show()
###Section 3
##Plot out mapC1
plt.plot(xAxis2500, mapC1[6000:9000], color='red',linewidth=0.3)
##Plot out mapC2
plt.plot(xAxis2500, mapC2[6000:9000], color='orange',linewidth=0.3)
###Plot out mapI1
#plt.plot(xAxis2500, mapI1[5000:7500], color='teal',linewidth=0.3)
###Plot out mapI2
#plt.plot(xAxis2500, mapI2[5000:7500], color='purple',linewidth=0.3)
plt.title('SPGD Detectors TP2 Testing S3 Lineup Post Map ')
plt.xlabel('seconds')
plt.ylabel('Kilowatts ')
plt.grid()
plt.savefig("Rx Power S3 TP2 Lineup SPGD Post Map.svg")
plt.show()
###Section 4
##Plot out mapC1
plt.plot(xAxis2500, mapC1[9000:12000], color='red',linewidth=0.3)
##Plot out mapC2
plt.plot(xAxis2500, mapC2[9000:12000], color='orange',linewidth=0.3)
###Plot out mapI1
#plt.plot(xAxis2500, mapI1[75000:100000], color='teal',linewidth=0.3)
###Plot out mapI2
#plt.plot(xAxis2500, mapI2[75000:100000], color='purple', linewidth=0.3)
plt.title('SPGD Detectors TP2 Testing S4 Lineup Post Map ')
plt.xlabel('seconds')
plt.ylabel('Kilowatts ')
plt.grid()
plt.savefig("Rx Power S4 TP2 Lineup SPGD Post Map.svg")
plt.show()
###Section 5
##Plot out mapC1
plt.plot(xAxis2500, mapC1[12000:15000], color='red',linewidth=0.3)
##Plot out mapC2
plt.plot(xAxis2500, mapC2[12000:15000], color='orange',linewidth=0.3)
###Plot out mapI1
#plt.plot(xAxis2500, mapI1[10000:12500], color='teal', linewidth=0.3)
###Plot out mapI2
#plt.plot(xAxis2500, mapI2[10000:12500], color='purple',linewidth=0.3)
plt.title('SPGD Detectors TP2 Testing S5 Lineup Post Map ')
plt.xlabel('seconds')
plt.ylabel('Kilowatts ')
plt.grid()
plt.savefig("Rx Power S5 TP2 Lineup SPGD Post Map.svg")
plt.show()
###Section 6
##Plot out mapC1
plt.plot(xAxis2500, mapC1[15000:18000], color='red', linewidth=0.3)
##Plot out mapC2
plt.plot(xAxis2500, mapC2[15000:18000], color='orange', linewidth=0.3)
###Plot out mapI1
#plt.plot(xAxis2500, mapI1[12500:15000], color='teal', linewidth=0.3)
###Plot out mapI2
#plt.plot(xAxis2500, mapI2[12500:15000], color='purple', linewidth=0.3)
plt.title('SPGD Detectors TP2 Testing S6 Lineup Post Map ')
plt.xlabel('seconds')
plt.ylabel('Kilowatts ')
plt.grid()
plt.savefig("Rx Power S6 TP2 Lineup SPGD Post Map.svg")
plt.show()
###Section 7
##Plot out mapC1
plt.plot(range(2000), mapC1[18000:20000], color='red', linewidth=0.3)
##Plot out mapC2
plt.plot(range(2000), mapC2[18000:20000], color='orange', linewidth=0.3)
###Plot out mapI1
#plt.plot(range(4000), mapI1[15000:19000], color='teal', linewidth=0.3)
###Plot out mapI2
#plt.plot(range(4000), mapI2[15000:19000], color='purple',linewidth=0.3)
plt.title('SPGD Detectors TP2 Testing S7 Lineup Post Map ')
plt.xlabel('seconds')
plt.ylabel('Kilowatts ')
plt.grid()
plt.savefig("Rx Power S7 TP2 Lineup SPGD Post Map.svg")
plt.show()
