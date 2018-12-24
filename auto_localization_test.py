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


#PATH
reco_root_path = "/nfs/project/daily_3drecon/"
localization_root_path = "/nfs/project/localization/"  
model_normalizer = "/home/luban/sutenghui/ar/colmap/build/src/exe"


test_model_path = "/nfs/project/daily_3drecon/20181214/3drecon/test_partial_ba/samsung_starneto_xierqizhanfanxiang_1fps_100/sparse"

#default settings
default_test_sensor = "iphone7p" 

#constant value
byte_to_Mbyte = 1024 * 1024
model_threshold_size = 20 

def get_dirsize(dirpath):
    size = 0 
    for root , dirs , files in os.walk(dirpath):
        size += sum( [os.path.getsize(os.path.join(root,name)) for name in files] )
    size /= byte_to_Mbyte
    return size 

def parse_model_path( model_path , user) :
    print "--------------------------------------------------------------------------------------------\n"
    print "model_path:" , str(model_path) 
    print "--------------------------------------------------------------------------------------------\n"

    #parse model_path
    model_info = model_path.split('/')
    model_date = model_info[4]
    
     
    detail_info = model_info[7].split('_')
    
    model_sensor = detail_info[0]
    location = detail_info[2]
    yaw_degree = detail_info[-1] 

    print "[date] , [model_sensor] , [location] , [yaw_degree] :", model_date , model_sensor , location , yaw_degree 
        
    return (model_date , model_sensor , location , yaw_degree) 
# ###########################################
# Desc :Select Model and merge it into one 
# ############################################
def deal_with_model(model_path):
    model_sparse_path = os.path.join(model_path,"sparse")
    model_dir = os.listdir(model_sparse_path )
    if (len(model_dir) == 1) :
        print "There is only " + str(len(model_dir)) +" directories in " + str(model_sparse_path) + "\n" 
    else :
        print "There are " + str(len(model_dir)) +" directories in " + str(model_sparse_path) + "\n______________SELECT_______________\n"
        selected_dir = os.path.join(model_path,"selected")
        if (os.path.exists(selected_dir) == True) : 
            print str(selected_dir) + " has existed !\n______________REMOVE______________ \n"
            shutil.rmtree(selected_dir)
            os.mkdir( selected_dir )

        qulified_model_num = 0 
        for p in model_dir : 
            each_model_path = os.path.join(model_sparse_path , p)  
            if os.path.isdir(each_model_path): 
                size = get_dirsize(each_model_path)
                print "directory[" + str(p)+ "]" + " size: " + str(size) + "MB"  
                if size < model_threshold_size :
                    print "directory[" + str(p) + "]" + " is smaller than " + str(model_threshold_size) + "\n_______________IGNORE_______________\n" 
                else :
                    dst_path = os.path.join(selected_dir,p)
                    shutil.copytree( each_model_path , dst_path )
                    qulified_model_num += 1

    if (qulified_model_num > 1) :
        print "\n_______________MERGE_______________\n"
        merged_dir = os.path.join(model_path,"merged")
        merged_target = os.path.join(merged_dir , "0")
    
        if (os.path.exists(merged_dir)):
            shutil.rmtree(merged_dir)
               
        os.makedirs(merged_target)
        
        cmd = model_normalizer  + "/model_normalizer " + "--input " + selected_dir  + " " + "--output " + merged_target 
        (status , output) = commands.getstatusoutput(cmd)
        if( status == 0) :
            print "\n_______________SUCCESS_______________\n"
            return merged_dir 
        else :
            print "\n_______________FAILED_______________\n"

# ###########################################   
# Desc :Generate testing_set & validation_set     
# ############################################   
def deal_with_testing_validation_set(test_date,location,yaw_degree):
    
    test_set_name = test_date + "_" + location + "_iphone7p_test.txt"  
    validation_set_name = test_date + "_" + location + "_iphone7p_validation.txt"
    
    test_set_path = localization_root_path + "/measure_set/testing_set/"
    validation_set_path =localization_root_path + "/measure_set/validation_set/" 

    total_test_set_name = test_set_path + test_set_name 
    total_validation_set_name = validation_set_path + validation_set_name 

    print test_set_name , validation_set_name    
    
    if( os.path.exists( total_test_set_name ) == True) : 
        print total_test_set_name + " has existed!\n"
  #  else : 
    pic_path = reco_root_path + "/" + test_date + "/Beijing_Buick+Q9Q3M0/" 
    pic_dirname = "iphone7p_" + location 
    print "pic_dirname:" , pic_dirname 
    
    pic_path += pic_dirname 
    print "pic_path :" , pic_path +"\n"
    
    merge_5fps(pic_path , test_set_path , test_set_name) 

# ###########################################
# Desc :Merge 5fps_* to 5fps and remove picture in 1fps.txt 
# ############################################
def merge_5fps(pic_path , dst_path , name ):
    #merge 5fps_*.txt into 5fps.txt
    mergefile = os.path.join(pic_path,"5fps.txt")
    discardfile = os.path.join(pic_path,"1fps.txt")
    print mergefile , discardfile
    if (os.path.exists(mergefile) == False) :
        f = open(mergefile,"a+")
        for filename in os.listdir(pic_path):
            arr = filename.split('_')
            if(arr[0] == "5fps") :
                print arr[1]
                filePath = os.path.join(pic_path,filename)
                for content in open(filePath,'r'):
                    f.write(content)

        f.close()
    print "merge end"

    #discard repeated pictures
    allfile = os.path.join(pic_path,'5fps.txt')
    disfile = os.path.join(pic_path,'1fps.txt')


    uniquefile = os.path.join(dst_path,name)
    if (os.path.exists(uniquefile) == True) :
        os.remove(uniquefile)


    f1 = open(allfile,'r')
    f2 = open(disfile,'r')
    f3 = open(uniquefile , 'a+')
    discard = []
    i = 0
    for line in discard :
        discard.append(line)
        i += 1

    print "1fps has " + str(i) + " lines"

    j = 0

    for line in f1 :
        if line in discard :
            j += 1
            continue
        else :
            f3.writelines(line)

    print "discard " + str(j) + " lines"
    f1.close()
    f2.close()
    f3.close()


     

if __name__ == "__main__":
    model_path = sys.argv[1] 
    user = sys.argv[2]
    (model_date , model_sensor , location , yaw_degree) = parse_model_path( model_path  , user) 
    print model_date , model_sensor , location , yaw_degree     

    #test name
    test_sensor = default_test_sensor
    test_date = model_date
    #choose test_set depend on location
    if (location == "ruanjianyuan") :
        print "location is ruanjianyuan1\n"
        test_date = "20181128"

    elif (location == "ruanjianyuan2") :
        print "location is ruanjianyuan2\n"
        test_date = "20181129"

    else :
        print "other places!\n"

    test_name = user + "_" + location + "_" + model_sensor + "_" + model_date + "_" + "yaw" + yaw_degree + "_" + test_sensor + "_" + test_date
    print "test name is :" +  test_name + "\n"
 
    #merged_dir = deal_with_model(model_path)     
    deal_with_testing_validation_set(test_date,location,yaw_degree) 
    


