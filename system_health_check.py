# system_health_check.py
import psutil
import socket
import platform
import time
import json
import uuid
from datetime import datetime

INCIDENT_FILE = "incidents.json"
CPU_THRESHOLD = 80
MEMORY_THRESHOLD = 80
DISK_THRESHOLD = 90

# Incident management functions
def load_incidents():
    try:
        with open(INCIDENT_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_incidents(incidents):
    with open(INCIDENT_FILE, "w") as file:
        json.dump(incidents, file, indent=4)

def create_incident(incident_type, severity, description):
    incidents = load_incidents()
    incident = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": incident_type,
        "severity": severity,
        "status": "Open",
        "description": description
    }
    incidents.append(incident)
    save_incidents(incidents)
    return incident  # return incident for dashboard use

# System health check functions
def check_cpu():
    usage = psutil.cpu_percent(interval=1)
    if usage > CPU_THRESHOLD:
        create_incident("CPU Alert", "High", f"CPU usage is {usage}%")
    return usage

def check_memory():
    memory = psutil.virtual_memory()
    if memory.percent > MEMORY_THRESHOLD:
        create_incident("Memory Alert", "High", f"Memory usage is {memory.percent}%")
    return memory.percent, round(memory.available/1024**3, 2)

def check_disk():
    disk = psutil.disk_usage('/')
    if disk.percent > DISK_THRESHOLD:
        create_incident("Disk Alert", "High", f"Disk usage is {disk.percent}%")
    return disk.percent, round(disk.free/1024**3, 2)

def check_network():
    try:
        socket.setdefaulttimeout(3)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(("8.8.8.8", 53))
        return "Connected"
    except socket.error:
        create_incident("Network Alert", "High", "Network disconnected!")
        return "Disconnected"

def get_uptime_hours():
    uptime_seconds = time.time() - psutil.boot_time()
    return round(uptime_seconds / 3600, 2)

# Combined function for dashboard
def get_system_metrics():
    cpu = check_cpu()
    memory_percent, memory_available = check_memory()
    disk_percent, disk_free = check_disk()
    network_status = check_network()
    uptime = get_uptime_hours()
    metrics = {
        "CPU Usage (%)": cpu,
        "Memory Usage (%)": memory_percent,
        "Memory Available (GB)": memory_available,
        "Disk Usage (%)": disk_percent,
        "Disk Free (GB)": disk_free,
        "Network": network_status,
        "Uptime (hours)": uptime,
        "System": f"{platform.system()} {platform.release()}",
        "Processor": platform.processor()
    }
    return metrics
