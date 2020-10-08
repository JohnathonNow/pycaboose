#!/usr/bin/env python3

import pycaboose
from pycaboose import database
import sys 
import os

def main():
	class bcolors:
	    HEADER = '\033[95m'
	    OKBLUE = '\033[94m'
	    OKGREEN = '\033[92m'
	    WARNING = '\033[93m'
	    FAIL = '\033[91m'
	    ENDC = '\033[0m'
	    BOLD = '\033[1m'
	    UNDERLINE = '\033[4m'

	def setup_db(filename):
		files = [f for f in os.listdir('.') if os.path.isfile(f)]
		found_it=False
		for i in files:
			if i==filename:
				found_it=True
				break
		if found_it:
			try:
				db=pycaboose.database.Database(f=filename)
			except Exception as e:
				print(e)
				print("The error is probably too much space after the flag in your script, remove it and re-run this program")
			return db
		else:
			print("Pls dont input shit, you cant scam me..")
			exit()
			return None
	def print_db(db):
		print(f"\n{bcolors.WARNING}KEY{bcolors.ENDC}\t{bcolors.OKGREEN}|{bcolors.ENDC}\t{bcolors.WARNING}VALUE{bcolors.ENDC}\n{bcolors.OKGREEN}--------+------------{bcolors.ENDC}")
		for key,value in db._db.items():
			print(f"{key}\t{bcolors.OKGREEN}|{bcolors.ENDC}\t{value.value} ")

	def add_to_db(db,input_data):#input data::(line,data)
		db.write(input_data[0],input_data[1])

	def import_csv(db,csv_file_path):
		try:
			with open(csv_file_path,"r") as f:
				content=f.read()
			content=content.strip().split("\n")
			for i in content:
				add_to_db(db,[i.split(",")[0].strip(),i.split(",")[1].strip()])


		except Exception as e:
			print(e)
			print("Bad Error has occured. Do you want to throw a masterball at it? jk")
	def delete_value(filename,db,key):
		try:
		#print(str(db._db[key].comment))
			
			with open(filename,"r") as file:
				contents=file.read()

			contents=contents.replace(str(db._db[key].comment)[2:-3],"")
			#print(str(db._db[key].comment)[2:-3])
			with open(filename,"w") as f:
				f.write(contents.rstrip()+"\n")


			del db._db[key]
			print(f"{bcolors.WARNING}Deleted sucessfully!{bcolors.ENDC}")



		except:
			print("Element did't exist in database.")
	def print_help():
		print(f"{bcolors.WARNING}{bcolors.BOLD}\t--- HELP ---{bcolors.ENDC} ")
		print(f"{bcolors.FAIL}-l {bcolors.ENDC} --> list all Values in database ")
		print(f"{bcolors.FAIL}-a (line, data) {bcolors.ENDC} --> add a Value to the database ")
		print(f"{bcolors.FAIL}-d (key) {bcolors.ENDC} --> delete value from database, key is the creation line")
		print(f"{bcolors.FAIL}-h {bcolors.ENDC} --> show this help menu")
		print(f"{bcolors.FAIL}-i (csv_file_path){bcolors.ENDC} --> import csv file")
		print(f"{bcolors.FAIL}-q {bcolors.ENDC} --> quit this application")



	filename="test_pycaboose.py"
	flag="# pycaboose #"
	

	print(f"\n\t{bcolors.OKGREEN}{bcolors.BOLD} EDIT PYCABOOSE{bcolors.ENDC}\n           -h for help   \n -------------------------------")
	if len(sys.argv)==1:
		filename=input("Enter filename to edit database on: ")
	else:
		filename=sys.argv[1]

	if not filename[-3:]==".py":
		filename+=".py"

	
	#setting up data_base
	db=setup_db(filename)
	#dictionary of commands

	while 1:
		user_input=input("--> ").strip()
		if user_input=="-h":
			print_help()
		elif user_input[:2]=="-a":
			try:
				inserting_data=user_input[2:].strip().split(" ")
				#print("inserting_data",inserting_data)
				add_to_db(db,inserting_data)
			except:
				print(f"Wrong syntax.\nDo {bcolors.FAIL}-h{bcolors.ENDC}--> for help ")
		elif user_input[:2]=="-l":
			print_db(db)
		elif user_input[:2]=="-d":
			inserting_data=user_input[2:].strip().split(" ")[0]
			delete_value(filename,db,inserting_data)
		elif user_input[:2]=="-q":
			print("Application shutting off.")
			exit()
		elif user_input[:2]=="-i":#add to help
			import_csv(db,user_input[2:].strip().split(" ")[0])
		else:
			print("This command is not valid.\n")





if __name__=="__main__":
	main()
