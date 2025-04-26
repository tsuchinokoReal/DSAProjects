#011975117
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

#retrieves distance between two locations using the distance matrix. time complexity = O(1)
def get_distance(truck_address, package_address):
    try:
        distance = distances[truck_address][package_address]
        if distance == '' or distance is None:
            distance = distances[package_address][truck_address]
        return float(distance)
    except Exception as e:
        print(f"Error: {e}")

#hashtable lookup by ID. time complexity = O(1)
def lookup(id):
    return parsed_packages.search(id)

#parse file and add to hash table. Time complexity: O(N) where n is the number of rows
def load_package():
    try:
        with open('package_file.csv', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            for row in reader:
                address_index = addressDict.get(row[1].strip(), 0)

                new_package = Package(
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
                parsed_packages.insert(new_package.id, new_package)
        return parsed_packages
    except Exception as e:
        print(f"Error parsing packages: {e}")
        return None

#reads the address file and builds dictionaries for faster lookup. time complexity = O(N)
def load_addresses():
    with open("address_file.csv", encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            index = int(row[0])
            address = row[2]
            addressDict[address] = index
            reverseAddressDict[index] = address

#loads the distance matrix from file into memory. Time-complexity: O(N) where n is the number of rows
def read_distance():
    with open('distance_data.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            distances.append(row)
    return distances

#finding the best route for trucks. time complexity: O(N^2) - greedy algorithm loop through all unvisited packages
def best_route(truck):
    unvisited = truck.packages.copy()
    route = []
    current_address = truck.address

    while unvisited:
        #find the closest package to current address
        nearest_package_id = min(unvisited, key=lambda pid: get_distance(current_address, lookup(pid).address))
        nearest_package = lookup(nearest_package_id)
        route.append(nearest_package_id)
        current_address = nearest_package.address
        unvisited.remove(nearest_package_id)

    return route

#initialization
load_addresses()
parsedPackages = load_package()
distanceData = read_distance()

#simulates package delivery by a truck using its route. time complexity = O(N^2)
def init(truck):
    route = best_route(truck)
    current_address = truck.address

    for packageID in route:
        package = lookup(packageID)
        if package:
            #dynamic reroute for package 9 at 10:20 AM
            if truck.time >= datetime.timedelta(hours=10, minutes=20) and package.id == '9':
                package.address = addressDict["410 S State St"]
                #recalculate the route
                remaining_packages = [pid for pid in route[route.index(packageID):] if pid != package.id]
                new_truck_state = Truck(remaining_packages, current_address, truck.miles, truck.time, truck.truckID)
                route = [package.id] + best_route(new_truck_state)

            distance = get_distance(current_address, package.address)
            truck.miles += distance
            truck.time += datetime.timedelta(minutes=(distance / 0.3))
            print(f"Truck {truck.truckID} delivered package {package.id} at {truck.time}")

            current_address = package.address
            package.delivered = truck.time
            package.truckID = truck.truckID

    hub = addressDict["4001 South 700 East"]
    distance_to_hub = get_distance(current_address, hub)
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
def sort_packages(parsed_packages, trucks):
    try:
        for package in parsed_packages.values():
            assigned = False
            special_notes = package.notes
            delivery_time = package.deliveryTime

            #assign to trucks based on special conditions
            if "Can only be on truck 2" in special_notes:
                trucks[1].packages.append(package)
                assigned = True
            elif "Must be delivered with" in special_notes:
                pair_packages = [id.strip() for id in special_notes.split("Must be delivered with")[1].split(",")]
                for extractIDs in pair_packages:
                    related_package = parsed_packages.get(extractIDs.strip())
                    if related_package:
                        trucks[0].packages.append(related_package)
                trucks[0].packages.append(package)
                assigned = True
            elif "Delayed on flight---will not arrive to depot until 9:05 am" in special_notes:
                trucks[1].packages.append(package)
                assigned = True
            elif "Wrong address listed" in special_notes:
                trucks[2].packages.append(package)
                assigned = True
            elif "EOD" in delivery_time:
                trucks[2].packages.append(package)
                assigned = True
            if not assigned:
                trucks[2].packages.append(package)
    except Exception as e:
        print(f"Exception: {e}")

#add trucks
trucks = [None, truck1, truck2, truck3]

#inits and executes delivery sim for all trucks. time complexity = O(3N^2) => O(N^2) - because it calls init() for each truck
def run():
    init(truck1)
    init(truck2)
    init(truck3)

#cli for package status by time, waits for user input. time complexity = O(N) for each listing in option 2
def interface():
    print('Delivery Summary')
    print('********************')
    total_miles = round(truck1.miles + truck2.miles + truck3.miles, 2)
    print(f"Route completed in: {total_miles} miles")
    print(f"Truck 1 miles: {truck1.miles}")
    print(f"Truck 2 miles: {truck2.miles}")
    print(f"Truck 3 miles: {truck3.miles}")
    print('********************')

    while True:
        print("\nEnter a command (1-3):")
        print("1. Display a specific package")
        print("2. Display the status of ALL packages")
        print("3. Exit")

        try:
            selected_num = int(input("> "))
        except ValueError:
            print("Invalid input. Please enter 1, 2, or 3.")
            continue

        if selected_num == 1:
            packageId = input('Enter a Package ID (1-40): ')
            timestamp = input('Enter a time in HH:MM format: ')
            h, m = map(int, timestamp.split(':'))
            user_time = datetime.timedelta(hours=h, minutes=m)

            #fetch package
            temp_storage = lookup(packageId)
            address = reverseAddressDict.get(temp_storage.address, "Unknown")
            if temp_storage.id == '9':
                address = "410 S State St" if user_time >= datetime.timedelta(hours=10, minutes=20) else "300 State St"

            truck_departure = {
                1: datetime.timedelta(hours=8),
                2: datetime.timedelta(hours=9, minutes=5),
                3: datetime.timedelta(hours=10, minutes=10)
            }.get(temp_storage.truckID, datetime.timedelta(0))

            #determine status
            if user_time <= truck_departure:
                status = "at hub"
                delivered_time = "--"
            elif not temp_storage.delivered or user_time < temp_storage.delivered:
                status = "en route"
                delivered_time = "--"
            else:
                status = "delivered"
                delivered_time = str(temp_storage.delivered)

            print("\nPackage Details:")
            print("-" * 70)
            print(f"{'Package ID:':20} {temp_storage.id}")
            print(f"{'Leaves Hub At:':20} {truck_departure}")
            print(f"{'Status:':20} {status}")
            print(f"{'Deadline:':20} {temp_storage.delivery_time}")
            print(f"{'Delivery Address:':20} {address}")
            print(f"{'Time Delivered:':20} {delivered_time}")
            print(f"{'Truck ID:':20} {temp_storage.truckID}")
            print("-" * 70)

        elif selected_num == 2:
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
                elif not Package.delivered or query_time < Package.delivered:
                    status = "en route"
                    delivered_time = "--"
                else:
                    status = "delivered"
                    delivered_time = str(Package.delivered)

                delivery_time = str(Package.delivery_time) if Package.delivery_time else "--"
                delivered_time_str = str(delivered_time) if delivered_time and delivered_time != "--" else "--"
                truck_id = str(Package.truckID) if Package.truckID is not None else "--"
                if not hasattr(Package, 'id') or Package.id == 'id':
                    continue
                print(f"{Package.id:<5} {address:<35} {str(truck_departure):<15} {status:<12} {delivery_time:<12} {delivered_time_str:<15} {truck_id:<6}")

            print("-" * 110)

        elif selected_num == 3:
            print("Exiting program...")
            break

        else:
            print("Invalid command, please try again.")

if "__main__":
    run()
    interface()
