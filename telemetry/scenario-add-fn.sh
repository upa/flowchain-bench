#!/bin/bash

add="localhost:5000/override/45.0.80.1/32/none/none/user-global"
del="localhost:5000/delete/45.0.80.1/32"

interval=20

echo `date +%s` Start
sleep $interval


echo `date +%s` add fn1
http GET ${add}/fp1-fn1
sleep $interval


echo `date +%s` add fn2
http GET ${add}/fp1-fn1_fp1-fn2
sleep $interval


echo `date +%s` add fn3
http GET ${add}/fp1-fn1_fp1-fn2_fp1-fn3
sleep $interval


echo `date +%s` remove fn1
http GET ${add}/fp1-fn2_fp1-fn3
sleep $interval


echo `date +%s` remove fn2
http GET ${add}/fp1-fn3
sleep $interval


echo `date +%s` remove all
http GET ${del}
sleep $interval
