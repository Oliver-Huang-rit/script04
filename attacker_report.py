#!/usr/bin/env python3
# Author: Oliver Huang
# Date: 10/14/2021

import os
import sys
from os import system, name
from datetime import date
import subprocess
import csv
import re
import time
from subprocess import check_output
 

FAILED_INDEX = 5
IP_INDEX = 10

# this function to clear the terminal
def clear_terminal():
    if name == 'nt': # if the system is Windows
        _ = system('cls')
    else: # if is other system
        _ = system('clear')

# this function to read the data from the csv file
def readFile(filename):
    try:
        with open(filename) as new_file:
            reader = new_file.readlines()
            return reader
        return None
    except:
        return None

# this function determine wether the line has a valid ip address
def valid_ip(current):
    regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    for i in range(0, len(current)):
        if(re.search(regex, current[i])):
            return current[i]
    return None

# this function find the country origin of the IP address
def find_country(ip_addr):
    return None

# this function return an instruction about the order
# of the ip address the script should print in
def get_instruction_for_print(attackers_file):
    keys = attackers_file.keys()
    temp1 = {}
    temp2 = []
    for key in keys:
        current_count = (attackers_file[key])[0]
        if current_count not in temp1.keys():
            new_list = [key]
            temp1[current_count] = new_list
            temp2.append(current_count)
        else:
            (temp1[current_count]).append(key)
    temp2.sort()
    temp3 = []
    for i in range(0, len(temp2)):
        current_list = temp1[temp2[i]]
        for i in range(0, len(current_list)):
            temp3.append(current_list[i])
    return temp3

# this function print the report
def print_report(instruction, attackers_file):
    print("\033[32mAttacker Report\033[0m -", date.today(), "\n")
    table_data = []
    print("\033[31mCOUNT\tMORE/EQUAL -> 10\tIP ADDRESS\ttCOUNTRY\033[0m")
    for i in range(0, len(instruction)):
        temp_list = []
        temp_list.append((str)((attackers_file[instruction[i]])[0]))
        if (attackers_file[instruction[i]])[0] >= 10:
            temp_list.append("True")
        else:
            temp_list.append("False")
        temp_list.append((str)(instruction[i]))
        temp_list.append((str)((attackers_file[instruction[i]])[1]))
        table_data.append(temp_list)
    for row in table_data:
        print("{: <20} {:<20} {:<20} {:<20}".format(*row))

def main():
    clear_terminal()
    reader = readFile("syslog.log")
    
    if reader == None:
        print("ERROR: could not open the file")
    else:
        attackers_file = {}
        for line in reader:
            current = line.split(" ")
            ip_addr = valid_ip(current)
            if ip_addr != None:
                if ip_addr not in attackers_file.keys():
                    country = find_country(ip_addr)
                    new_list = [1, country]
                    attackers_file[ip_addr] = new_list
                else:
                    (attackers_file[ip_addr])[0] += 1
        clear_terminal()
        instruction = get_instruction_for_print(attackers_file)
        print_report(instruction, attackers_file)

main()