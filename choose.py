import os
import sys 
import commands 


if __name__ == "__main__":
    path = sys.argv[1]
    
    uniquefile = os.path.join(path,'5fps_without_1fps.txt')
    
    test_set_path = "/nfs/project/localization/measure_set/testing_set"
    name = "20181210_ruanjianyuan2_iphone7p_test.txt"
    test_name = os.path.join(test_set_path , name ) 
    
    cmd = 'cat ' + uniquefile + ' | wc -l' 
    (status, output) = commands.getstatusoutput(cmd)
    print status , output

    size = 1000 
    internal = int(output) / 1000 

    print "internal:" , internal 

    f4 = open(uniquefile , 'r') 
    f5 = open(test_name , 'a+')
    index = 0 
    for line in f4 : 
        if (index % internal == 0) : 
            f5.writelines(line)
        index += 1 

    f4.close()
    f5.close() 
 
    

