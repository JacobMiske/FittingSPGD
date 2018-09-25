# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 11:11:07 2018

@author: Jacob Miske
"""

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

#Importing a bunch of stuff I might use
#import statistics as sts
import numpy as np
#import pandas as pd
import scipy
#from scipy import signal
#import matplotlib
import matplotlib.pyplot as plt
#import csv

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

#######################
###Reading txt files###
#######################
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

#INL lists have some bad items, offset into large real numbers, removed here
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
FixfINL_SPGD_1 = FixfINL_SPGD_1[27119:-40059]
FixfINL_SPGD_2 = FixfINL_SPGD_2[27019:-40059]
#DONT CHANGE, vital for making data line up properly
#This part expands INL detector lists artificially to work well with CEA
ExpdINL1=[]
ExpdINL2=[]
for i in range(19000):
    for j in range(5):
        ExpdINL1.append(FixfINL_SPGD_1[i])
    for j in range(5):
        ExpdINL2.append(FixfINL_SPGD_2[i])

xAxisINL1 = range(19000)
xAxisINL2 = range(19000)

#Views INL detectors together, raw
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

#Looks at just CEA
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

#Looks at normalizing CEA against each other
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
xAxis=range(19000) #Points of data, not actual seconds exactly

##Look at all four detector's raw output
#plt.plot(xAxis, FixfCEA1, color='red')
#plt.plot(xAxis, FixfCEA2, color='orange')
#plt.plot(xAxis, FixfINL_SPGD_1, color='teal')
#plt.plot(xAxis, FixfINL_SPGD_2, color='purple')
#plt.title('Four Detectors')
#plt.xlabel('seconds')
#plt.ylabel('Four Detector Output Raw')
#plt.show()


###Normalization of all detectors
#Just a guess that gets them close enough to make predictions and analysis on the graphs
multNorm = 2.2
for i in range(19000):
    FixfINL_SPGD_1[i]=FixfINL_SPGD_1[i]*multNorm
    FixfINL_SPGD_2[i]=FixfINL_SPGD_2[i]*multNorm

#Simple name for INL SPGDs
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

## Savitzky Golay plot
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


###Plotting sections of 2500 points
xAxis2500=range(2500)

######
###Plot for arbitrary unit of 'Reactor Power' ###Interesting Bit
######
#Very peak power is 60kW, ~2.2e-9 on CEA detectors == 20 kW


C1 = FixfCEA1
C2 = FixfCEA2
I1 = FixfINL1
I2 = FixfINL2


#C1 = fCEA1
#C2 = fCEA2
#I1 = fINL_SPGD_1
#I2 = fINL_SPGD_2

#Plot simplied lists
plt.plot(xAxis, C1, color='red')
plt.plot(xAxis, C2, color='orange')
plt.plot(xAxis, I1, color='teal')
plt.plot(xAxis, I2, color='purple')
plt.title(' Four Detectors (C1, C2, I1, I2)')
plt.xlabel('seconds')
plt.ylabel('Detector Output ')
plt.savefig("Four Detectors.svg")
plt.savefig("Four Detectors.png")
plt.show()

###Try averaging for Rx Power Interpreted before each individually
RxPowerInterp = []
for i in range(len(C1)):
    PInterp = (C1[i]+C2[i]+I1[i]+I2[i])/4
    RxPowerInterp.append(PInterp)

#Plotting Rx Power Average Value
plt.plot(xAxis, RxPowerInterp, color='black')
plt.title(' Rx Power Amperes Detectors ')
plt.xlabel('seconds')
plt.ylabel('Rx Power at Pico-Amperes Output ')
plt.savefig("Rx Power.svg")
plt.savefig("Rx Power.png")
plt.show()


#Getting far values of C and I
#Maxes, more useful here because detectors sometimes drop out to zero
maxC1=max(C1)
maxC2=max(C2)
maxI1=max(I1)
maxI2=max(I2)
#not as useful but could become so
minC1=min(C1)
minC2=min(C2)
minI1=min(I1)
minI2=min(I2)
#20kW point roughly, can refine later
medianC1 = (maxC1+minC1)/2
medianC2 = (maxC2+minC2)/2
medianI1 = (maxI1+minI1)/2
medianI2 = (maxI2+minI2)/2

#Notice points of interest
print('maxC1 ' + str(maxC1))
print('maxC2 ' + str(maxC2))
print('maxI1 ' + str(maxI1))
print('maxI2 ' + str(maxI2))

#Retain a version without mapping them to kilowatt values
picoampsC1 = C1
picoampsC2 = C2
picoampsI1 = I1
picoampsI2 = I2
#Get values for linear mapping functions
selectingXaxis = range(100)
meanC120kW = np.mean(picoampsC1[5500:5600])
meanC220kW = np.mean(picoampsC2[5500:5600])
meanI120kW = np.mean(picoampsI1[5500:5600])
meanI220kW = np.mean(picoampsI2[5500:5600])
meanC160kW = np.mean(picoampsC1[9800:9900])
meanC260kW = np.mean(picoampsC2[9800:9900])
meanI160kW = np.mean(picoampsI1[9800:9900])
meanI260kW = np.mean(picoampsI2[9800:9900])
meanAllFour20kW = np.mean([meanC120kW,meanC220kW,meanI120kW,meanI220kW] )
meanAllFour60kW = np.mean([meanC160kW,meanC260kW,meanI160kW,meanI260kW] )


#Useful for taking picoampere measures from SPGD to power measures
#for INL detectors, 60kW happans at max. INL1, 20kW, around 1.4e-9 and INL2, 20kW, around 6.77e-10
#For CEA1, 20kW around 2.18e-9. For CEA2, 20kW around 1.87e-9 
def SPGDmapperINL1(List, minList, maxList):
    for i in range(len(List)):
        List[i] = ((List[i])*(60- 20)/(meanI160kW-(meanI120kW)))
    return List
def SPGDmapperINL2(List, minList, maxList):
    for i in range(len(List)):
        List[i] = ((List[i])*(60- 20)/(meanI260kW-(meanI220kW)))
    return List
def SPGDmapperCEA1(List, minList, maxList):
    for i in range(len(List)):
        List[i] = ((List[i])*(60- 20)/(meanC160kW-(meanC120kW)))
    return List
def SPGDmapperCEA2(List, minList, maxList):
    for i in range(len(List)):
        List[i] = ((List[i])*(60- 20)/(meanC260kW-(meanC220kW)))
    return List
def SPGDmapperAverage(List, minList, maxList):
    for i in range(len(List)):
        List[i] = ((List[i])*(60- 20)/(meanAllFour60kW - (meanAllFour20kW)))
    return List
#Max value in list is not 60kW but closer to 65kW
def SPGDdetractAve(List):
    for i in range(len(List)):
        List[i] = (List[i]-30)
    return List
def SPGDdetractC1(List):
    for i in range(len(List)):
        List[i] = (List[i]-17.1)
    return List
def SPGDdetractC2(List):
    for i in range(len(List)):
        List[i] = (List[i]-15.85)
    return List
def SPGDdetractI1(List):
    for i in range(len(List)):
        List[i] = (List[i]-12.95)
    return List
def SPGDdetractI2(List):
    for i in range(len(List)):
        List[i] = (List[i]-12.5)
    return List

##Using functions written
mapC1=C1
mapC2=C2
mapI1=I1
mapI2=I2
mapC1 = SPGDmapperCEA1(C1, minC1, maxC1)    
mapC2 = SPGDmapperCEA2(C2, minC2, maxC2)    
mapI1 = SPGDmapperINL1(I1, minI1, maxI1)    
mapI2 = SPGDmapperINL2(I2, minI2, maxI2)  
mapC1 = SPGDdetractC1(C1)    
mapC2 = SPGDdetractC2(C2)    
mapI1 = SPGDdetractI1(I1)    
mapI2 = SPGDdetractI2(I2)  

###
###Plot one detector at a time
###

#mapC1 = SPGDdetractC1(mapC1)
plt.plot(xAxis, mapC1, color='red')
plt.title(' SPGD Detector C1 Against Rx Power ')
plt.xlabel('seconds')
plt.ylabel('Kilowatts ')
plt.savefig("SPGD mapped C1 test.svg")
plt.savefig("SPGD mapped C1 test.png")
plt.show()

#mapC2 = SPGDdetractC2(mapC2)
plt.plot(xAxis, mapC2, color='orange')
plt.title(' SPGD Detector C2 Against Rx Power ')
plt.xlabel('seconds')
plt.ylabel('Kilowatts ')
plt.savefig("SPGD mapped C2 test.svg")
plt.savefig("SPGD mapped C2 test.png")
plt.show()

#mapI1 = SPGDdetractI1(mapI1)
plt.plot(xAxis, mapI1, color='teal')
plt.title(' SPGD Detector I1 Against Rx Power ')
plt.xlabel('seconds')
plt.ylabel('Kilowatts ')
plt.savefig("SPGD mapped I1 test.svg")
plt.savefig("SPGD mapped I1 test.png")
plt.show()

#mapI2 = SPGDdetractI2(mapI2)
plt.plot(xAxis, mapI2, color='purple')
plt.title(' SPGD Detector I2 Against Rx Power ')
plt.xlabel('seconds')
plt.ylabel('Kilowatts ')
plt.savefig("SPGD mapped I2 test.svg")
plt.savefig("SPGD mapped I2 test.png")
plt.show()

#Plot mapped lists
plt.plot(xAxis, mapC1, color='red')
plt.plot(xAxis, mapC2, color='orange')
plt.plot(xAxis, mapI1, color='teal')
plt.plot(xAxis, mapI2, color='purple')
plt.title(' Four Detectors Against Rx Power ')
plt.xlabel('seconds')
plt.ylabel('Kilowatts ')
plt.savefig("Four SPGD mapped.svg")
plt.savefig("Four SPGD mapped.png")
plt.show()

#Plot to Kilowatts on averaged detector Rx Power
maxRxPI = max(RxPowerInterp)
minRxPI = min(RxPowerInterp)
RxPowerInterp = SPGDmapperAverage(RxPowerInterp, minRxPI, maxRxPI)
RxPowerInterp = SPGDdetractAve(RxPowerInterp)

plt.plot(xAxis, RxPowerInterp, color='black')
plt.title(' Rx Power Detectors ')
plt.xlabel('seconds')
plt.ylabel('Rx Power at Kilowatts Output ')
plt.savefig("Rx Power.svg")
plt.savefig("Rx Power.png")
plt.show()

###Average out all 4 detectors for Approx. Rx Power
RxPowerAverage =[]
for i in range(len(mapC1)):
    PowerInterp = (mapC1[i]+mapC2[i]+mapI1[i]+mapI2[i])/4
    RxPowerAverage.append(PowerInterp)

plt.plot(xAxis, RxPowerAverage, color='grey')
plt.title(' Rx Power Detectors ')
plt.xlabel('seconds')
plt.ylabel('Rx Power at Kilowatts Output ')
plt.savefig("Rx Power Average Detectors.svg")
plt.savefig("Rx Power Average Detectors.png")
plt.show()

##################################
### Sectioning ###################
##################################
RxPowerAverage_1 = RxPowerAverage[2500:5000]
RxPowerAverage_2 = RxPowerAverage[5000:7500]
RxPowerAverage_3 = RxPowerAverage[7500:10000]
RxPowerAverage_4 = RxPowerAverage[10000:12500]
RxPowerAverage_5 = RxPowerAverage[12500:15000]
RxPowerAverage_6 = RxPowerAverage[15000:17500]

#Section 1
plt.plot(xAxis2500, RxPowerAverage_1, color='grey')
plt.title('Rx Power S1')
plt.xlabel('seconds')
plt.ylabel('Detector Output ')
plt.savefig("S1 Rx Power Ave.svg")
plt.savefig("S1 Rx Power Ave.png")
plt.show()

#Section 2
plt.plot(xAxis2500, RxPowerAverage_2, color='grey')
plt.title('Rx Power S2')
plt.xlabel('seconds')
plt.ylabel('Detector Output ')
plt.savefig("S2 Rx Power Ave.svg")
plt.savefig("S2 Rx Power Ave.png")
plt.show()

#Section 3
plt.plot(xAxis2500, RxPowerAverage_3, color='grey')
plt.title('Rx Power S3')
plt.xlabel('seconds')
plt.ylabel('Detector Output ')
plt.savefig("S3 Rx Power Ave.svg")
plt.savefig("S3 Rx Power Ave.png")
plt.show()

#Section 4
plt.plot(xAxis2500, RxPowerAverage_4, color='grey')
plt.title('Rx Power S4')
plt.xlabel('seconds')
plt.ylabel('Detector Output ')
plt.savefig("S4 Rx Power Ave.svg")
plt.savefig("S4 Rx Power Ave.png")
plt.show()

#Section 5
plt.plot(xAxis2500, RxPowerAverage_5, color='grey')
plt.title('Rx Power S5')
plt.xlabel('seconds')
plt.ylabel('Detector Output ')
plt.savefig("S5 Rx Power Ave.svg")
plt.savefig("S5 Rx Power Ave.png")
plt.show()

#Section 6
plt.plot(xAxis2500, RxPowerAverage_6, color='grey')
plt.title('Rx Power S6')
plt.xlabel('seconds')
plt.ylabel('Detector Output ')
plt.savefig("S6 Rx Power Ave.svg")
plt.savefig("S6 Rx Power Ave.png")
plt.show()

###
# Search for mean(current) in range(20kw)
# Search for mean(current) in range(60kw)
## Do this independently for all four detectors
# Then state the function noted above "SPGDmapper" with these values
# Signal_60 - Signal_20 / (60-20)



###Section for plotting blade drop time in NRL 
newXrange = range(20)

#inital testing range for blade drop == [15840:15860]
# Each detector in series
mapC1 = SPGDdetractC1(mapC1)
plt.plot(xAxis, mapC1, color='red')
plt.xlabel('seconds')
plt.ylabel('Kilowatts ')
#plt.show()
mapC2 = SPGDdetractC2(mapC2)
plt.plot(xAxis, mapC2, color='orange')
plt.xlabel('seconds')
plt.ylabel('Kilowatts ')
#plt.show()
mapI1 = SPGDdetractI1(mapI1)
plt.plot(xAxis, mapI1, color='teal')
plt.xlabel('seconds')
plt.ylabel('Kilowatts ')
#plt.show()
mapI2 = SPGDdetractI2(mapI2)
plt.plot(xAxis, mapI2, color='purple')
plt.title('SPGD Detectors With Power Comparison ')
plt.xlabel('seconds')
plt.ylabel('Kilowatts ')
plt.savefig("SPGD Power Comparison.svg")
plt.savefig("SPGD Power Comparison.png")
plt.show()

#####################################
### Sectioning these good results ###
#####################################
RxPowerAverage =[]
for i in range(len(mapC1)):
    PowerInterp = (mapC1[i]+mapC2[i]+mapI1[i]+mapI2[i])/4
    RxPowerAverage.append(PowerInterp)
RxPowerAverage_1 = RxPowerAverage[2500:5000]
RxPowerAverage_2 = RxPowerAverage[5000:7500]
RxPowerAverage_3 = RxPowerAverage[7500:10000]
RxPowerAverage_4 = RxPowerAverage[10000:12500]
RxPowerAverage_5 = RxPowerAverage[12500:15000]
RxPowerAverage_6 = RxPowerAverage[15000:17500]

plt.plot(xAxis, RxPowerAverage, color='grey')
plt.title(' Rx Power Comparison with All  Detectors ')
plt.xlabel('seconds')
plt.ylabel('Rx Power at Kilowatts Output ')
plt.savefig("Rx Power Comparison with All Detectors.svg")
plt.savefig("Rx Power Comparison with All  Detectors.png")
plt.show()

#####################
### Test Plotting ###
#####################
##Plot out mapC1
plt.plot(xAxis, mapC1, color='red')
plt.title('SPGD Detector C1 ')
plt.xlabel('seconds')
plt.ylabel('Kilowatts ')
plt.savefig("Rx Power CEA 1 SPGD.svg")
plt.savefig("Rx Power CEA 1 SPGD.png")
plt.show()
##Plot out mapC2
plt.plot(xAxis, mapC2, color='orange')
plt.title('SPGD Detector C2 ')
plt.xlabel('seconds')
plt.ylabel('Kilowatts ')
plt.savefig("Rx Power CEA 2 SPGD.svg")
plt.savefig("Rx Power CEA 2 SPGD.png")
plt.show()
##Plot out mapI1
plt.plot(xAxis, mapI1, color='teal')
plt.title('SPGD Detector I1 ')
plt.xlabel('seconds')
plt.ylabel('Kilowatts ')
plt.savefig("Rx Power INL 1 SPGD.svg")
plt.savefig("Rx Power INL 1 SPGD.png")
plt.show()
##Plot out mapI2
plt.plot(xAxis, mapI2, color='purple')
plt.title('SPGD Detector I2 ')
plt.xlabel('seconds')
plt.ylabel('Kilowatts ')
plt.savefig("Rx Power INL 2 SPGD.svg")
plt.savefig("Rx Power INL 2 SPGD.png")
plt.show()

### Lineup SPGD all together

##Plot out mapC1
plt.plot(xAxis, fCEA1, color='red')
##Plot out mapC2
plt.plot(xAxis, fCEA2, color='orange')
##Plot out mapI1
plt.plot(xAxis, fINL_SPGD_1, color='teal')
##Plot out mapI2
plt.plot(xAxis, fINL_SPGD_2, color='purple')
plt.title('SPGD Detectors Testing Lineup ')
plt.xlabel('seconds')
plt.ylabel('Kilowatts ')
plt.savefig("Rx Power Lineup SPGD.svg")
plt.savefig("Rx Power Lineup SPGD.png")


###Citations###
# https://www.solver.com/smoothing-techniques

