import streamlit as st
from pymongo import MongoClient
import pandas as pd

st.set_page_config(page_title="AI Traffic Dashboard", layout="wide")
st.title("🚦 Smart Traffic & AI Analytics Dashboard")

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

st.divider()

st.subheader("Live Raw Data Feed (Latest 20 Records)")
st.dataframe(df.head(20), use_container_width=True)