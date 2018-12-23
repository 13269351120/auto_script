#
# -*- coding: utf-8 -*- 
# This Script is used to merge 5fps_00 5fps_01 ... to 5fps.txt
# by author sthsutenghui_i@didichuxing.com

import os 
import sys
import commands 

if __name__ == "__main__": 
    PATH = sys.argv[1]
    print PATH
    mergefile = os.path.join(PATH,"5fps.txt")
    discardfile = os.path.join(PATH,"1fps.txt")
    print mergefile , discardfile 
    if (os.path.exists(mergefile) == False) :
        f = open(mergefile,"a+") 
        for filename in os.listdir(PATH):
            arr = filename.split('_')
            if(arr[0] == "5fps") :
                print arr[1]
                filePath = os.path.join(PATH,filename) 
                for content in open(filePath,'r'):
                    f.write(content)

        f.close()
    print "merge end"

    path = PATH 
    allfile = os.path.join(path,'5fps.txt')
    disfile = os.path.join(path,'1fps.txt')

    uniquefile = os.path.join(path,'5fps_without_1fps.txt')


    f1 = open(allfile,'r')
    f2 = open(disfile,'r')
    f3 = open(uniquefile , 'a+')
    l2 = []
    i = 0 
    for line in f2 :
        l2.append(line)
        i += 1 

    print "1fps has " + str(i) + " lines"  

    j = 0 

    for line in f1 :
        if line in l2 :
            j += 1
            continue
        else :
            f3.writelines(line)
    

    print "discard " + str(j) + " lines"
    f1.close()
    f2.close()
    f3.close()

    
    
     
