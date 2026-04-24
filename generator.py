from pymongo import MongoClient
from datetime import datetime
import random
import time

# WSL FIX: Using explicit 127.0.0.1 instead of localhost
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["AITrafficDB"]
col = db["logs"]

roads = ["MG Road", "Ring Road", "Airport Road", "Brigade Road", "ORR"]

col.create_index("timestamp")
col.create_index("road_name")

print("Starting live traffic generation... Press Ctrl+C to stop.")

while True:
    batch = []
    for i in range(200):
        vehicles = random.randint(20, 500)
        speed = random.randint(5, 90)

        # Simple logic to determine congestion level
        if vehicles < 100:
            congestion = 0
        elif vehicles < 250:
            congestion = 1
        elif vehicles < 400:
            congestion = 2
        else:
            congestion = 3

        batch.append({
            "road_name": random.choice(roads),
            "vehicle_count": vehicles,
            "avg_speed": speed,
            "congestion": congestion,
            "timestamp": datetime.now()
        })

    col.insert_many(batch)
    print("Inserted 200 records")
    time.sleep(1)