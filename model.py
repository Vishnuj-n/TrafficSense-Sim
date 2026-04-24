from pymongo import MongoClient
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# WSL FIX: Using explicit 127.0.0.1
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["AITrafficDB"]
col = db["logs"]

print("Fetching data from MongoDB...")

# MEMORY FIX: Pull only the latest 10,000 records
data = list(col.find().sort("timestamp", -1).limit(10000))

# CRASH PREVENTION: Check if data actually exists
if len(data) == 0:
    print("Error: No data found! Please run generator.py first and wait a few seconds.")
    exit()

df = pd.DataFrame(data)

# Features and Target
X = df[["vehicle_count", "avg_speed"]]
y = df["congestion"]

# Train-Test Split
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Training Random Forest AI Model...")
model = RandomForestClassifier()
model.fit(x_train, y_train)

print(f"AI Accuracy Score: {model.score(x_test, y_test) * 100:.2f}%")