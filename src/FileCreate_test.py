'''
Created on Jul 1, 2013

This is a script to automate the entire data generating process involved with
parsing the raw data from the XL2 textfiles, and generates all the neccessary
excel readable CSV Files. These CSV files can be used for graphing and visualizing
the data quickly and easily. There are many types of files that are automatically 
generated for the user, listed below

'All_site_3rd_day#' : All the data points from one day representing the 1/3 octave frequencies
'All_site_3rd_Stitch : one CSV file containing all the days of 1/3 octave frequency readings, stitched together
'All_site_DB_day#' : All the decibel readings from one day of recording
'site_3rd_day#' : The averaged 1/3 octave frequency columns for one day of recording
'site_DB_day#' : 5 minute samples of the DB readings from one day, used for graphing purposes
'site_Stitch' : one CSV file that contains all the days of DB readings stitched together
'site_stitch_moving_avg' : the same as above, but with a 3rd column representing the moving average points

@author: Matt
'''
import os
import csv
import CreateCSV as create
import stitching_data as stitch
import Calc_Statistics as calc


#Variables that the user must specify.
#raw:      The complete path where all of the raw db and raw 3rd data files from the XL2 are located.
#site:     The complete site name (safest without spaces) that all generated files will use in their
#          file names.
#update:   update should be marked as 'True' if the user wants to check to regenerate stitched files 
#          with newer data files or days. The user should mark 'False' if they do not want to run the
#          stitching programs at this time
#cut:      cut should be true if the user wants to run the cutting program that cuts out the bad times
#          in their data
         
raw = "C:\Users\Matt\Documents\IQP\PINEHILLTEST\RawData"
site = "PineHill"
update = True
cut = False

#Interference and maintentance times specified in this cutTimes list in the format
# [[[date],[startTimeCut],[endTimeCut]],[...],[...]]
# [[YYYY,DD,MM],[hh,mm,ss],[hh,mm,ss]]
#
# List all times to be cut
#
# NOTE: Cut times are only applied to 'All' files that would be used for computing
# averages on the basis that maintenence interference would not greatly impact
# the sampled graphs for viewing purposes.
cutTimes = [[[2013,6,28],[10,00,00],[17,05,00]],
            [[2013,6,29],[17,00,00],[17,20,00]],
            [[2013,6,30],[16,51,00],[17,8,00]],
            [[2013,7,1],[16,52,00],[17,9,00]],
            [[2013,7,2],[16,17,00],[16,30,00]],
            [[2013,7,3],[17,01,00],[17,22,00]],
            [[2013,7,4],[17,50,00],[18,06,00]],
            [[2013,7,5],[15,40,00],[17,20,00]]]

#create the raw dir if the one given doesn't exist
if not os.path.exists(raw):
    os.makedirs(raw)

#change directories to given path with raw data and get parent
os.chdir(raw)
parent = os.path.split(raw)[0]
dbDay = os.path.join(parent,'dbDaily')
freqDay = os.path.join(parent,'3rdDaily')
dbAll = os.path.join(parent,'AllDB')
freqAll = os.path.join(parent,'All3rd')

# if not os.path.exists(os.path.join(parent,'dbDaily')):
#     dbDay = os.path.join(parent,'dbDaily')
#     os.makedirs(dbDay)
# if not os.path.exists(os.path.join(parent,'3rdDaily')):
#     freqDay = os.path.join(parent,'3rdDaily')
#     os.makedirs(freqDay)
# if not os.path.exists(os.path.join(parent,'AllDB')):
#     dbAll = os.path.join(parent,'AllDB')
#     os.makedirs(dbAll)
# if not os.path.exists(os.path.join(parent,'All3rd')):
#     freqAll = os.path.join(parent,'All3rd')
#     os.makedirs(freqAll)
   
#A list of all the raw data files 
list = os.listdir(raw)

#A list of all the generated files inside of the main site location folder
parentList = [x.split('.')[0] for x in os.listdir(parent)]

#Loops through the raw data files in the directory given, 
#creating the daily decibel csv files for graphing (5 minute sample)
#along with the spectrogram data. Both types of files are created
#in the parent directory of the raw files folder
dayCnt = 0
print 'begin'
for count,file in enumerate(sorted(list)):
    if count %2 == 0: #increments the day counter every other file
        dayCnt += 1
    dbFileName = site+'_DB_day'+str(dayCnt)#Create the new decibel file name  
    specFileName = site+'_3rd_day'+str(dayCnt)#Create the new spec file name 
    
    print file
    #If the current file is a DB file
    if file.split('_')[3] == '123':
        
        if dbFileName not in parentList: #If the dbFile is not already generated
            dbData = create.CSVcreate(db_file=file)
            dbData.db_CSV(os.path.join(parent,dbFileName+'.csv'), True)#Create the sampled dB CSV file
        
        if 'All_'+dbFileName not in parentList: #if the All_dbFile is not already generated
            dbData = create.CSVcreate(db_file=file)
            unsampledFileName = 'All_' + dbFileName
            dbData.db_CSV(os.path.join(parent,unsampledFileName+'.csv'),False)#Create the All_dB unsampled CSV file
        
    #If the current file is a Frequency file   
    elif file.split('_')[3] == 'RTA':
        
        if specFileName not in parentList: #If the specFile is not already generated
            specData = create.CSVcreate(spec_file=file)
            specData.spec_CSV(os.path.join(parent,specFileName+'.csv')) #Create the freq CSV file
        
        if  'All_'+specFileName not in parentList: #If the All_specFile is not already generated
            specData = create.CSVcreate(spec_file=file)
            specData.write_All_Spec(os.path.join(parent,'All_'+specFileName+'.csv')) #Create the All_specFile CSV file

#make to change directory to the parent, main site folder
os.chdir(parent)

#if the db Stitch file is not already generated, or it is desired to update the file,
#then create or update the stitch file with all available day files
if site+'_Stitch' not in parentList or update: 
    stitch.stitch(site+'_Stitch.csv', True,
                  site+'_DB_day1.csv',
                  site+'_DB_day2.csv',
                  site+'_DB_day3.csv',
                  site+'_DB_day4.csv',
                  site+'_DB_day5.csv',
                  site+'_DB_day6.csv',
                  site+'_DB_day7.csv')
    
    #calculate the rolling average for the stitched dB file for graphing purposes and put
    #it in a seperate file
    stitch.appendAverages(site+'_Stitch.csv', 7)

#if the All_db Stitch file is not already generated, or it is desired to update the file,
#then create or update the stitch file with all available day files
if 'All_'+site+'_Stitch' not in parentList or update:
    stitch.stitch('All_'+site+'_Stitch.csv', False,
                  'All_'+site+'_DB_day1.csv',
                  'All_'+site+'_DB_day2.csv',
                  'All_'+site+'_DB_day3.csv',
                  'All_'+site+'_DB_day4.csv',
                  'All_'+site+'_DB_day5.csv',
                  'All_'+site+'_DB_day6.csv',
                  'All_'+site+'_DB_day7.csv')

#if the All_3rd freq Stitch file is not already generated, or it is desired to update the file,
#then create or update the stitch file with all available day files
if 'All_'+site+'_3rd_Stitch' not in parentList or update:
    stitch.stitch('All_'+site+'_3rd_Stitch.csv', False,
                  'All_'+site+'_3rd_day1.csv',
                  'All_'+site+'_3rd_day2.csv',
                  'All_'+site+'_3rd_day3.csv',
                  'All_'+site+'_3rd_day4.csv',
                  'All_'+site+'_3rd_day5.csv',
                  'All_'+site+'_3rd_day6.csv',
                  'All_'+site+'_3rd_day7.csv')

# calc.cutTime('All_'+site+'_Stitch.csv',[2013,6,28],[10,00,00],[17,05,00])
# calc.cutTime('All_'+site+'_Stitch.csv',[2013,6,29],[17,00,00],[17,20,00])
# calc.cutTime('All_'+site+'_Stitch.csv',[2013,6,30],[16,51,00],[17,8,00])
# calc.cutTime('All_'+site+'_Stitch.csv',[2013,7,1],[16,52,00],[17,9,00])
# calc.cutTime('All_'+site+'_Stitch.csv',[2013,7,2],[16,17,00],[16,30,00])
# calc.cutTime('All_'+site+'_Stitch.csv',[2013,7,3],[17,01,00],[17,22,00])
# calc.cutTime('All_'+site+'_Stitch.csv',[2013,7,4],[17,50,00],[18,06,00])
# calc.cutTime('All_'+site+'_Stitch.csv',[2013,7,5],[15,40,00],[17,20,00])

if cut:
    for timeStamp in cutTimes:
        calc.cutTime('All_'+site+'_Stitch.csv',timeStamp[0],timeStamp[1],timeStamp[2])
        calc.cutTime('All_'+site+'_3rd_Stitch.csv',timeStamp[0],timeStamp[1],timeStamp[2])

#hourlyLeq,hourlyL50,hourlyL90 = calc.averageHourly('All_'+site+'_Stitch.csv')
#ovrLeq,overL50,overL90 = calc.overallAverages('All_'+site+'_Stitch.csv')
#dayAvg,nightAvg = calc.dayNightAverages('All_'+site+'_Stitch.csv')


# hourlyAvg_csv = open(site+'_hourlyAverages.csv','wb')
# hourlyWriter = csv.writer(hourlyAvg_csv,dialect='excel')
# hourlyWriter.writerow(['hour','Leq','L50','L90'])
# for hour,avg in enumerate(hourlyLeq):
#     print '%s,%s'%(hour,avg)
#     hourlyWriter.writerow([hour,avg,hourlyL50[hour],hourlyL90[hour]])




    

        
        
        
        
        