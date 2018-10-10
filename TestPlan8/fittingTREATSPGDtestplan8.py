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
#from scipy import signal
#import matplotlib
import matplotlib.pyplot as plt

#read a txt
CEA_txt_file = r"Test_Plan_8_2018_1.txt"

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
        
print(len(CEA1))
xRange = range(281644)

plt.plot(xRange, CEA1, 'red')
plt.title('CEA SPGD Detector Test Plan 8')
plt.xlabel('Data Points')
plt.savefig('CEA_TP8_Raw.svg')
plt.grid()
plt.show()