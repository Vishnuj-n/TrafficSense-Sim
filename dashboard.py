import streamlit as st
from pymongo import MongoClient
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time

st.set_page_config(page_title="AI Traffic Dashboard", layout="wide")
st.title("🚦 Smart Traffic & AI Analytics Dashboard")

# Auto-refresh functionality
auto_refresh = st.sidebar.checkbox("🔄 Auto Refresh (10s)", value=True)
refresh_interval = st.sidebar.slider("Refresh Interval (seconds)", 5, 60, 10)

if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()

# WSL FIX: Using explicit 127.0.0.1
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client["AITrafficDB"]
col = db["logs"]

# Fetch latest 5000 records
data = list(col.find().sort("timestamp", -1).limit(5000))

if len(data) == 0:
    st.warning("Waiting for data... Please run generator.py in your terminal.")
    st.stop()

df = pd.DataFrame(data)

# STREAMLIT BUG FIX: Convert MongoDB ObjectId to string
if "_id" in df.columns:
    df["_id"] = df["_id"].astype(str)

# Layout: Split into columns for a better UI look
col1, col2 = st.columns(2)

with col1:
    st.subheader("Total Traffic by Road")
    chart = df.groupby("road_name")["vehicle_count"].sum()
    st.bar_chart(chart, color="#ff4b4b")

with col2:
    st.subheader("Average Speed per Road")
    speed = df.groupby("road_name")["avg_speed"].mean()
    st.bar_chart(speed, color="#0068c9")

# REAL-TIME LINE CHART
st.divider()
st.subheader("📈 Real-Time Traffic Flow (Last 50 Records)")

# Get last 50 records for time series
recent_data = list(col.find().sort("timestamp", -1).limit(50))
if recent_data:
    recent_df = pd.DataFrame(recent_data)
    recent_df['timestamp'] = pd.to_datetime(recent_df['timestamp'])
    recent_df = recent_df.sort_values('timestamp')
    
    # Create interactive time series chart
    fig = px.line(recent_df, x='timestamp', y='vehicle_count', 
                  color='road_name', title='Live Traffic Volume',
                  markers=True, line_shape='spline')
    fig.update_layout(height=400, xaxis_title="Time", yaxis_title="Vehicle Count")
    st.plotly_chart(fig, use_container_width=True)

# WEATHER & EVENT IMPACT ANALYSIS
st.divider()
col3, col4 = st.columns(2)

with col3:
    st.subheader("🌦️ Weather Impact")
    if 'weather' in df.columns:
        weather_impact = df.groupby('weather')['vehicle_count'].mean()
        st.bar_chart(weather_impact, color="#00b4d8")

with col4:
    st.subheader("🎭 Event Impact")
    if 'event' in df.columns:
        event_impact = df.groupby('event')['avg_speed'].mean()
        st.bar_chart(event_impact, color="#f72585")

# CONGESTION HEATMAP
st.subheader("🔥 Congestion Heatmap")
if len(data) > 0:
    # Create pivot table for heatmap
    pivot_data = df.pivot_table(values='congestion', index='road_name', 
                               columns=pd.to_datetime(df['timestamp']).dt.hour, 
                               aggfunc='mean', fill_value=0)
    
    fig_heatmap = px.imshow(pivot_data, title="Congestion Levels by Hour",
                           labels=dict(x="Hour of Day", y="Road", color="Congestion"))
    st.plotly_chart(fig_heatmap, use_container_width=True)

# PREDICTIONS & ALERTS
st.divider()
st.subheader("⚡ Live Predictions & Alerts")

# Simple anomaly detection
latest_data = df.head(100)
if len(latest_data) > 0:
    avg_traffic = latest_data['vehicle_count'].mean()
    current_traffic = latest_data.iloc[0]['vehicle_count']
    
    if current_traffic > avg_traffic * 2:
        st.error(f"🚨 HIGH TRAFFIC ALERT: Current traffic ({current_traffic}) is {current_traffic/avg_traffic:.1f}x above average!")
    elif current_traffic < avg_traffic * 0.3:
        st.warning(f"⚠️ UNUSUALLY LOW TRAFFIC: Current traffic ({current_traffic}) is significantly below average")
    else:
        st.success(f"✅ Normal traffic conditions: {current_traffic} vehicles")
    
    # Show current conditions
    if 'weather' in latest_data.columns and 'event' in latest_data.columns:
        current_weather = latest_data.iloc[0]['weather']
        current_event = latest_data.iloc[0]['event']
        st.info(f"🌤️ Current conditions: {current_weather} weather, {current_event} event")

st.divider()

st.subheader("Live Raw Data Feed (Latest 20 Records)")
st.dataframe(df.head(20), use_container_width=True)