# SOC Dashboard

A **Streamlit-based Security Operations Center (SOC) Dashboard** that visualizes and monitors system logs, alerts, and security metrics in real time.  

---

## Features
- Log monitoring & visualization  
- Real-time system health graphs (CPU, Memory, Network)  
- Alerts for abnormal activities  
- User-friendly web interface with Streamlit  

---

## Tech Stack
- **Python**   
- **Streamlit** for the dashboard UI  
- **Matplotlib / Plotly** for graphs  
- **Pandas** for data handling  

---

## Installation

Clone the repository:

```bash
git clone https://github.com/noluzar/SOC-Dashboard.git
cd SOC-Dashboard

Create a virtual environment (recommended):
python -m venv venv
venv\Scripts\activate   # on Windows
source venv/bin/activate  # on macOS/Linux

Install dependencies:
pip install -r requirements.txt

Usage:
Run the Streamlit app:
streamlit run dashboard.py

License
This project is licensed under the MIT License.
