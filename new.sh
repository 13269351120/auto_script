#/bin/bash

cat "/nfs/project/daily_3drecon/20181211/Beijing_Buick_Q9Q3M0/iphone7p_shangqinyuan/starneto/5fps.txt" | awk {
if [[ `cat "/nfs/project/daily_3drecon/20181211/Beijing_Buick_Q9Q3M0/iphone7p_shangqinyuan/starneto/1fps.txt" | grep $0 | wc -l` == 0  ]] ; then 
print $0 
fi 
}
