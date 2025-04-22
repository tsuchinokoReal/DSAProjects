import csv
import datetime
from HashTable import *
from Package import *
from Truck import *

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
    with open("address_file.csv", encoding='utf-8-sig') as f:
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

    #parse data from the csv file. Time-complexity: O(N) where n is the number of rows
def read_distance():
    with open('distance_data.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            distances.append(row)
    return distances


#finding the best route for trucks
def best_route(truck):
    unvisited = truck.packages.copy()
    route = []
    currentAddress = truck.address

    while unvisited:
        # Find the closest package to current address
        nearest_package_id = min(unvisited, key=lambda pid: get_distance(currentAddress, lookup(pid).address))
        nearest_package = lookup(nearest_package_id)
        route.append(nearest_package_id)
        currentAddress = nearest_package.address
        unvisited.remove(nearest_package_id)

    return route

#retrieves distance between two locations using the distance matrix. time complexity = O(1)
def get_distance(truckAddress, packageAddress):
    try:
        distance = distances[truckAddress][packageAddress]
        if distance == '' or distance is None:
            distance = distances[packageAddress][truckAddress]
        return float(distance)
    except Exception as e:
        print(f"Error: {e}")

load_addresses()
parsedPackages = load_package()
distanceData = read_distance()

def init(truck):
    route = best_route(truck)
    currentAddress = truck.address

    for packageID in route:
        package = lookup(packageID)
        if package:
            # Dynamic reroute for package 9 at 10:20 AM
            if truck.time >= datetime.timedelta(hours=10, minutes=20) and package.id == '9':
                package.address = addressDict["410 S State St"]
                # Recalculate the route from current package forward
                remaining_packages = [pid for pid in route[route.index(packageID):] if pid != package.id]
                new_truck_state = Truck(remaining_packages, currentAddress, truck.miles, truck.time, truck.truckID)
                route = [package.id] + best_route(new_truck_state)

            distance = get_distance(currentAddress, package.address)
            truck.miles += distance
            truck.time += datetime.timedelta(minutes=(distance / 0.3))
            print(f"Truck {truck.truckID} delivered package {package.id} at {truck.time}")

            currentAddress = package.address
            package.time_delivered = truck.time
            package.truckID = truck.truckID

    # Return to hub
    hub = addressDict["4001 South 700 East"]
    distance_to_hub = get_distance(currentAddress, hub)
    truck.miles += distance_to_hub
    truck.time += datetime.timedelta(minutes=(distance_to_hub / 0.3))
    truck.miles = float(f"{truck.miles:.1f}")

#instantiate trucks
truck1 = Truck(packages=[str(a) for a in [15, 13, 14, 1, 16, 19, 20, 29, 30, 31, 34, 37, 40]], address=addressDict["4001 South 700 East"], miles=0, time=datetime.timedelta(hours=8), truckID=1)

truck2Packages = [str(b) for b in [6, 25, 18, 22, 23, 3, 27, 28, 32, 33, 35, 36, 38]]
truck2 = Truck(truck2Packages, addressDict["4001 South 700 East"], 0, datetime.timedelta(hours=9, minutes=5), 2)

truck3Packages = [str(c) for c in [2, 4, 5, 7, 8, 9, 10, 11, 12, 17, 21, 24, 26, 39]]
truck3 = Truck(truck3Packages, addressDict["4001 South 700 East"], 0, datetime.timedelta(hours=10, minutes=10), 3)

    #assign packages to trucks based on notes. Time complexity O(N^2)
def sort_packages(parsedPackages, trucks):
    try:
        for package in parsedPackages.values():
            assigned = False
            specialNotes = package.notes
            deliveryTime = package.deliveryTime

            #assign to trucks based on special conditions
            if "Can only be on truck 2" in specialNotes:
                trucks[1].packages.append(package)
                assigned = True
            elif "Must be delivered with" in specialNotes:
                pairPackages = [id.strip() for id in specialNotes.split("Must be delivered with")[1].split(",")]
                for extractIDs in pairPackages:
                    related_package = parsedPackages.get(extractIDs.strip())
                    if related_package:
                        trucks[0].packages.append(related_package)
                trucks[0].packages.append(package)
                assigned = True
            elif "Delayed on flight---will not arrive to depot until 9:05 am" in specialNotes:
                trucks[1].packages.append(package)
                assigned = True
            elif "Wrong address listed" in specialNotes:
                trucks[2].packages.append(package)
                assigned = True
            elif "EOD" in deliveryTime:
                trucks[2].packages.append(package)
                assigned = True
            if not assigned:
                trucks[2].packages.append(package)
    except Exception as e:
        print(f"Exception: {e}")

trucks = [None, truck1, truck2, truck3]

def run():
    init(truck1)
    init(truck2)
    init(truck3)

    def interface():
        print('Package Parcel Delivery Service')
    print('**********************')
    totalmiles = round(truck1.miles + truck2.miles + truck3.miles, 2)
    print(f"Route completed in: {totalmiles} miles")
    print(f"Truck 1 miles: {truck1.miles}")
    print(f"Truck 2 miles: {truck2.miles}")
    print(f"Truck 3 miles: {truck3.miles}")
    print('**********************')

    while True:
        print("\nEnter a command (1-3):")
        print("1. Display specific package")
        print("2. Display all package status")
        print("3. Exit")

        try:
            selectedNum = int(input("> "))
        except ValueError:
            print("Invalid input. Please enter 1, 2, or 3.")
            continue

        if selectedNum == 1:
            packageId = input('Enter a Package ID (1-40): ')
            timestamp = input('Enter a time in HH:MM format: ')
            h, m = map(int, timestamp.split(':'))
            user_time = datetime.timedelta(hours=h, minutes=m)

            # fetch package
            tempStorage = lookup(packageId)
            address = reverseAddressDict.get(tempStorage.address, "Unknown")
            if tempStorage.id == '9':
                address = "410 S State St" if user_time >= datetime.timedelta(hours=10, minutes=20) else "300 State St"

            truck_departure = {
                1: datetime.timedelta(hours=8),
                2: datetime.timedelta(hours=9, minutes=5),
                3: datetime.timedelta(hours=10, minutes=10)
            }.get(tempStorage.truckID, datetime.timedelta(0))

            # determine status
            if user_time <= truck_departure:
                status = "at hub"
                delivered_time = "--"
            elif not tempStorage.time_delivered or user_time < tempStorage.time_delivered:
                status = "en route"
                delivered_time = "--"
            else:
                status = "delivered"
                delivered_time = str(tempStorage.time_delivered)

            print("\nPackage Details:")
            print("-" * 70)
            print(f"{'Package ID:':20} {tempStorage.id}")
            print(f"{'Leaves Hub At:':20} {truck_departure}")
            print(f"{'Status:':20} {status}")
            print(f"{'Deadline:':20} {tempStorage.delivery_time}")
            print(f"{'Delivery Address:':20} {address}")
            print(f"{'Time Delivered:':20} {delivered_time}")
            print(f"{'Truck ID:':20} {tempStorage.truckID}")
            print("-" * 70)

        elif selectedNum == 2:
            timestamp = input('Enter a time in HH:MM format: ')
            h, m = map(int, timestamp.split(':'))
            query_time = datetime.timedelta(hours=h, minutes=m)

            print(f"\nStatus of all packages at {timestamp}")
            print("-" * 110)
            print(f"{'ID':<5} {'Address':<35} {'Leaves Hub':<15} {'Status':<12} {'Deadline':<12} {'Delivered At':<15} {'Truck':<6}")
            print("-" * 110)

            for Package in parsedPackages.values():
                address = reverseAddressDict.get(Package.address, "Unknown")
                if Package.id == '9':
                    address = "410 S State St" if query_time >= datetime.timedelta(hours=10, minutes=20) else "300 State St"

                truck_departure = {
                    1: datetime.timedelta(hours=8),
                    2: datetime.timedelta(hours=9, minutes=5),
                    3: datetime.timedelta(hours=10, minutes=10)
                }.get(Package.truckID, datetime.timedelta(0))

                if query_time <= truck_departure:
                    status = "at hub"
                    delivered_time = "--"
                elif not Package.time_delivered or query_time < Package.time_delivered:
                    status = "en route"
                    delivered_time = "--"
                else:
                    status = "delivered"
                    delivered_time = str(Package.time_delivered)

                print(f"{Package.id:<5} {address:<35} {str(truck_departure):<15} {status:<12} {str(Package.delivery_time):<12} {delivered_time:<15} {Package.truckID:<6}")

            print("-" * 110)

        elif selectedNum == 3:
            print("Exiting program...")
            break

        else:
            print("Invalid command, please try again.")