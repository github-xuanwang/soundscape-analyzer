'''
Created on Jun 24, 2013

@author: Matt
'''
import csv
import operator
import datetime

def nthPercent(dbFile):
    csv_reader = csv.reader(open(dbFile,'r'))
    sortedList = sorted(csv_reader, key=operator.itemgetter(1), reverse=False)
    l = len(sortedList)
    print sortedList[:20]
    l50 = sortedList[l/2]
    l90 = sortedList[l-int(l * .9)]
    return l50[1],l90[1]

#input date format: [year,month,day]
#input time format: [hour,mins,sec]
def cutTime(dbFile,date,sTime,eTime):
    reader = csv.reader(open(dbFile, 'r'))
    start = datetime.datetime(date[0],date[1],date[2],sTime[0],sTime[1],sTime[2])
    end = datetime.datetime(date[0],date[1],date[2],eTime[0],eTime[1],eTime[2])
    correctedData = []
    for row in reader:
        if row:
            year,month,day = row[0].split(' ')[0].split('-')
            hours,mins,secs = row[0].split(' ')[1].split(':')
            
            #Convert all date data into ints
            year = int(year)
            month = int(month)
            day = int(day)
            hours = int(hours)
            mins = int(mins)
            secs = int(secs)
        
            timeStamp = datetime.datetime(year,month,day,hours,mins,secs)
            
            if start <= timeStamp and timeStamp <= end:
                None
            elif row:
                correctedData.append(row)
                
    writer = csv.writer(open(dbFile,'wb'),dialect='excel')
    for row in correctedData:
        writer.writerow(row)

#takes a stitch of site's complete,un-sampled, 
#week of data and averages each hour
def averageHourly(siteFile):
    hours = {}
    averages = {}
    l50 = {}
    l90 = {}
    reader = csv.reader(open(siteFile, 'r'))
    for row in reader:
        hour = row[0].split(' ')[1].split(':')[0]
        if hour not in hours:
            list = [float(row[1])]
            hours[hour] = (1,float(row[1]),list)
        else:
            count,sums,hourList = hours[hour]
            hourList.append(float(row[1]))
            hours[hour] = (count+1,sums+float(row[1]),hourList)
    for hour in hours.keys():
        if hour not in averages:
            count,sums,hourList = hours[hour]
            hourList = sorted(hourList)
            length = len(hourList)
            l50[hour] = hourList[length/2]
            l90[hour] = hourList[length-int(length * .9)]
            averages[hour] = sums/count
    count = 0
    for key in sorted(averages.iterkeys()):
        print "%s: Leq: %s, L50: %s, L90: %s"  % (count,averages[key],l50[key],l90[key])
        count +=1
    return averages,l50,l90
    
def overallAverages(siteFile):
    hourlyAvgs,l50,l90 = averageHourly(siteFile)
    Leq = sum(hourlyAvgs.values())/24
    L50,L90 = nthPercent(siteFile)
    print "Leq: %s, L50: %s, L90: %s" % (Leq,L50,L90)
    return Leq,L50,L90
    
def dayNightAverages(siteFile):
    reader = csv.reader(open(siteFile,'r'))
    dayData = []
    nightData = []
    for row in reader:
        hour = row[0].split(' ')[1].split(':')[0]
        print hour
        if (7 <= int(hour)) and (int(hour) < 19):
            dayData.append(float(row[1]))
        else:
            nightData.append(float(row[1]))
    
    dayLen = len(dayData)
    nightLen = len(nightData)
    
    print dayLen, nightLen
    
    orderedDay = sorted(dayData)
    orderedNight = sorted(nightData)
    
    dLeq = sum(dayData)/len(dayData)
    nLeq = sum(nightData)/len(nightData)
    
    dL50 = orderedDay[dayLen/2]
    nL50 = orderedNight[nightLen/2]
    
    dL90 = orderedDay[dayLen-int(dayLen * .9)]
    nL90 = orderedNight[nightLen-int(nightLen * .9)]
    
    print 'Daytime: Leq= %s, L50=%s, L90=%s' % (dLeq,dL50,dL90)
    print 'NightTime: Leq= %s, L50=%s, L90=%s' % (nLeq,nL50,nL90)
    return (dLeq,dL50,dL90),(nLeq,nL50,nL90)

#Averages all of the frequency columns from an 'All_3rd' file.
#  
#WARNING: THIS IS AN INCREDIBLY SLOW AND COSTLY PROCCESS AND HAS NOT BEEN FULLY TESTED. 
#         SPREADSHEET PROGRAMS LIKE EXCEL ARE RECOMMENDED TO AVERAGE THE FREQUENCY COLUMNS
#         MUCH FASTER
def averageFrequencies(siteFile):
    frequencies = [12.5,16.0,20.0,25.0,31.5,40.0,50.0,63.0,80.0,100.0,125.0,160.0,200.0,250.0,315.0,400.0,500.0,630.0,800.0,1000.0,1250.0,1600.0,2000.0,2500.0,3150.0,4000.0,5000.0,6300.0,8000.0,10000.0,12500.0,16000.0,20000.0]
    decibels = []
    reader = csv.reader(open(siteFile,'r'))
    
    count = 0
    print 'done'
    for row in reader:
#         print row
        for i in range(len(frequencies)):
            if len(decibels) > i:
                decibels[i] += row[i+1]
            else:
                decibels.append(row[i+1])
        count +=1
    
    for i in range(len(decibels)):
        print '%s: %s' %(frequencies[i],decibels[i]/count)
    
    return (frequencies,decibels/count)
        
     
      
                
# cutTime('All_Cadillac_3rd_stitch_complete.csv',[2013,6,21],[10,00,00],[16,40,00])
# cutTime('All_Cadillac_3rd_stitch_complete.csv',[2013,6,22],[13,10,00],[13,30,00])
# cutTime('All_Cadillac_3rd_stitch_complete.csv',[2013,6,23],[17,07,00],[17,18,00])
# cutTime('All_Cadillac_3rd_stitch_complete.csv',[2013,6,24],[16,30,00],[16,40,00])
# cutTime('All_Cadillac_3rd_stitch_complete.csv',[2013,6,25],[16,17,00],[16,30,00])
# cutTime('All_Cadillac_3rd_stitch_complete.csv',[2013,6,26],[16,52,00],[17,15,00])
# cutTime('All_Cadillac_3rd_stitch_complete.csv',[2013,6,27],[17,03,00],[17,20,00])

#averageHourly('All_Cadillac_stitch_complete.csv')
#overallAverages('All_Cadillac_stitch_complete.csv')
#dayNightAverages('All_Cadillac_stitch_complete.csv')

#averageFrequencies('All_Cadillac_3rd_stitch.csv')


