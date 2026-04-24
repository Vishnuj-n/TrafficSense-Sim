from pymongo import MongoClient
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np
from datetime import datetime

# WSL FIX: Using explicit 127.0.0.1
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["AITrafficDB"]
col = db["logs"]

print("🤖 Advanced AI Traffic Prediction System")
print("=" * 50)

# Fetch latest data
data = list(col.find().sort("timestamp", -1).limit(15000))

if len(data) == 0:
    print("❌ No data found! Please run generator.py first.")
    exit()

df = pd.DataFrame(data)

# Enhanced feature engineering
df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.dayofweek
df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)

# Weather and event encoding
if 'weather' in df.columns:
    df = pd.get_dummies(df, columns=['weather'], prefix='weather')
if 'event' in df.columns:
    df = pd.get_dummies(df, columns=['event'], prefix='event')

# Feature selection
feature_cols = ['vehicle_count', 'avg_speed', 'hour', 'day_of_week', 'is_weekend']
if 'weather_rainy' in df.columns:
    feature_cols.extend(['weather_clear', 'weather_rainy', 'weather_foggy', 'weather_stormy'])
if 'event_normal' in df.columns:
    feature_cols.extend(['event_normal', 'event_accident', 'event_marathon', 'event_holiday', 'event_rush_hour'])

X = df[feature_cols]
y = df['congestion']

# Train-test split
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"📊 Training on {len(x_train)} samples, testing on {len(x_test)} samples")

# Advanced model
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=10,
    random_state=42,
    class_weight='balanced'
)

model.fit(x_train, y_train)

# Evaluation
y_pred = model.predict(x_test)
accuracy = model.score(x_test, y_test)

print(f"\n🎯 Model Accuracy: {accuracy * 100:.2f}%")
print("\n📋 Classification Report:")
print(classification_report(y_test, y_pred))

# Feature importance
feature_importance = pd.DataFrame({
    'feature': feature_cols,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

print("\n🔍 Top 5 Most Important Features:")
for _, row in feature_importance.head(5).iterrows():
    print(f"  • {row['feature']}: {row['importance']:.3f}")

# Real-time prediction function
def predict_traffic(vehicle_count, avg_speed, hour, day_of_week, weather='clear', event='normal'):
    """Predict congestion for given traffic conditions"""
    
    # Prepare input
    input_data = {
        'vehicle_count': vehicle_count,
        'avg_speed': avg_speed,
        'hour': hour,
        'day_of_week': day_of_week,
        'is_weekend': 1 if day_of_week >= 5 else 0
    }
    
    # Add weather features
    for w in ['clear', 'rainy', 'foggy', 'stormy']:
        input_data[f'weather_{w}'] = 1 if w == weather else 0
    
    # Add event features
    for e in ['normal', 'accident', 'marathon', 'holiday', 'rush_hour']:
        input_data[f'event_{e}'] = 1 if e == event else 0
    
    # Create DataFrame in correct order
    input_df = pd.DataFrame([input_data])[feature_cols]
    
    # Predict
    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]
    
    congestion_labels = ['Low', 'Medium', 'High', 'Severe']
    
    return {
        'predicted_congestion': congestion_labels[prediction],
        'confidence': max(probabilities) * 100,
        'all_probabilities': dict(zip(congestion_labels, probabilities * 100))
    }

# Example predictions
print("\n🔮 Sample Predictions:")
print("-" * 30)

current_hour = datetime.now().hour
current_day = datetime.now().weekday()

scenarios = [
    (150, 45, current_hour, current_day, 'clear', 'normal'),
    (350, 20, current_hour, current_day, 'rainy', 'accident'),
    (50, 80, current_hour, current_day, 'clear', 'holiday'),
    (500, 10, 18, 0, 'stormy', 'rush_hour')  # Monday evening storm
]

for i, (vehicles, speed, hour, day, weather, event) in enumerate(scenarios, 1):
    result = predict_traffic(vehicles, speed, hour, day, weather, event)
    print(f"Scenario {i}: {vehicles} vehicles, {speed}km/h, {weather} weather, {event} event")
    print(f"  → Predicted: {result['predicted_congestion']} (Confidence: {result['confidence']:.1f}%)")

print(f"\n✅ Prediction model ready! Use predict_traffic() function for real-time predictions.")
