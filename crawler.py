import os
import csv
import time
import sys

a=int(sys.argv[1])
file_name = str(sys.argv[2])
channel_list = file_name
with open(channel_list, 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    total_entries = 0
    count = 0
    for row in csv_reader:
        count +=1
        if count > a:
            command = "python3 crawl_link.py "+row[0]
            os.system(command)
