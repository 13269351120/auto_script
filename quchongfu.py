import os 
import sys 

if __name__ == "__main__":
    path = sys.argv[1]
    allfile = os.path.join(path,'5fps.txt')
    disfile = os.path.join(path,'1fps.txt')
    
    uniquefile = os.path.join(path,'5fps_without_1fps.txt')
    

    f1 = open(allfile,'r')
    f2 = open(disfile,'r')
    f3 = open(uniquefile , 'a+')
    l2 = []
    for line in f2 :
        l2.append(line) 


    for line in f1 :
        if line in l2 :
            continue 
        else : 
            f3.writelines(line)

    f1.close()
    f2.close()
    f3.close()
