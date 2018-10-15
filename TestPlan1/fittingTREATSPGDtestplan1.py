# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 18:04:38 2018

@author: Jacob Miske
"""

#Fitting Test Plan 7 SPGDs from TREAT nuclear reactor at Idaho National Labs

#necessary libraries
import numpy as np
#import pandas as pd
import scipy
from scipy import signal
#import matplotlib
import matplotlib.pyplot as plt

#read a txt
CEA_txt_file = r"Test_Plan_1_2018_1.txt"

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
plt.title('CEA SPGD Raw Detector Data Plan 1')
plt.xlabel('Data Points'); plt.ylabel('Picoamperes'); plt.legend()
plt.savefig('CEA TP1 Raw Data.svg')
plt.grid()
plt.show()



savGolCEA1 = scipy.signal.savgol_filter(CEA1, 11, 5)
savGolCEA2 = scipy.signal.savgol_filter(CEA2, 11, 5)

plt.plot(xRange, savGolCEA1, 'red', label='CEA 1')
plt.plot(xRange, savGolCEA2, 'orange', label='CEA 2')
plt.title('CEA SPGD Filtered Detector Data Plan 1')
plt.xlabel('Data Points'); plt.ylabel('Picoamperes'); plt.legend()
plt.savefig('CEA TP1 Filtered Data.svg')
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
meanC120kW = np.mean(picoampsC1[2000:2100])
meanC220kW = np.mean(picoampsC2[2000:2100])
#meanI120kW = np.mean(picoampsI1[5500:5600])
#meanI220kW = np.mean(picoampsI2[5500:5600])
meanC160kW = np.mean(picoampsC1[4100:4200])
meanC260kW = np.mean(picoampsC2[4100:4200])
#meanI160kW = np.mean(picoampsI1[9800:9900])
#meanI260kW = np.mean(picoampsI2[9800:9900])
#meanAllFour20kW = np.mean([meanC120kW,meanC220kW,meanI120kW,meanI220kW] )
#meanAllFour60kW = np.mean([meanC160kW,meanC260kW,meanI160kW,meanI260kW] )

#### Try plot after picoamp means determined

### Lineup SPGD all together
nXaxis = range(1500)

##Plot out mapC1
plt.plot(nXaxis, picoampsC1[0:1500], color='red')
##Plot out mapC2
plt.plot(nXaxis, picoampsC2[0:1500], color='orange')
###Plot out mapI1
#plt.plot(nXaxis, picoampsI1[0:15000], color='teal')
###Plot out mapI2
#plt.plot(nXaxis, picoampsI2[0:15000], color='purple')
plt.title('SPGD Detectors TP1 Testing Lineup In PicoAmps ')
plt.xlabel('seconds')
plt.ylabel('Picoamps ')
plt.savefig("Rx Power TP1 Lineup SPGD In PicoAmps.svg")
plt.savefig("Rx Power TP1 Lineup SPGD In PicoAmps.png")
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



xAxis = range(8000)

##Plot out mapC1
plt.plot(xAxis, mapC1[0:8000], color='red')
##Plot out mapC2
plt.plot(xAxis, mapC2[0:8000], color='orange')
###Plot out mapI1
#plt.plot(xAxis, mapI1[0:19000], color='teal')
###Plot out mapI2
#plt.plot(xAxis, mapI2[0:19000], color='purple')
plt.title('SPGD Detectors TP1 Testing Lineup Post Map ')
plt.xlabel('seconds')
plt.ylabel('Kilowatts ')
plt.grid()
plt.savefig("Rx Power TP1 Lineup SPGD Post Map.svg")
plt.show()

xAxis2500 = range(1000)

### Sectioning on Proper Fitting
###Section 1
##Plot out mapC1
plt.plot(xAxis2500, mapC1[0:1000], color='red',linewidth=0.3)
##Plot out mapC2
plt.plot(xAxis2500, mapC2[0:1000], color='orange',linewidth=0.3)
###Plot out mapI1
#plt.plot(xAxis2500, mapI1[0:25000], color='teal',linewidth=0.3)
###Plot out mapI2
#plt.plot(xAxis2500, mapI2[0:25000], color='purple', linewidth=0.3)
plt.title('SPGD Detectors TP1 Testing S1 Lineup Post Map ')
plt.xlabel('seconds')
plt.ylabel('Kilowatts ')
plt.grid()
plt.savefig("Rx Power S1 TP1 Lineup SPGD Post Map.svg")
plt.show()
###Section 2
##Plot out mapC1
plt.plot(xAxis2500, mapC1[1000:2000], color='red',linewidth=0.3)
##Plot out mapC2
plt.plot(xAxis2500, mapC2[1000:2000], color='orange',linewidth=0.3)
###Plot out mapI1
#plt.plot(xAxis2500, mapI1[25000:50000], color='teal',linewidth=0.3)
###Plot out mapI2
#plt.plot(xAxis2500, mapI2[25000:50000], color='purple', linewidth=0.3)
plt.title('SPGD Detectors TP1 Testing S2 Lineup Post Map ')
plt.xlabel('seconds')
plt.ylabel('Kilowatts ')
plt.grid()
plt.savefig("Rx Power S2 TP1 Lineup SPGD Post Map.svg")
plt.show()
###Section 3
##Plot out mapC1
plt.plot(xAxis2500, mapC1[2000:3000], color='red',linewidth=0.3)
##Plot out mapC2
plt.plot(xAxis2500, mapC2[2000:3000], color='orange',linewidth=0.3)
###Plot out mapI1
#plt.plot(xAxis2500, mapI1[5000:7500], color='teal',linewidth=0.3)
###Plot out mapI2
#plt.plot(xAxis2500, mapI2[5000:7500], color='purple',linewidth=0.3)
plt.title('SPGD Detectors TP1 Testing S3 Lineup Post Map ')
plt.xlabel('seconds')
plt.ylabel('Kilowatts ')
plt.grid()
plt.savefig("Rx Power S3 TP1 Lineup SPGD Post Map.svg")
plt.show()
###Section 4
##Plot out mapC1
plt.plot(xAxis2500, mapC1[3000:4000], color='red',linewidth=0.3)
##Plot out mapC2
plt.plot(xAxis2500, mapC2[3000:4000], color='orange',linewidth=0.3)
###Plot out mapI1
#plt.plot(xAxis2500, mapI1[75000:100000], color='teal',linewidth=0.3)
###Plot out mapI2
#plt.plot(xAxis2500, mapI2[75000:100000], color='purple', linewidth=0.3)
plt.title('SPGD Detectors TP1 Testing S4 Lineup Post Map ')
plt.xlabel('seconds')
plt.ylabel('Kilowatts ')
plt.grid()
plt.savefig("Rx Power S4 TP1 Lineup SPGD Post Map.svg")
plt.show()
###Section 5
##Plot out mapC1
plt.plot(xAxis2500, mapC1[4000:5000], color='red',linewidth=0.3)
##Plot out mapC2
plt.plot(xAxis2500, mapC2[4000:5000], color='orange',linewidth=0.3)
###Plot out mapI1
#plt.plot(xAxis2500, mapI1[10000:12500], color='teal', linewidth=0.3)
###Plot out mapI2
#plt.plot(xAxis2500, mapI2[10000:12500], color='purple',linewidth=0.3)
plt.title('SPGD Detectors TP1 Testing S5 Lineup Post Map ')
plt.xlabel('seconds')
plt.ylabel('Kilowatts ')
plt.grid()
plt.savefig("Rx Power S5 TP1 Lineup SPGD Post Map.svg")
plt.show()
###Section 6
##Plot out mapC1
plt.plot(xAxis2500, mapC1[5000:6000], color='red', linewidth=0.3)
##Plot out mapC2
plt.plot(xAxis2500, mapC2[5000:6000], color='orange', linewidth=0.3)
###Plot out mapI1
#plt.plot(xAxis2500, mapI1[12500:15000], color='teal', linewidth=0.3)
###Plot out mapI2
#plt.plot(xAxis2500, mapI2[12500:15000], color='purple', linewidth=0.3)
plt.title('SPGD Detectors TP1 Testing S6 Lineup Post Map ')
plt.xlabel('seconds')
plt.ylabel('Kilowatts ')
plt.grid()
plt.savefig("Rx Power S6 TP1 Lineup SPGD Post Map.svg")
plt.show()
###Section 7
##Plot out mapC1
plt.plot(range(2000), mapC1[6000:8000], color='red', linewidth=0.3)
##Plot out mapC2
plt.plot(range(2000), mapC2[6000:8000], color='orange', linewidth=0.3)
###Plot out mapI1
#plt.plot(range(4000), mapI1[15000:19000], color='teal', linewidth=0.3)
###Plot out mapI2
#plt.plot(range(4000), mapI2[15000:19000], color='purple',linewidth=0.3)
plt.title('SPGD Detectors TP1 Testing S7 Lineup Post Map ')
plt.xlabel('seconds')
plt.ylabel('Kilowatts ')
plt.grid()
plt.savefig("Rx Power S7 TP1 Lineup SPGD Post Map.svg")
plt.show()
