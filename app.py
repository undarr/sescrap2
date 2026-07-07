import subprocess
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def get_driver():
    options = Options()
    
    # 1. NEW HEADLESS ENGINE (Required for Version 130+)
    options.add_argument("--headless=new")
    
    # 2. THE "VERSION 150" FIX
    # This flag is often required for the very latest Chromium builds in Docker
    options.add_argument("--remote-debugging-pipe")
    
    # 3. STANDARD CLOUD FLAGS
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    
    # 4. PATHS
    options.binary_location = "/usr/bin/chromium"
    service = Service("/usr/bin/chromedriver")

    chrome_version = subprocess.check_output(["chromium", "--version"]).decode("utf-8")
        
    # Check ChromeDriver Version
    driver_version = subprocess.check_output(["chromedriver", "--version"]).decode("utf-8")
        
    st.write(f"**Browser:** {chrome_version}")
    st.write(f"**Driver:** {driver_version}")
    
    return webdriver.Chrome(service=service, options=options)

try:
    st.info("Starting Chromium 150...")
    driver = get_driver()
    driver.get("https://www.google.com")
    st.success(f"Success! Page title: {driver.title}")
    driver.quit()
except Exception as e:
    st.error("Still crashing. Error details below:")
    st.code(str(e))
