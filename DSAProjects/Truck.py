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