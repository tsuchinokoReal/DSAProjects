#object for packages
class Package:
    def __init__(self, id, address, city, state, zip, delivery_time, weight, notes, status):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.delivery_time = delivery_time
        self.weight = weight
        self.notes = notes
        self.status = status
        self.delivered = None
        self.truckID = None

    def __str__(self):
        return ("ID: " + self.id +
                " Address: " + self.address +
                " City: " + self.city +
                " State: " + self.state +
                " Zip: " + self.zip +
                " Delivery Time: " + self.delivery_time +
                " Weight: " + self.weight +
                " Notes: " + self.notes +
                " Time Delivered: " + self.delivered +
                " Truck ID: " + self.truckID)