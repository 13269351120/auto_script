import os 
import commands 

i = 0 

while ( i < 2):
    if( i == 0) :
        os.chdir("/home/luban/sutenghui/colmap_perf/")
        print os.getcwd()
        i+=1
    else :
        i+=1
        print os.getcwd() 

#cmd = 'sh distance.sh /nfs/project/localization/measure_set/software_park_one/20181128_iphone_starneto_validation_1fps_01.txt  /home/luban/sutenghui/localization_task/20181218/merged_model_software_park_one_two_linxiuguigu_20181210/perf_test.txt > /home/luban/sutenghui/localization_task/scripts/sth.log'

#(status, output) = commands.getstatusoutput(cmd)

validation = "/nfs/project/daily_3drecon/20181211/3drecon/test_partial_ba/iphone7p_starneto_shangqingyuan_120/sparse"

dirnum = 0

for lists in os.listdir(validation):
    dirname = os.path.join(validation,lists)
    print dirname 
    
    if os.path.isdir(dirname): 
        dirnum += 1 

if dirnum > 1 :    
    print "There are " + str(dirnum) + "directories,  we should merge into one ! "

##

shell_log="shell.log"
cmd = 'du -h ' + validation + ' > /home/luban/sutenghui/localization_task/scripts/' + shell_log 
(status, output ) = commands.getstatusoutput(cmd)

## delete small model 
log = open("/home/luban/sutenghui/localization_task/scripts/shell.log")
for line in log :
    print line 
    arr = line.split('  ') 
    size = arr[0]
    modelpath = arr[1]
    print "size:" + size + "  model:" + modelpath  

log.close 

 
