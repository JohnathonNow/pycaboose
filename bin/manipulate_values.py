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
        found_it = False
        for i in files:
            if i == filename:
                found_it = True
                break
        if found_it:
            try:
                db = pycaboose.database.Database(f=filename)
            except Exception as e:
                print(e)
                print(
                    "The error is probably too much space after the flag in your script, remove it and re-run this program")
            return db
        else:
            print("File not found >:(")
            exit()
            return None

    def print_db(db):
        print("\n{w}KEY{e}\t{green}|{e}\t{w}VALUE{e}\n{green}--------+------------{e}".format(w=bcolors.WARNING,e=bcolors.ENDC,green=bcolors.OKGREEN,))
        for key, value in db._db.items():
            print("{k}\t{g}|{e}\t{v} ".format(k=key,v=value.value,g=bcolors.OKGREEN,e=bcolors.ENDC))

    def add_to_db(db, input_data):  # input data::(line,data)
        db.write(input_data[0], input_data[1])

    def import_csv(db, csv_file_path):
        try:
            with open(csv_file_path, "r") as f:
                content = f.read()
            content = content.strip().split("\n")
            for i in content:
                add_to_db(
                    db, [
                        i.split(",")[0].strip(), i.split(",")[1].strip()])

        except Exception as e:
            print(e)
            print("Bad Error has occured. Do you want to throw a masterball at it? jk")

    def delete_value(filename, db, key):
        try:
            # print(str(db._db[key].comment))

            with open(filename, "r") as file:
                contents = file.read()

            contents = contents.replace(str(db._db[key].comment)[2:-3], "")
            # print(str(db._db[key].comment)[2:-3])
            with open(filename, "w") as f:
                f.write(contents.rstrip() + "\n")

            del db._db[key]
            print("{a}Deleted sucessfully!{b}".format(a=bcolors.WARNING,b=bcolors.ENDC))

        except BaseException as e:
            print(e) 
            print("Element did't exist in database.")

    def print_help():
        print("{a}{b}\t--- HELP ---{c} ".format(a=bcolors.WARNING,b=bcolors.BOLD,c=bcolors.ENDC))
        print("{a}-l {b} --> list all Values in database ".format(a=bcolors.FAIL,b=bcolors.ENDC))
        print("{a}-a (line, data) {b} --> add a Value to the database ".format(a=bcolors.FAIL,b=bcolors.ENDC))
        print("{a}-d (key) {b} --> delete value from database, key is the creation line".format(a=bcolors.FAIL,b=bcolors.ENDC))
        print("{a}-h {b} --> show this help menu".format(a=bcolors.FAIL,b=bcolors.ENDC))
        print("{a}-i (csv_file_path){b} --> import csv file".format(a=bcolors.FAIL,b=bcolors.ENDC))
        print("{a}-q {b} --> quit this application".format(a=bcolors.FAIL,b=bcolors.ENDC))

    filename = "test_pycaboose.py"
    flag = "# pycaboose #"

    print("\n\t{a}{b} EDIT PYCABOOSE{c}\n           -h for help   \n -------------------------------".format(a=bcolors.OKGREEN,b=bcolors.BOLD,c=bcolors.ENDC))
    if len(sys.argv) == 1:
        filename = input("Enter filename to edit database on: ")
    else:
        filename = sys.argv[1]

    if not filename[-3:] == ".py":
        filename += ".py"

    # setting up data_base
    db = setup_db(filename)
    # dictionary of commands

    while True:
        user_input = input("--> ").strip()
        if user_input == "-h":
            print_help()
        elif user_input[:2] == "-a":
            try:
                inserting_data = user_input[2:].strip().split(" ")
                # print("inserting_data",inserting_data)
                add_to_db(db, inserting_data)
            except BaseException:
                print("Wrong syntax.\nDo {a}-h{b}--> for help ".format(a=bcolors.FAIL,b=bcolors.ENDC))
        elif user_input[:2] == "-l":
            print_db(db)
        elif user_input[:2] == "-d":
            inserting_data = user_input[2:].strip().split(" ")[0]
            delete_value(filename, db, inserting_data)
        elif user_input[:2] == "-q":
            print("Application shutting off.")
            exit()
        elif user_input[:2] == "-i":  # add to help
            import_csv(db, user_input[2:].strip().split(" ")[0])
        else:
            print("This command is not valid.\n")


if __name__ == "__main__":
    main()
