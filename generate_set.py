#!/usr/bin/python
# -*- coding: utf-8 -*-
# This Script is used to auto test localization 
# by author sthsutenghui_i@didiglobal.com

import os
import subprocess
import sys
import datetime
import time
import shutil
import commands


#CONST PATH , they should be the same with the real system
reco_root_path = "/nfs/project/daily_3drecon/"
localization_root_path = "/nfs/project/localization/"  
model_normalizer = "/home/luban/sutenghui/ar/colmap/build/src/exe"
localization_task_path = "/home/luban/sutenghui/localization_task"
distance_path = "/home/luban/sutenghui/colmap_perf/"
#test_model_path = "/nfs/project/daily_3drecon/20181214/3drecon/test_partial_ba/samsung_starneto_xierqizhanfanxiang_1fps_100/sparse"


#default settings , will change by different test  
default_test_sensor = "samsung" 
faiss_index = "/nfs/project/localization/faissindex/index_trained_SoftwareParkOne20180510_trained_NoPopulate.faissindex"
num_of_test_set = 1000
model_threshold_size = 20 
car_id = "Beijing_Buick_Q9Q3M0"

#constant value
byte_to_Mbyte = 1024 * 1024


# ###########################################
# Desc :Get_directory size
# ############################################
def get_dirsize(dirpath):
    size = 0 
    for root , dirs , files in os.walk(dirpath):
        size += sum( [os.path.getsize(os.path.join(root,name)) for name in files] )
    size /= byte_to_Mbyte
    return size 
	
	
# ###########################################
# Desc :parse model path , mining information
# ############################################
def parse_model_path( model_path , user) :
    print "\n\033[1;44m_______________Parse_Model_Path_______________\033[0m"
    #print "\n--------------------------------------------------------------------------------------------\n"
    print "\033[1;32m[model_path]  :\033[0m\033[1;34m" , str(model_path) + "\033[0m\n"
    #print "\n--------------------------------------------------------------------------------------------\n"

    #parse model_path
    model_info = model_path.split('/')
    model_date = model_info[4]
    
     
    detail_info = model_info[7].split('_')
    
    model_sensor = detail_info[0]
    location = detail_info[2]
    yaw_degree = detail_info[-1] 

    print "\033[1;32m[model_date]  :\033[0m", model_date  + "\n"  
    print "\033[1;32m[model_sensor]:\033[0m", model_sensor + "\n"
    print "\033[1;32m[location]    :\033[0m", location + "\n"
    print "\033[1;32m[yaw_degree]  :\033[0m", yaw_degree + "\n"
    
    return (model_date , model_sensor , location , yaw_degree) 
	
	
# ###########################################
# Desc :Select Model and merge it into one 
# ############################################
def deal_with_model(model_path):
    print "\n\033[1;44m_______________Deal_With_Model_______________\033[0m"
    model_sparse_path = os.path.join(model_path,"sparse")
    
    if(os.path.exists(model_sparse_path) == False):
        print('\033[1;41m The model_path is not exists!Please cheack!\033[0m',model_sparse_path)
        exit()
        
    model_dir = os.listdir(model_sparse_path )
    #1) 1 model 
    if (len(model_dir) == 1) :
        print "\n\033[1;32mThere is only " + str(len(model_dir)) +" directories in :" + str(model_sparse_path) + "\nDon't Need to Select Or Merge!\033[0m\n" 
        print "\n\033[1;32m[Real_Model_Path] : \033[1;34m" + model_sparse_path + "\033[0m\n"
        return model_sparse_path
    
    else :
        print "\nThere are \033[1;33m" + str(len(model_dir)) +"\033[0m directories in \033[1;34m;" + str(model_sparse_path) + "\033[0m\n\033[1;44m______________SELECT_______________\033[0m\n"
        selected_dir = os.path.join(model_path,"selected")
        if (os.path.exists(selected_dir) == True) : 
            print "\033[1;34m" + str(selected_dir) + "\033[0m has existed !\n\033[1;44m______________REMOVE Selected Dir______________\033[0m\n"
            shutil.rmtree(selected_dir)
            os.mkdir( selected_dir )

        qulified_model_num = 0 
        for p in model_dir : 
            each_model_path = os.path.join(model_sparse_path , p)  
            if os.path.isdir(each_model_path): 
                size = get_dirsize(each_model_path)
                print "\033[1;32mDirectory[" + str(p)+ "]" + " size: \033[1;33m" + str(size) + "MB\033[0m"  
                if size < model_threshold_size :
                    print "\033[34;43mDirectory[" + str(p) + "]" + " is smaller than threshold_size:" + str(model_threshold_size) + "\033[0m;\n\033[34;43m;_______________IGNORE_______________\033[0m\n" 
                else :
                    dst_path = os.path.join(selected_dir,p)
                    print "\n\033[1;44m_______________COPYING_______________\033[0m\n"
                    shutil.copytree( each_model_path , dst_path )
                    qulified_model_num += 1
    # 2) more than 1 model , and after selecting still more than 1 model
    if (qulified_model_num > 1) :
        print "\n\033[1;44m_______________MERGE_______________\033[0m\n"
        merged_dir = os.path.join(model_path,"merged")
        merged_target = os.path.join(merged_dir , "0")
    
        if (os.path.exists(merged_dir)):
            shutil.rmtree(merged_dir)
               
        os.makedirs(merged_target)
        
        cmd = model_normalizer  + "/model_normalizer " + "--input " + selected_dir  + " " + "--output " + merged_target 
        (status , output) = commands.getstatusoutput(cmd)
        if( status == 0) :
            print "\n\033[1;44m_______________MERGE SUCCESS_______________\033[0m\n"
            print "\n\033[1;32m[Real_Model_Path] : \033[1;34m" + merged_dir + "\033[0m\n"
            return merged_dir 
        else :
            print "\n\033[1;41m_______________MERGE FAILED_______________\033[0m\n"
    
    else :
        print "\n\033[1;32m[Real_model_path] : \033[1;34m" + selected_dir + "\033[0m\n"
        return selected_dir
            
            
# ############################################  
# Desc :Generate testing_set & validation_set     
# ############################################   
def deal_with_testing_validation_set(test_date,location):
    print "\n\033[1;44m_______________Deal_With_Testing & Validation_Set_______________\033[0m\n"    
    test_set_name = test_date + "_" + location + "_" + default_test_sensor + "_test.txt"  
    validation_set_name = test_date + "_" + location + "_" + default_test_sensor + "_validation.txt"
    
    test_set_path = localization_root_path + "/measure_set/testing_set/"
    validation_set_path =localization_root_path + "/measure_set/validation_set/" 

    total_test_set_name = test_set_path + test_set_name 
    total_validation_set_name = validation_set_path + validation_set_name 

    print "\033[1;32m[test_set_name]       :\033[0m" , test_set_name + "\n"
    print "\033[1;32m[validation_set_name] :\033[0m" , validation_set_name + "\n"
    if( os.path.exists( total_test_set_name ) == True) : 
        print "\033[1;34m" + total_test_set_name + "\033[1;41m has existed! \033[0m\n"
        #TO DO 
        
        
        
    #else : 
    pic_path = reco_root_path + "/" + test_date + "/" + car_id + "/" 
    if(os.path.exists( pic_path ) == False ):
        print "\n\033[1;41mTest set path is not exist ! Please Check test_date or car_id !" + pic_path + "\033[0m\n"
        exit()
    pic_dirname = default_test_sensor + "_" + location +"/starneto"
    
    pic_path += pic_dirname 
    if(os.path.exists(pic_path) == False) :
        print "\n\033[1;41mStarneto set path is not exist ! Please Check location or test sensor!" + pic_path + "\033[0m\n"
        exit()
        
    print "\033[1;32m[pic_path] \033[0m:\033[1;34m" , pic_path +"\033[0m\n"
    
    # Generate test_set
    merge_5fps(pic_path , total_test_set_name) 
    
    # Generate validation_set
    shutil.copyfile(total_test_set_name,total_validation_set_name)
    
    return (total_test_set_name,total_validation_set_name)
    
    
# ###########################################
# Desc :Merge 5fps_* to 5fps and remove picture in 1fps.txt 
# ############################################
def merge_5fps(pic_path , total_test_set_name ):
    #merge 5fps_*.txt into 5fps.txt
    mergefile = os.path.join(pic_path,"5fps.txt")
    discardfile = os.path.join(pic_path,"1fps.txt")
    
    if(os.path.exists(mergefile)):
        os.remove(mergefile)
        print "\nDelete old 5fps.txt\n"
   
    if(os.path.exists(os.path.join(pic_path,"5fps_without_1fps.txt"))) :
        os.remove(os.path.join(pic_path,"5fps_without_1fps.txt"))
        print "\nDelete old 5fps_without_1fps.txt\n"

    if (os.path.exists(mergefile) == False) :
        f = open(mergefile,"a+")
        for filename in os.listdir(pic_path):
            arr = filename.split('_')
            if(arr[0] == "5fps") :
                print "Merge txt :" + filename + "\n"
                filePath = os.path.join(pic_path,filename)
                for content in open(filePath,'r'):
                    f.write(content)

        f.close()
    print "\033[1;44m_______________TXT MERGE SUCCESS_______________\033[0m\n"

    #Discard repeated pictures
    allfile = os.path.join(pic_path,'5fps.txt')
    disfile = os.path.join(pic_path,'1fps.txt')

    if (os.path.exists(total_test_set_name) == True) :
        os.remove(total_test_set_name)


    without_1fps = os.path.join(pic_path , 'without_1fps.txt')
    if (os.path.exists(without_1fps ) == True): 
        os.remove(without_1fps)

    f1 = open(allfile,'r')
    f2 = open(disfile,'r')
    f3 = open(total_test_set_name , 'a+')
    f4 = open(without_1fps,'a+')
    discard = []
    #i : to record line number of 1fps.txt 
    i = 0
    for line in f2 :
        discard.append(line)
        i += 1

    print "\n1fps.txt has\033[1;33m " + str(i) + "\033[0m lines\n"
    
    #j : to record number of discard pictures
    j = 0

    k = 0
    for line in f1 :
        if line in discard :
            j += 1
            continue
        else :
            f4.writelines(line)
            k += 1 

    print "\n5fps.txt Discard \033[1;33m" + str(j) + "\033[0m lines from 1fps.txt\n"
    f1.close()
    f2.close()

    internal = k / num_of_test_set 
    print "5fps_without_1fps.txt total line:\033[1;33m" + str(k) + "\033[0m\nSelect Internal : \033[1;33m" + str(internal) + "\033[0m\n" 
    choose = 0
    f4.close()
    f4 = open(without_1fps,'r') 
    for line in f4 :
        if (choose % internal == 0) :
            f3.writelines(line)
        choose += 1
    
    f3.close()
    f4.close()


# ###########################################
# Desc :Fill in localization task shell script 
# ############################################
def fill_in_localization_scipt(test_name , focal_type , real_model_path ,total_test_set_name,total_validation_set_name,database_path):
    print "\n\033[1;44m_______________Fill In Localization Script_______________\033[0m\n"
    localization_template_path = os.path.join(localization_task_path, 'localization_template.sh')
    if(os.path.exists(localization_template_path) == False):
        print "\n\033[1;41mLocalization_template is not exist ! Please Check!" + localization_template_path + "\033[0m\n"
        exit()
    #read localization_template.sh
    table_ = open(localization_template_path,"r").read() 
    
    #Generate today's task directory , ex.20181225
    today=str(datetime.date.today().strftime('%Y%m%d'))  
    today_dir = os.path.join(localization_task_path, today)
    if os.path.exists(today_dir) : 
        print "\nToday's work directory has exists!\n" 
    else: 
        os.mkdir(today_dir)
        
    #Generate each task directory depend on its test_name
    task_dir = os.path.join(today_dir,test_name )
    if os.path.exists(task_dir) : 
        print "\n\033[1;41mThe same task has exist ! please check your test name , change it or delete old one..." + task_dir + "\033[0m\n"
    else :
        os.mkdir(task_dir)
    
    #Fill Actual Value into Template
    name = os.path.join(task_dir,test_name) + ".sh" 
    localization_sh = open(name,"w")
    localization_sh.write(table_.replace("____index____",faiss_index).replace("____model____",real_model_path).replace("____image____",total_test_set_name).replace("____database____",database_path).replace("____focaltype____",focal_type))
    localization_sh.close()
    
    return (name,task_dir)
	
	
# ###########################################
# Desc :Run the localization script 
# ############################################
def run_localization_script(name,task_dir,total_validation_set_name):
    print "\n\033[1;44m_______________Deal With The Localization Script_______________\033[0m\n"
    cmd = 'sh ' + name + ' > ' + task_dir +'/out.log'
    print "\n\033[1;44m_______________Start running Localization script_______________\033[0m\n"
    print "CHECK : \033[1;34mtail -f " + task_dir + '/out.log\033[0m\n'
    (status, output) = commands.getstatusoutput(cmd)
    if(status == 0):
        print "\n\033[1;44m_______________Start running Grep PerfTestSuccess_______________\033[0m\n"
    else :
        print "\n\033[1;41m_______________Error occur : localization script,check the script_______________\033[0m\n"
        print "CHECK : \033[1;34mvim " + name + "\033[0m\n"
        exit()
    
    #Grep ___PerfTestSuccess___ from out.log into perf_test.txt 
    cmd = 'cat '+task_dir + '/out.log | grep ___PerfTestSuccess___ > ' + task_dir + '/perf_test.txt' 
    (status, output) = commands.getstatusoutput(cmd)
    if(status == 0):
        print "\n\033[1;44m_______________Start running distance.sh_______________\033[0m\n"
    else :
        print "\n\033[1;41m_______________Error occur : Grep PerfTestSuccess_______________\033[0m\n"
    #Run the distance.sh 
    #Output : performance.txt
    
    #Enter distance.sh directory
    os.chdir(distance_path)
    
    cmd = 'sh distance.sh '+ total_validation_set_name + ' ' + task_dir +'/perf_test.txt > ' + task_dir + '/performance.txt' 
    (status , output) = commands.getstatusoutput(cmd)  
    if(status != 0):
        print "\n\033[1;41m_______________Error occur : distance.sh_______________\033[0m\n"
        print "CHECK : validation_set : \033[1;34m"+ total_validation_set_name + "\033[0m\n"
        print "CHECK : perf_test.txt  : \033[1;34m"+ task_dir + '/perf_test.txt\033[0m\n' 
    
    print "\033[1;34mCHECK : performance.txt: cat " + task_dir + "/performance.txt\033[0m\n" 
    
    cmd = 'cat '+total_validation_set_name + ' | wc -l'
    (status , total_line) = commands.getstatusoutput(cmd)
    if(status != 0):
        print "\n\033[1;41m_______________Error occur : Calculate Validation Line__________________\n"
        exit()
    cmd = 'cat '+ task_dir + '/performance.txt'  
    (status , output) = commands.getstatusoutput(cmd)
    if(status == 0):
        print "\n\033[1;44m_______________SHOW Performance.txt_______________\033[0m\n"
        print "\033[1;45m"
        print output 
        print "total image number :" + total_line
        print "\033[0m"
    else :
        print "\n\033[1;41m_______________Error occur : performance.txt_______________\033[0m\n"
    
    #Copy accuracy.txt 
    accuracy_path = distance_path + "/accuracy.txt"
    task_accuracy_path = task_dir + "/accuracy.txt"
    shutil.copyfile(accuracy_path,task_accuracy_path) 
    print "\nCHECK accuracy.txt:\033[1;34mvim " + task_accuracy_path + "\033[0m\n"  
    
    
# ###########################################
# Desc    : Running the localization test pipeline
# Usage   : python auto_localization_test model_path database_path user
# ############################################	
if __name__ == "__main__":
    model_path = sys.argv[1]
    #database_path = sys.argv[2]
    #database_path += '/database.db'
    #user = sys.argv[3]
    user = "sth"
    (model_date , model_sensor , location , yaw_degree) = parse_model_path( model_path ,user ) 
    #print model_date , model_sensor , location , yaw_degree     

    test_sensor = default_test_sensor
    test_date = model_date
    #choose test_set depend on location
    
    #if (location == "ruanjianyuan") :
    #    print "location is ruanjianyuan1\n"
    #    test_date = "20181128"

    #elif (location == "ruanjianyuan2") :
    #    print "location is ruanjianyuan2\n"
    #    test_date = "20181129"

        
    #test name
    test_name = user + "_" + location + "_" + model_sensor + "_" + model_date + "_" + "yaw" + yaw_degree + "_" + test_sensor + "_" + test_date
    
#    real_model_path = deal_with_model(model_path)     
    
    (total_test_set_name,total_validation_set_name) = deal_with_testing_validation_set(test_date,location) 
    #real_model_path = "/nfs/project/daily_3drecon/20181212/3drecon/test_partial_ba/iphone7p_starneto_liuwandasha_1fps_100/merged"
    #total_test_set_name = "/nfs/project/localization/measure_set/testing_set/20181212_liuwandasha_iphone7p_test.txt"
    #total_validation_set_name = "/nfs/project/localization/measure_set/validation_set/20181212_liuwandasha_iphone7p_validation.txt"
        
    focal_type = "2"
    if (model_sensor == "iphone7p"):
         focal_type = "1"

#    (name,task_dir) = fill_in_localization_scipt(test_name,focal_type,real_model_path ,total_test_set_name,total_validation_set_name,database_path)
    
#    run_localization_script(name,task_dir,total_validation_set_name)
        
        


