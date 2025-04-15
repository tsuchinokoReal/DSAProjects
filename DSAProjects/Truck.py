#Truck class object
class Truck:
    def __init__(self, packages, address, miles, time, truckID):
        self.packages = packages
        self.address = address
        self.miles = miles
        self.time = time
        self.truckID = truckID

    def __str__(self):
        return ("Truck ID: " + self.truckID +
                "Current Address: " + self.address +
                "Total Miles Driven: " + self.miles +
                "Total Time: " + self.time +
                f"Packages: {', '.join(str(package) for package in self.packages)}")











#from datetime import timedelta
# class Truck:
#     #constants
#     average_speed = 18
#     max_num_packages = 16
#
#     def __init__(self, truck_id, mph=average_speed, max_num_packages=max_num_packages):
#         self.id = truck_id
#         self.packages_id_list = []
#         self.mph = mph
#         self.max_num_packages = max_num_packages
#         self.total_distance_travelled = 0
#         self.mileage_timestamps = []
#         self.driver = None
#         self.time_obj = timedelta(hours=8, minutes=0, seconds=0)
#         self.hub_address = "placeholder"
#         self.at_hub = True
#
#     #adds package to list of packages to be delivered
#     def assign_package(self, package):
#         #check if truck is full
#         if len(self.packages_id_list) < self.max_num_packages:
#             self.packages_id_list.append(package.id_number)
#             package.assigned_truck_id = self.id
#         else:
#             return False
#
#     #space-time complexity: O(n)
#     #sets delivery status to "En route" for all packages loaded
#         def set_packages_en_route(self, ht):
#             for package_id in self.packages_id_list:
#                 package = ht.lookup(package_id)
#                 package.delivery_status = "En route"
#                 package.en_route_timestamp = self.time_obj
#
#     #delivers package and updates relevant fields
#         def deliver_package(self, ht, package_id, distance_traveled):
#             package = ht.lookup(package_id)
#             self.packages_id_list.remove(package_id)
#             self.at_hub = False
#             self.add_mileage(distance_traveled)
#             self.time_obj += timedelta(minutes=(distance_traveled / self.mph * 60))
#             self.mileage_timestamps.append([self.total_distance_traveled, self.time_obj])
#             package.delivery_status = "Delivered"
#             package.delivery_timestamp = self.time_obj
#
#     #adds mileage to TDT
#     def add_mileage(self, miles):
#         self.total_distance_travelled = self.total_distance_travelled + miles
#
#     #returns a list of packages on truck
#     def get_package_list(self, ht):
#         packages_list = [];
#
#         for package_id in self.packages_id_list:
#             packages_list.append(ht.lookup(package_id))
#
#         return packages_list
#
#     #returns true if num packages assigned = max capacity
#     def is_full(self):
#         if len(self.packages_id_list) == self.max_num_packages:
#             return True
#         return False