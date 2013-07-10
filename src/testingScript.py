'''
Created on May 18, 2013

@author: Matt
'''
import CreateCSV as create
import GraphCSV as graph

#db_CSV(filename,sample?)
dbData = create.CSVcreate(db_file='2013-06-29_SLM_000_123_Log.txt')
dbData.db_CSV('PineHill_DB_day2.csv',True)
# 
# dbData = create.CSVcreate(db_file='2013-06-22_SLM_000_123_Log.txt')
# dbData.db_CSV('Cadillac_DB_day2_.csv',True)
# 
# dbData = create.CSVcreate(db_file='2013-06-23_SLM_000_123_Log.txt')
# dbData.db_CSV('Cadillac_DB_day3_.csv',True)
# 
# dbData = create.CSVcreate(db_file='2013-06-24_SLM_000_123_Log.txt')
# dbData.db_CSV('Cadillac_DB_day4_.csv',True)
# 
# dbData = create.CSVcreate(db_file='2013-06-25_SLM_000_123_Log.txt')
# dbData.db_CSV('Cadillac_DB_day5_.csv',True)
# 
# dbData = create.CSVcreate(db_file='2013-06-26_SLM_000_123_Log.txt')
# dbData.db_CSV('Cadillac_DB_day6_.csv',True)
# 
# dbData = create.CSVcreate(db_file='2013-06-27_SLM_000_123_Log.txt')
# dbData.db_CSV('Cadillac_DB_day7_.csv',True)
  
specData = create.CSVcreate(spec_file='2013-06-29_SLM_000_RTA_3rd_Log.txt')
# specData.write_All_Spec('All_Cadillac_3rd_day1.csv')
specData.spec_CSV('PineHill_3rd_day2.csv')
# 
# specData = create.CSVcreate(spec_file='2013-06-22_SLM_000_RTA_3rd_Log.txt')
# specData.write_All_Spec('All_Cadillac_3rd_day2.csv')
# specData.spec_CSV('Cadillac_3rd_day2.csv')
# 
# specData = create.CSVcreate(spec_file='2013-06-23_SLM_000_RTA_3rd_Log.txt')
# specData.write_All_Spec('All_Cadillac_3rd_day3.csv')
# specData.spec_CSV('Cadillac_3rd_day3.csv')
# 
# specData = create.CSVcreate(spec_file='2013-06-24_SLM_000_RTA_3rd_Log.txt')
# specData.write_All_Spec('All_Cadillac_3rd_day4.csv')
# specData.spec_CSV('Cadillac_3rd_day4.csv')
# 
# specData = create.CSVcreate(spec_file='2013-06-25_SLM_000_RTA_3rd_Log.txt')
# specData.write_All_Spec('All_Cadillac_3rd_day5.csv')
# specData.spec_CSV('Cadillac_3rd_day5.csv')
# 
# specData = create.CSVcreate(spec_file='2013-06-26_SLM_000_RTA_3rd_Log.txt')
# specData.write_All_Spec('All_Cadillac_3rd_day6.csv')
# specData.spec_CSV('Cadillac_3rd_day6.csv')

# specData = create.CSVcreate(spec_file='2013-06-27_SLM_000_RTA_3rd_Log.txt')
# specData.write_All_Spec('All_Cadillac_3rd_day7.csv')
# specData.spec_CSV('Cadillac_3rd_day7.csv')
 
 
# dbGrapher = graph.CSVgraph(db_file='room2.csv')
# dbGrapher.graphDB('room2_dbGraph.png')
# 

# dbGrapher = graph.CSVgraph(spec_file='room2_spec.csv')
# dbGrapher.graphSpec('spec_room2_Graph.png')