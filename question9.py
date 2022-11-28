import sys
import random
from pyspark import SparkContext
import time
from definition import *
from functools import reduce

# start timer
start = time.time()

# Finds out the average of elements in the list lst
def computeAverage(lst):
	return reduce(lambda a, b: a + b, lst) / len(lst)

# convert string value of CPU request to float
def convertCpuValueToFloat(lst):
   # ignore elements having missing infor about CPU request
   if lst[Task_events_table.CPU_REQUEST] != "" :
      return float(lst[Task_events_table.CPU_REQUEST])
   else:
      return "";

# convert string value of MEMORY request to float
def convertMemValueToFloat(lst):
   # ignore elements having missing infor about MEM request
   if lst[Task_events_table.MEMORY_REQUEST] != "" :
      return float(lst[Task_events_table.MEMORY_REQUEST])
   else:
      return "";



def func(a,b):
    global temp
    if a == '' and b == '':
        return 0
    elif a == '' and b != '':
        return float(b)
    elif b == '' and a != '':
        return float(a)
    else:
        temp += 1
        print("temp", temp)
        return float(a) + float(b)



# start spark with 1 worker thread
sc = SparkContext("local[1]")
sc.setLogLevel("ERROR")

# Question 9____________________________________________________________start

# number of files in table
nb_of_files = 1

temp = 1

# declare an empty RDD for containing data from all files of a table
task_events_RDD_combined = sc.parallelize([])

# read all of input files into an RDD[String]
for i in range(nb_of_files):
   task_events_RDD = sc.textFile("./Task_events/part-00" + standardizeToStr(i) + "-of-00500.csv")
   task_events_RDD_combined = task_events_RDD_combined.union(task_events_RDD)

# transformation to a new RDD with spliting each line into an array of items
task_events_RDD_combined = task_events_RDD_combined.map(lambda x: x.split(','))

# transformation to a new RDD with each line has only the priority field
priority_RDD = task_events_RDD_combined.map(lambda x: (x[Task_events_table.PRIORITY],x[Task_events_table.CPU_REQUEST]))

priority_RDD = sc.parallelize([('8', ''), ('8', '1'), ('8', '0.5'),('8', ''), ('8', '0.25'), ('8', '0.5')])

reduce_prio_RDD = priority_RDD.reduceByKey(func)

print("reduce: " , reduce_prio_RDD.collect(), "temp: ", temp)

# end timer
end = time.time()

print("elapsed time:  " , end-start)

# Question 9______________________________________________________________end

input("Press Enter to continnnue...")
