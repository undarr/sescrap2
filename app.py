import os
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

st.title("🔍 Path & Binary Checker")

# The paths we are testing
chrome_path = "/usr/bin/chromium"
driver_path = "/usr/bin/chromedriver"

def check_file(path, name):
    st.subheader(f"Checking {name}")
    if os.path.exists(path):
        st.success(f"✅ Found: `{path}`")
        
        # Check if it's executable
        if os.access(path, os.X_OK):
            st.info(f"👍 `{name}` has permission to run.")
        else:
            st.error(f"⚠️ `{name}` is found, but cannot be executed (Permission Denied).")
            
        # Try to get the version by running it
        try:
            version = subprocess.check_output([path, "--version"]).decode()
            st.write(f"**Version Info:** {version}")
        except Exception as e:
            st.warning(f"Could not get version: {e}")
    else:
        st.error(f"❌ NOT FOUND: `{path}`")
        st.info(f"Try searching the system for `{name}`...")
        # This searches the system to see where the OS put it
        search = subprocess.check_output(["which", name.lower().replace(" ", "")]).decode()
        st.write(f"System says `{name}` is actually at: `{search}`")

check_file(chrome_path, "Chromium Browser")
check_file(driver_path, "ChromeDriver")

try:
    st.info("Starting Chromium 150...")
    driver = get_driver()
    driver.get("https://www.google.com")
    st.success(f"Success! Page title: {driver.title}")
    driver.quit()
except Exception as e:
    st.error("Still crashing. Error details below:")
    st.code(str(e))
