
import json
import csv

def export_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

def export_to_csv(data, filename, headers):
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
