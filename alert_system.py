from pymongo import MongoClient
import pandas as pd
import time
import random
from datetime import datetime, timedelta
# Sound alerts disabled - pygame removed

# WSL FIX: Using explicit 127.0.0.1
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["AITrafficDB"]
col = db["logs"]

class TrafficAlertSystem:
    def __init__(self):
        self.alert_thresholds = {
            'high_traffic': 400,
            'low_speed': 15,
            'congestion_spike': 3,
            'accident_probability': 0.7
        }
        self.alert_history = []
        self.cooldown_period = 60  # seconds
        
    def check_anomalies(self):
        """Check for traffic anomalies and generate alerts"""
        
        # Get recent data
        recent_data = list(col.find().sort("timestamp", -1).limit(100))
        
        if len(recent_data) < 10:
            return []
        
        df = pd.DataFrame(recent_data)
        
        alerts = []
        current_time = datetime.now()
        
        # 1. High Traffic Alert
        current_traffic = df.iloc[0]['vehicle_count']
        if current_traffic > self.alert_thresholds['high_traffic']:
            alerts.append({
                'type': 'HIGH_TRAFFIC',
                'message': f"🚨 Extreme traffic: {current_traffic} vehicles detected!",
                'severity': 'HIGH',
                'timestamp': current_time,
                'road': df.iloc[0]['road_name']
            })
        
        # 2. Low Speed Alert
        current_speed = df.iloc[0]['avg_speed']
        if current_speed < self.alert_thresholds['low_speed']:
            alerts.append({
                'type': 'LOW_SPEED',
                'message': f"🐌 Traffic crawl: Speed dropped to {current_speed} km/h",
                'severity': 'MEDIUM',
                'timestamp': current_time,
                'road': df.iloc[0]['road_name']
            })
        
        # 3. Congestion Spike Detection
        recent_congestion = df.head(5)['congestion'].mean()
        historical_congestion = df['congestion'].mean()
        
        if recent_congestion > historical_congestion * 1.5:
            alerts.append({
                'type': 'CONGESTION_SPIKE',
                'message': f"📈 Congestion spike: Current level {recent_congestion:.1f} vs historical {historical_congestion:.1f}",
                'severity': 'HIGH',
                'timestamp': current_time,
                'road': df.iloc[0]['road_name']
            })
        
        # 4. Weather-Related Alerts
        if 'weather' in df.columns:
            current_weather = df.iloc[0]['weather']
            if current_weather in ['stormy', 'foggy']:
                alerts.append({
                    'type': 'WEATHER_ALERT',
                    'message': f"🌦️ Hazardous weather: {current_weather} conditions affecting traffic",
                    'severity': 'MEDIUM',
                    'timestamp': current_time,
                    'road': 'All roads'
                })
        
        # 5. Accident Detection (based on sudden speed drop + high traffic)
        if current_traffic > 300 and current_speed < 10:
            alerts.append({
                'type': 'POTENTIAL_ACCIDENT',
                'message': f"💥 Possible accident: High traffic ({current_traffic}) with very low speed ({current_speed} km/h)",
                'severity': 'CRITICAL',
                'timestamp': current_time,
                'road': df.iloc[0]['road_name']
            })
        
        # Filter alerts based on cooldown
        filtered_alerts = []
        for alert in alerts:
            if not self.is_duplicate_alert(alert):
                filtered_alerts.append(alert)
                self.alert_history.append(alert)
        
        return filtered_alerts
    
    def is_duplicate_alert(self, new_alert):
        """Check if alert is duplicate within cooldown period"""
        current_time = datetime.now()
        
        for old_alert in self.alert_history:
            time_diff = (current_time - old_alert['timestamp']).seconds
            
            if (time_diff < self.cooldown_period and 
                old_alert['type'] == new_alert['type'] and 
                old_alert['road'] == new_alert['road']):
                return True
        
        return False
    
    def play_alert_sound(self, severity):
        """Sound alerts disabled - pygame removed"""
        print(f"🔊 ALERT: {severity} severity alert (sound disabled)")

def main():
    print("🚨 Traffic Alert System Started")
    print("Monitoring for real-time traffic anomalies...")
    print("Press Ctrl+C to stop")
    print("-" * 50)
    
    alert_system = TrafficAlertSystem()
    
    try:
        while True:
            alerts = alert_system.check_anomalies()
            
            for alert in alerts:
                print(f"\n⚠️  [{alert['severity']}] {alert['message']}")
                print(f"   📍 Location: {alert['road']}")
                print(f"   🕐 Time: {alert['timestamp'].strftime('%H:%M:%S')}")
                
                # Play sound alert
                alert_system.play_alert_sound(alert['severity'])
                
                # Log to database (optional)
                col.insert_one({
                    'alert_type': alert['type'],
                    'message': alert['message'],
                    'severity': alert['severity'],
                    'road': alert['road'],
                    'timestamp': alert['timestamp'],
                    'is_alert': True
                })
            
            time.sleep(5)  # Check every 5 seconds
            
    except KeyboardInterrupt:
        print("\n🛑 Alert system stopped by user")
    except Exception as e:
        print(f"\n❌ Error in alert system: {e}")

if __name__ == "__main__":
    main()
