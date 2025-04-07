import csv
def csv_to_hash_table(csv_file):
    hash_table = {}
    with open(csv_file, mode = 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            key = row['id']
            hash_table[key] = row
    return hash_table

csv_file = 'package_file.csv'
hash_table = csv_to_hash_table(csv_file)

for key, value in hash_table.items():
    print(f"Key: {key} => Value: {value}")