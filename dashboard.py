import streamlit as st
import psutil
import platform
import socket
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Auto refresh every 10 seconds
st_autorefresh(interval=10000, key="refresh")

# Dashboard Title
st.set_page_config(page_title="SOC Dashboard", layout="wide")
st.title("SOC Monitoring Dashboard")
st.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Health Check Function

def health_check():
    health = {}

    # CPU usage
    health["CPU Usage"] = f"{psutil.cpu_percent()}%"

    # Memory usage
    memory = psutil.virtual_memory()
    health["Memory Usage"] = f"{memory.percent}%"

    # Disk usage
    disk = psutil.disk_usage('/')
    health["Disk Usage"] = f"{disk.percent}%"

    # Network connectivity
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        health["Network"] = "Connected"
    except OSError:
        health["Network"] = "Disconnected"

    # System info
    health["OS"] = platform.system()
    health["Machine"] = platform.machine()

    return health

# Display Health Status

status = health_check()

col1, col2, col3 = st.columns(3)
col1.metric("CPU Usage", status["CPU Usage"])
col2.metric("Memory Usage", status["Memory Usage"])
col3.metric("Disk Usage", status["Disk Usage"])

st.subheader("Network Status")
st.info(status["Network"])

st.subheader("System Information")
st.json({
    "Operating System": status["OS"],
    "Machine": status["Machine"]
})
