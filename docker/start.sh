#!/bin/bash

# Start Selenium server in background
/opt/bin/entry_point.sh &

# Wait for Selenium to fully initialize
sleep 5

# Start your Streamlit app
streamlit run home_page.py --server.headless=true --server.port=8501 --server.address=0.0.0.0