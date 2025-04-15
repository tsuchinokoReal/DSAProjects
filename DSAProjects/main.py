import csv
import datetime
from HashTable import *
from Package import *
from Truck import *
from collections import deque
from itertools import permutations
from tabulate import tabulate
from colorama import Fore, Style
import random
import heapq

#inits
#empty forwards and reverse address dicts
addressDict = {}
reverseAddressDict = {}
#distance array
distances = []
#HashTable
parsed_packages = HashTable()


#hashtable lookup by ID. time complexity = O(1)
def lookup(id):
    return parsed_packages.search(id)

def load_addresses():
    with open("address_file", encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            index = int(row[0])
            address = row[2]
            addressDict[address] = index
            reverseAddressDict[index] = address

#parse file and add to dict. Time complexity: O(N) where n is the number of rows
def load_package():
    try:
        with open('package_file.csv', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            for row in reader:
                address_index = addressDict.get(row[1].strip(), 0)

                newpackage = Package(
                    id=row[0].strip(),
                    address=address_index,
                    city=row[2].strip(),
                    state=row[3].strip(),
                    zip=row[4].strip(),
                    delivery_time=row[5].strip(),
                    weight=row[6].strip(),
                    notes=row[7].strip(),
                    status= "At hub"
                )
                parsed_packages.insert(newpackage.id, newpackage)
        return parsed_packages
    except Exception as e:
        print(f"Error parsing packages: {e}")
        return None

