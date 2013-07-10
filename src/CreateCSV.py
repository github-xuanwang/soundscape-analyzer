import csv, pygame
import datetime

class CSVcreate:
    def __init__(self,*args,**kwargs):
        self.dbFile = kwargs.get('db_file')
        self.specFile = kwargs.get('spec_file')
    
    def db_CSV(self,dest_name,sample):
#         raw_db = open(self.dbFile)
#         raw_lines = raw_db.read().split('/n')
        raw_lines, line_cnt = self.get_starting_line(self.dbFile,"# Broadband LOG Results",3)
        db_csv = open(dest_name,'wb')
        db_writer = csv.writer(db_csv,dialect='excel')
        
        count = 0
        first = True
        beginCount = False
        timeStart = datetime.time(16,55,0)
        startDay = None
        
        for line in raw_lines[line_cnt:]:
            data_point = line.split()
            if len(data_point) > 1:
                
                dayDate = data_point[0]+ ' '+ data_point[1]
                year,month,day = dayDate.split(' ')[0].split('-')
                hours,mins,secs = dayDate.split(' ')[1].split(':')
                
                year = int(year)
                month = int(month)
                day = int(day)
                hours = int(hours)
                mins = int(mins)
                secs = int(secs)
                
                date = datetime.date(year,month,day)
                time = datetime.time(hours,mins,secs)
                current = datetime.datetime.combine(date,time)
                
                if mins%5 == 0 and secs == 0 and sample:
                    db_writer.writerow([data_point[0]+ ' '+ data_point[1],data_point[3]])
                    count = 0
                elif not sample:
                    db_writer.writerow([data_point[0]+ ' '+ data_point[1],data_point[3]])
            else:
                print count
                break
            
        
        print "Decibel readings CSV File created with filename '%s'"%dest_name
    
    def spec_CSV(self,dest_name):
        
        raw_lines,line_cnt = self.get_starting_line(self.specFile,"# RTA LOG Results LAeq_dt",1)
        print line_cnt
        
        all_vals=raw_lines[line_cnt].split()
        print all_vals
        HZ_vals = all_vals[8:]
        for item in range(len(HZ_vals)):
            HZ_vals[item] = float(HZ_vals[item])   
                
        raw_lines,line_cnt = self.get_starting_line(self.specFile,"# RTA LOG Results LAeq over the whole log period",1)
        all_db_vals = raw_lines[line_cnt].split()
        db_vals = all_db_vals[6:]
        
        for item in range(len(db_vals)):
            if db_vals < 50:
                db_vals[item] = float(db_vals[item])
            
        spec_csv = open(dest_name,'wb')
        spec_writer = csv.writer(spec_csv,dialect='excel')
        
        spec_writer.writerow(HZ_vals)
        spec_writer.writerow(db_vals) 
        
       
    def write_All_Spec(self,dest_name):
        raw_lines,line_cnt = self.get_starting_line(self.specFile,"# RTA LOG Results LAeq_dt",3)
        
        reader = open(self.specFile).read().strip().split('\n')
        writer = csv.writer(open(dest_name,'wb'))
        counter = 0
        for row in reader:
            row = row.split()
            if counter >=line_cnt:
                if not row or len(row) < 35:
                    break
                dateStamp = row[0]+ ' '+ row[1]
                writer.writerow([dateStamp]+map(float,row[6:]))
                counter +=1
            counter +=1
        
    def get_starting_line(self,file,delimeter,skipln):
        raw_db = open(file)
        raw_lines = raw_db.read().split('\n')
        line_cnt = 0
        for line in raw_lines:
            if str(line) == delimeter:
                print "done!"
                line_cnt += skipln
                break;
            line_cnt += 1
        return raw_lines,line_cnt
    
    
# raw = open('DbLog_Quad.txt','r')
# print "yo"
# data = raw.read()
# data = data.split('\n')
# count = 0
# for line in data:
#     if str(line) == "# Broadband LOG Results":
#         count += 3
#         print "break"
#         break;
#     count += 1
# print "writing"
# db_by_time = open('Quad_db.csv','r+b')
# db_writer = csv.writer(db_by_time,dialect='excel')
# for line in data[count:]:
#     data_point = line.split()
#     if data_point:
#         db_writer.writerow([data_point[1],data_point[3]])
#         print data_point
#     else:
#         break

