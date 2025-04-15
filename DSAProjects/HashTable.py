#code for the HashTable obtained from: https://wgu.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=f08d7871-d57a-496e-a6a1-ac7601308c71
class HashTable:
    #init hash table and predefine capacity
    def __init__(self, initial_capacity=41):
        self.table = [[] for _ in range(initial_capacity)]
    #insertion method
    def insert(self, key, item):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        #update key if it is already in the bucket
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return
        bucket_list.append([key, item])

    #searches for a matching key extant in hashtable
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        return None
    #returns all values in hashtable
    def values(self):
        all_values = []
        for bucket in self.table:
            for key_value in bucket:
                all_values.append(key_value[1])
        return all_values























# import csv
# def csv_to_hash_table(csv_file):
#     hash_table = {}
#     with open(csv_file, mode = 'r', newline='') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             key = row['id']
#             hash_table[key] = row
#     return hash_table
#
# csv_file = 'package_file.csv'
# hash_table = csv_to_hash_table(csv_file)
#
# for key, value in hash_table.items():
#     print(f"Key: {key} => Value: {value}")