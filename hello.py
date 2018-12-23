import os 
import subprocess

#subprocess.Popen('cat choose.py > out.log' , shell='true')
p = subprocess.Popen('cat choose.py ',shell = True,stdout = subprocess.PIPE)

stdoutput = p.communicate() 

print stdoutput
