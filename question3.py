import sys
from pyspark import SparkContext
import time
from definition import *

# start timer
start = time.time()

# start spark with 1 worker thread
sc = SparkContext("local[1]")
sc.setLogLevel("ERROR")

# Question 3____________________________________________________________start

# number of files in table
nb_of_files = 2;

# declare an empty RDD for containing data from all files of a table
job_events_RDD_combined = sc.parallelize([])

# read all of input files into an RDD[String]
for i in range(nb_of_files):
   job_events_RDD = sc.textFile("./Job_events/part-00" + standardizeToStr(i) + "-of-00500.csv")
   job_events_RDD_combined = job_events_RDD_combined.union(job_events_RDD)

# sum of elements(machines)
sum_of_elements = job_events_RDD_combined.count()

# transformation to a new RDD with spliting each line into an array of items
job_events_RDD_combined = job_events_RDD_combined.map(lambda x: x.split(','))

# transformation to a new RDD with each line contains a <the scheduling_class,1> pair
scheduling_class_RDD = job_events_RDD_combined.map(lambda x: (x[Job_events_table.SCHEDULING_CLASS],1))

# return a hashmap with the count of each key
hashmap_scheduling_class = scheduling_class_RDD.countByKey()

# return as a dictionary
dict_scheduling_class = dict(hashmap_scheduling_class)

# iterate each element in dictionary
for key in dict_scheduling_class:
    # empty key is not valid 
    if key != '':
        print("Percentage of jobs correspond with scheduling class =", key ,"is", round(dict_scheduling_class[key]/sum_of_elements * 100 , 2) ,
         "%  " , dict_scheduling_class[key],"of",sum_of_elements)

# end timer
end = time.time()

print("elapsed time:  " , end-start)

# Question 3______________________________________________________________end

input("Press Enter to continnnue...")
