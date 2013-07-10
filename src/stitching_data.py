'''
Created on Jun 24, 2013

@author: Matt
'''
import csv
import numpy
import os
import datetime

def stitch(dest,lineGap,*filenames):
    first = True
    
    timeStart = datetime.time(17,0,0)
    timeEnd = datetime.time(16,59,59)
    
    stitch_csv = open(dest,'wb')
    writer = csv.writer(stitch_csv,dialect='excel')
        
    for count, file in enumerate(filenames):
        if os.path.exists(file):
            csv_reader = csv.reader(open(file,'r'))
            next_day = None
            for row in csv_reader:
                year,month,day = row[0].split(' ')[0].split('-')
                hours,mins,secs = row[0].split(' ')[1].split(':')
                
                #Convert all date data into ints
                year = int(year)
                month = int(month)
                day = int(day)
                hours = int(hours)
                mins = int(mins)
                secs = int(secs)
                d = datetime.date(year,month,day)
                t = datetime.time(hours,mins,secs)
                
                dayDate = datetime.datetime.combine(d,t)
                
                #get to first day of data starting at 1700
                if lineGap:
                    stamp = row[0].split(' ')[1]
                
                if first == True:
                    startDay = datetime.datetime.combine(d,timeStart)
                    
                    endDate = startDay + datetime.timedelta(days=1)
                    nextDay = datetime.datetime.combine(endDate,timeEnd)
                    
                    first = False
                    
                if dayDate >= startDay and dayDate < nextDay:
                    if lineGap:
                        writer.writerow([stamp,row[1]])
                    else:
                        writer.writerow(row)
                    
                if dayDate >= nextDay:
                    
                    if lineGap:
                        writer.writerow('')
                    
                    startDay = datetime.datetime.combine(d,timeStart)
                    
                    endDate = startDay + datetime.timedelta(days=1)#datetime.date(year,month,day+1)
                    nextDay = datetime.datetime.combine(endDate,timeEnd)
                    
                    if lineGap:
                        writer.writerow([stamp,row[1]])
                    else:
                        writer.writerow(row)
    print 'done appending averages'

def movingaverage(dest, window_size):
    data = csv.reader(open(dest,'r'))
    window= numpy.ones(int(window_size))/float(window_size)
    decibels = []
    for row in data:
        if row:
            if len(row) == 2:
                date = row[0]
                db = row[1]
                decibels.append(float(db)) 
    return numpy.convolve(decibels, window, 'same')

def appendAverages(dest,window_size): 
    averages = movingaverage(dest,window_size)
    counter = 0
    avg_file = dest[0:-4] + '_moving_avg.csv'
    avg_writer = csv.writer(open(avg_file,'wb'))
    avg_reader = csv.reader(open(dest,'r'))
    
    for row in avg_reader:
        if row:
            row.append(averages[counter])
            avg_writer.writerow(row)
            counter += 1
        else:
            avg_writer.writerow('')
    
               
# stitch('PineHill_Stitch.csv', True,
#        'PineHill_DB_day1.csv',
#        'PineHill_DB_day2.csv')
# 
# 
# appendAverages('PineHill_Stitch.csv',7)
            
        