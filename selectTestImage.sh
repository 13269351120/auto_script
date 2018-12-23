#!/bin/bash
# This Script is used for selecting images from 5fps.txt ,and remove 1fps.txt 
# by author sthsutenghui_i@didichuxing.com

#PATH=$1

if [ -f "/nfs/project/daily_3drecon/20181211/Beijing_Buick_Q9Q3M0/iphone7p_xiaomikejiyuan/starneto/5fps_without_1fps.txt"];then 
    rm /nfs/project/daily_3drecon/20181211/Beijing_Buick_Q9Q3M0/iphone7p_xiaomikejiyuan/starneto/5fps_without_1fps.txt
fi

cat "/nfs/project/daily_3drecon/20181211/Beijing_Buick_Q9Q3M0/iphone7p_xiaomikejiyuan/starneto/5fps.txt" | while read line 
do 
    if [[ `cat "/nfs/project/daily_3drecon/20181211/Beijing_Buick_Q9Q3M0/iphone7p_xiaomikejiyuan/starneto/1fps.txt" | grep $line | wc -l` == 0 ]] ; then
        echo $line >> "/nfs/project/daily_3drecon/20181211/Beijing_Buick_Q9Q3M0/iphone7p_xiaomikejiyuan/starneto/5fps_without_1fps.txt"  
    fi
done
