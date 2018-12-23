#!/usr/bin/python
#! -*- encoding: utf-8 -*-

#This script will run localization.sh 
#Author:    sthsuitenghui_i@didichuxing.com

import os
import subprocess
import sys
import datetime
import time
import commands 

ROOT_PATH = "/home/luban/sutenghui/localization_task"
table_ = open(os.path.join(ROOT_PATH, 'localization_template.sh'),"r").read() 


today=str(datetime.date.today().strftime('%Y%m%d'))  
today_dir = os.path.join(ROOT_PATH, today)

if os.path.exists(today_dir) : 
    print "has exists!" 
else: 
    os.mkdir(today_dir)

# task title 
titlearr = [
"jincheng_huaweidasha_iphone7p_20181206_yaw100_iphone7p_20181206"
,"jincheng_huaweidasha_iphone7p_20181206_yaw120_iphone7p_20181206"
,"jincheng_huaweidasha_samsung_20181206_yaw100_iphone7p_20181206"
,"jincheng_huaweidasha_samsung_20181206_yaw120_iphone7p_20181206"

]
focaltypearr = ["1","1","2","2"]
 
indexarr = [
"/nfs/project/localization/faissindex/index_trained_SoftwareParkOne20180510_trained_NoPopulate.faissindex"
,"/nfs/project/localization/faissindex/index_trained_SoftwareParkOne20180510_trained_NoPopulate.faissindex"
,"/nfs/project/localization/faissindex/index_trained_SoftwareParkOne20180510_trained_NoPopulate.faissindex"
,"/nfs/project/localization/faissindex/index_trained_SoftwareParkOne20180510_trained_NoPopulate.faissindex"

 ] 
modelarr = [
"/nfs/project/daily_3drecon/20181206/3drecon/test_partial_ba/iphone7_starneto_huaweidasha_1fps_100/sparse"
,"/nfs/project/daily_3drecon/20181206/3drecon/test_partial_ba/iphone7_starneto_huaweidasha_1fps_120/sparse"
,"/nfs/project/daily_3drecon/20181206/3drecon/test_partial_ba/samsung_starneto_huaweidasha_1fps_100/sparse"
,"/nfs/project/daily_3drecon/20181206/3drecon/test_partial_ba/samsung_starneto_huaweidasha_1fps_120/sparse"

] 

imagearr = [
"/nfs/project/localization/measure_set/testing_set/20181206_huaweidasha_iphone7p_test.txt"
,"/nfs/project/localization/measure_set/testing_set/20181206_huaweidasha_iphone7p_test.txt"
,"/nfs/project/localization/measure_set/testing_set/20181206_huaweidasha_iphone7p_test.txt"
,"/nfs/project/localization/measure_set/testing_set/20181206_huaweidasha_iphone7p_test.txt"

] 
databasearr = [
"/nfs/project/daily_3drecon/20181206/3drecon/databases/iphone7p_starneto_huaweidasha_1fps/database.db"
,"/nfs/project/daily_3drecon/20181206/3drecon/databases/iphone7p_starneto_huaweidasha_1fps/database.db"
,"/nfs/project/daily_3drecon/20181206/3drecon/databases/samsung_starneto_huaweidasha_1fps/database.db"
,"/nfs/project/daily_3drecon/20181206/3drecon/databases/samsung_starneto_huaweidasha_1fps/database.db"

] 

validationarr = [
"/nfs/project/localization/measure_set/validation_set/20181206_huaweidasha_iphone7p_validation.txt"
,"/nfs/project/localization/measure_set/validation_set/20181206_huaweidasha_iphone7p_validation.txt"
,"/nfs/project/localization/measure_set/validation_set/20181206_huaweidasha_iphone7p_validation.txt"
,"/nfs/project/localization/measure_set/validation_set/20181206_huaweidasha_iphone7p_validation.txt"

]

count = len(modelarr)

print "count:" ,count 
for i in range(0,count) :
    print i 
    task_dir = os.path.join(today_dir,titlearr[i])
    if os.path.exists(task_dir) : 
        print "task has exist ! please check your title name and make them unique..."
        continue 
    else :
        os.mkdir(task_dir)
    title = titlearr[i]+".sh" 
    focaltype = focaltypearr[i]
    index = indexarr[i]
    model = modelarr[i]
    image = imagearr[i]
    database = databasearr[i]
    validation = validationarr[i]

    ## Check whether the model is unique , if not , merge it into one 
     

 
#    print index , model , image , database
    ## Fill Actual Value into Template
    name = os.path.join(task_dir,title) 
    localization_sh = open(name,"w")
    localization_sh.write(table_.replace("____index____",index).replace("____model____",model).replace("____image____",image).replace("____database____",database).replace("____focaltype____",focaltype))
    localization_sh.close()

    ## Run the Localization Script 
    cmd = 'sh ' + name + ' > ' + task_dir +'/out.log'
    print cmd 
    (status, output) = commands.getstatusoutput(cmd)
    print status, output
   
    ## Grep ___PerfTestSuccess___ from out.log into perf_test.txt 
    cmd = 'cat '+task_dir + '/out.log | grep ___PerfTestSuccess___ > ' + task_dir + '/perf_test.txt' 
    (status, output) = commands.getstatusoutput(cmd)
    print status , output 
    ## Run the distance.sh 
    ## Output : performance.txt
    distance_path = "/home/luban/sutenghui/colmap_perf/"
    os.chdir(distance_path)
    
    cmd = 'sh distance.sh '+ validation + ' ' + task_dir +'/perf_test.txt > ' + task_dir + '/performance.txt' 
    (status , output) = commands.getstatusoutput(cmd)  
    print status , output  
    
    
    




