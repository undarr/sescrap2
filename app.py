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

from selenium.webdriver.chrome.service import Service

def get_driver_with_logs():
    options = Options()
    # 1. THE ESSENTIAL TRINITY FOR VERSION 150
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-setuid-sandbox") # NEW: Extra sandbox bypass
    
    # 2. THE "NO-ZYGOTE" FIX (Critical for Debian 13)
    # This prevents Chrome from trying to fork processes it isn't allowed to
    options.add_argument("--no-zygote")
    options.add_argument("--disable-dev-shm-usage")
    
    # 3. COMMUNICATION FIX
    options.add_argument("--remote-debugging-pipe")
    
    # 4. DISABLING EXTRAS TO SAVE MEMORY
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-dev-tools")

    # Create a log file path
    log_path = "chromedriver.log"
    
    # Start service with verbose logging
    service = Service(
        executable_path="/usr/bin/chromedriver", 
        log_path=log_path,
        service_args=["--verbose"]
    )
    
    return webdriver.Chrome(service=service, options=options), log_path

# In your Streamlit app:
if st.button("Debug Flags"):
    try:
        driver, log_file = get_driver_with_logs()
        st.success("Started successfully!")
        driver.quit()
    except Exception as e:
        st.error("Crash detected. Reading logs...")
        if os.path.exists("chromedriver.log"):
            with open("chromedriver.log", "r") as f:
                st.code(f.read()) # This will show exactly why Chrome said 'No'

try:
    st.info("Starting Chromium 150...")
    driver = get_driver()
    driver.get("https://www.google.com")
    st.success(f"Success! Page title: {driver.title}")
    driver.quit()
except Exception as e:
    st.error("Still crashing. Error details below:")
    st.code(str(e))
