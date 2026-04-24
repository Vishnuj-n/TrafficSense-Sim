# 🚦 AI Traffic Analytics System

A real-time traffic monitoring and prediction system with MongoDB, Streamlit, and Machine Learning.

## Features

### 📊 Real-Time Dashboard
- **Live Data Visualization**: Auto-refreshing charts showing current traffic conditions
- **Interactive Time Series**: Real-time traffic flow monitoring with Plotly
- **Congestion Heatmap**: Hourly traffic patterns across different roads
- **Weather & Event Impact**: Analysis of external factors on traffic

### 🎲 Unpredictability Engine
- **Dynamic Weather System**: Clear, rainy, foggy, stormy conditions affecting traffic
- **Random Events**: Accidents, marathons, holidays, rush hours
- **Traffic Spikes**: Black swan events with sudden traffic surges
- **Road-Specific Weights**: Realistic variations between different road types

### 🤖 AI-Powered Features
- **Traffic Prediction**: Machine learning model for congestion forecasting
- **Anomaly Detection**: Real-time alerts for unusual traffic patterns
- **Smart Alert System**: Critical notifications for accidents and extreme conditions

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start MongoDB
Make sure MongoDB is running on `localhost:27017`

### 3. Generate Traffic Data
```bash
python generator.py
```
This starts the traffic generator with unpredictability features.

### 4. Launch Dashboard
```bash
streamlit run dashboard.py
```
Open your browser to `http://localhost:8501`

### 5. Train AI Model (Optional)
```bash
python predictor.py
```

### 6. Start Alert System (Optional)
```bash
python alert_system.py
```

## Project Structure

- `dashboard.py` - Real-time Streamlit dashboard with auto-refresh
- `generator.py` - Traffic data generator with weather/events/unpredictability
- `model.py` - Basic ML model for traffic classification
- `predictor.py` - Advanced AI prediction system
- `alert_system.py` - Real-time anomaly detection and alerts
- `requirements.txt` - Python dependencies

## Dashboard Features

- **Auto-Refresh**: Configurable refresh intervals (1-30 seconds)
- **Live Charts**: Real-time traffic flow visualization
- **Weather Impact**: Traffic analysis by weather conditions
- **Event Analysis**: Speed and congestion by events
- **Anomaly Alerts**: Automatic detection of unusual patterns
- **Heatmaps**: Congestion patterns by hour and road

## Data Schema

Each traffic record includes:
- `road_name`: MG Road, Ring Road, Airport Road, Brigade Road, ORR
- `vehicle_count`: Number of vehicles (10-500+ with spikes)
- `avg_speed`: Average speed (5-120 km/h)
- `congestion`: Level 0-3 (Low, Medium, High, Severe)
- `weather`: clear, rainy, foggy, stormy
- `event`: normal, accident, marathon, holiday, rush_hour
- `timestamp`: Real-time timestamp

## Advanced Features

### Unpredictability Factors
- Weather changes every 10-30 seconds
- Random traffic spikes (2% probability)
- Dynamic road weight multipliers
- Event-based traffic modifications
- Realistic speed and congestion calculations

### AI Predictions
- Feature engineering with time-based features
- Weather and event encoding
- Random Forest classification
- Real-time congestion prediction
- Confidence scoring

### Alert System
- High traffic detection (>400 vehicles)
- Low speed alerts (<15 km/h)
- Congestion spike detection
- Weather-related warnings
- Potential accident detection
- Sound alerts (optional)

## Technologies Used

- **MongoDB**: Real-time data storage
- **Streamlit**: Interactive dashboard
- **Plotly**: Advanced visualizations
- **scikit-learn**: Machine learning
- **pandas**: Data analysis

## Customization

You can easily modify:
- Road names and weights in `generator.py`
- Alert thresholds in `alert_system.py`
- Refresh intervals in dashboard
- Weather conditions and events
- ML model parameters

Enjoy monitoring your intelligent traffic system! 🚗💨
