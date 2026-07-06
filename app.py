import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os

def get_driver():
    options = Options()
    
    # 1. Use the new headless mode (required for Chrome 120+)
    options.add_argument("--headless=new")
    
    # 2. Critical Stability Flags
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=dbus") # Disable dbus to prevent hangs
    options.add_argument("--disable-dev-tools")
    
    # 3. Explicitly set the binary and driver locations
    # On Debian 13, these are the verified paths
    options.binary_location = "/usr/bin/chromium"
    service = Service("/usr/bin/chromedriver")
    
    return webdriver.Chrome(service=service, options=options)

try:
    st.info("Attempting to start Chromium 150...")
    driver = get_driver()
    driver.get("https://www.google.com")
    st.success(f"Connection Successful! Page: {driver.title}")
    driver.quit()
except Exception as e:
    st.error("Browser failed to start.")
    st.code(str(e))
