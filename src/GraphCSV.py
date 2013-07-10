'''
Created on May 18, 2013

@author: Matt
'''
import sys
import csv
import numpy as np
import dates
import pyplot as plt

class CSVgraph:
    def __init__(self,**kwargs):
        self.dbFile = kwargs.get('db_file')
        self.specFile = kwargs.get('spec_file')
    
    def graphDB(self,graphName):
        print self.dbFile
        csv_reader = csv.reader(open(self.dbFile,'r'))
        bigx = float(-sys.maxint -1)
        bigy = float(-sys.maxint -1)
        smallx = float(sys.maxint)
        smally = float(sys.maxint)
        
        verts = []
        for row in csv_reader:
            print row
            verts.append(row)

        x_arr = []
        y_arr = []
        for vert in verts:
            date = vert[0].split(':')
            print float(date[0])+(float(date[1])/60)
            x_arr.append(float(date[0])+(float(date[1])/60))
            y_arr.append(vert[1])
        
#         dates.date2num(x_arr)
        fig = plt.figure()
        ax = fig.add_axes([0.1,0.1,0.8,0.8])
        ax.set_xlabel('Time (hh:mm:ss)')
        ax.set_ylabel('Decibels (db)')
        #ax.set_xlim()
        ax.set_ylim(30,80)
        ax.plot(x_arr,y_arr)
        plt.show()
        plt.savefig(graphName)
    
    def graphSpec(self,graphName):
        csv_reader = csv.reader(open(self.specFile,'r'))
        cnt = 0
        frequencies = None
        decibels = None
        for line in csv_reader:
            if cnt == 0:
                frequencies = line
                cnt += 1
            else:
                decibels = line
#         decibels = [(decibels)]
        print frequencies, decibels

        cnt=0
        frequencies_floats=[]
        for x in frequencies:
            frequencies_floats.append(float(x))
            cnt+=1
        cnt=0
        decibels_floats=[]
        for x in decibels:
            decibels_floats.append(float(x))
            cnt+=1
        N=len(decibels)
        ind = np.arange(N)
        width = .35
        fig = plt.figure()
        plt.bar(ind,decibels_floats,width)
        plt.xticks(ind+width/2., frequencies,rotation=40, size='small')
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Decibels (db)")
        plt.show()
