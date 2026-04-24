from pymongo import MongoClient
from datetime import datetime
import random
import time
import numpy as np

# WSL FIX: Using explicit 127.0.0.1 instead of localhost
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["AITrafficDB"]
col = db["logs"]

roads = ["MG Road", "Ring Road", "Airport Road", "Brigade Road", "ORR"]

# UNPREDICTABILITY FACTORS
weather_conditions = ["clear", "rainy", "foggy", "stormy"]
events = ["normal", "accident", "marathon", "holiday", "rush_hour"]

# Dynamic road weights (simulating real-world variations)
road_weights = {
    "MG Road": 1.0,
    "Ring Road": 0.8,
    "Airport Road": 1.2,
    "Brigade Road": 0.9,
    "ORR": 1.1
}

col.create_index("timestamp")
col.create_index("road_name")

print("Starting live traffic generation with unpredictability... Press Ctrl+C to stop.")

# Global unpredictability state
current_weather = "clear"
current_event = "normal"
last_change = datetime.now()

while True:
    batch = []
    
    # RANDOMLY CHANGE CONDITIONS (every 10-30 seconds)
    if (datetime.now() - last_change).seconds > random.randint(10, 30):
        current_weather = random.choice(weather_conditions)
        current_event = random.choice(events)
        last_change = datetime.now()
        print(f" Conditions changed: {current_weather} weather, {current_event} event")
    
    for i in range(200):
        road = random.choice(roads)
        
        # BASE TRAFFIC WITH ROAD WEIGHTS
        base_vehicles = random.randint(20, 500) * road_weights[road]
        base_speed = random.randint(5, 90)
        
        # WEATHER IMPACTS
        weather_multiplier = 1.0
        speed_impact = 0
        if current_weather == "rainy":
            weather_multiplier = random.uniform(0.7, 0.9)
            speed_impact = random.randint(-10, -5)
        elif current_weather == "foggy":
            weather_multiplier = random.uniform(0.5, 0.8)
            speed_impact = random.randint(-20, -10)
        elif current_weather == "stormy":
            weather_multiplier = random.uniform(0.3, 0.6)
            speed_impact = random.randint(-30, -15)
        
        # EVENT IMPACTS
        event_multiplier = 1.0
        if current_event == "accident":
            event_multiplier = random.uniform(0.2, 0.5) if random.random() > 0.7 else 1.0
            speed_impact -= random.randint(15, 25)
        elif current_event == "marathon":
            event_multiplier = random.uniform(0.1, 0.3)
            speed_impact -= random.randint(20, 30)
        elif current_event == "holiday":
            event_multiplier = random.uniform(0.4, 0.7)
        elif current_event == "rush_hour":
            event_multiplier = random.uniform(1.5, 2.5)
            speed_impact -= random.randint(5, 15)
        
        # SUDDEN SPIKES (Black Swan Events)
        if random.random() < 0.02:  # 2% chance
            spike_multiplier = random.uniform(3, 8)
            print(f" TRAFFIC SPIKE on {road}!")
        else:
            spike_multiplier = 1.0
        
        # FINAL CALCULATIONS
        vehicles = int(base_vehicles * weather_multiplier * event_multiplier * spike_multiplier)
        speed = max(5, base_speed + speed_impact)  # Minimum speed of 5
        
        # Add some noise
        vehicles += random.randint(-10, 10)
        speed = max(5, speed + random.randint(-3, 3))
        
        # Dynamic congestion calculation
        if vehicles < 100:
            congestion = 0
        elif vehicles < 250:
            congestion = 1
        elif vehicles < 400:
            congestion = 2
        else:
            congestion = 3
        
        # Weather can increase congestion
        if current_weather in ["rainy", "foggy", "stormy"] and random.random() > 0.6:
            congestion = min(3, congestion + 1)

        batch.append({
            "road_name": road,
            "vehicle_count": max(10, vehicles),  # Minimum 10 vehicles
            "avg_speed": min(120, speed),  # Maximum speed 120
            "congestion": congestion,
            "weather": current_weather,
            "event": current_event,
            "timestamp": datetime.now()
        })

    col.insert_many(batch)
    print(f"Inserted 200 records | Weather: {current_weather} | Event: {current_event}")
    time.sleep(1)