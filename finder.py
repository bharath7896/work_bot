import os
import json
import re
import sys
from datetime import datetime
from threading import Thread
import pandas as pd

dict1 = {}


def get_drives():
	response = os.popen("wmic logicaldisk get caption")
	list1 = []
	total_file = []
	t1= datetime.now()
	for line in response.readlines():
		line = line.strip("\n")
		line = line.strip("\r")
		line = line.strip(" ")
		if (line == "Caption" or line == ""):
			continue
		list1.append(line)
	return list1
	

def search1(drive):
	for root, dir, files in os.walk(drive, topdown = True):
		for file in files:
			file= file.lower()
			if file in dict1:
				file = file+"_1"
				dict1[file]= root
			else :
				dict1[file]= root
				

def create():
	t1= datetime.now()
	list2 = []   # empty list is created	
	list1 = get_drives()
	print(list1)
	for each in list1:
		process1 = Thread(target=search1, args=(each,))
		process1.start()
		list2.append(process1)
		  
	for t in list2:
		t.join() # Terminate the threads
	pd.DataFrame(dict1).to_json('file_data.json')
	t2= datetime.now()
	total =t2-t1
	print("Time taken to create ", total)


if len(sys.argv) < 2 or len(sys.argv) > 2:
	print("Please use proper format")
	print("Use <finder -c >  to create database file")
	print("Use <finder file-name> to search file")

elif sys.argv[1] == '-c':
	create()	
	
else:
	t1= datetime.now()
	try:
		file_dict = pd.read_json('file_data.json').to_dict()
	except IOError:
		create()
	except Exception as e:
		print(e)
		sys.exit()
	file_to_be_searched = sys.argv[1].lower()
	list1= []
	print("Path \t\t: File-name")
	for key in file_dict.keys():
		if re.search(file_to_be_searched, key):
			str1 = file_dict[key]+" : "+key
			list1.append(str1)
	list1.sort()
	for each in list1:
		print(each)
		print("---------------------------------")
	t2= datetime.now()
	total =t2-t1
	print("Total files are", len(list1))
	print("Time taken to search ", total)

		

