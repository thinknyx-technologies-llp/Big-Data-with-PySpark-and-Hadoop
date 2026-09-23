import csv
import random
from datetime import datetime, timedelta

# Scale up to 3,000,000 rows (~165MB - 180MB CSV file)
num_rows = 3000000
categories = ["Electronics", "Apparel", "Home & Kitchen", "Toys", "Books", "Sports", "Beauty"]
start_time = datetime(2026, 11, 27, 0, 0, 0)

print(f"Generating {num_rows:,} rows of Black Friday data. Please wait...")

with open("shopsphere_black_friday.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["transaction_id", "customer_id", "product_category", "purchase_amount", "timestamp"])
    
    for i in range(1, num_rows + 1):
        txn_id = f"TXN-{10000000 + i}"
        cust_id = f"CUST-{random.randint(10000, 99999)}"
        category = random.choice(categories)
        
        if category == "Electronics":
            amount = round(random.uniform(50.0, 2500.0), 2)
        elif category in ["Books", "Beauty"]:
            amount = round(random.uniform(5.0, 50.0), 2)
        else:
            amount = round(random.uniform(10.0, 300.0), 2)
            
        timestamp = (start_time + timedelta(seconds=int(i * 0.05))).strftime("%Y-%m-%dT%H:%M:%SZ")
        writer.writerow([txn_id, cust_id, category, amount, timestamp])

print("Success: shopsphere_black_friday.csv created on local server!")
