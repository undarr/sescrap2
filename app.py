import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import subprocess

st.title("Selenium Debugger")

# --- DEBUGGING: Check if binaries exist ---
st.subheader("System Check")
paths = ["/usr/bin/chromium", "/usr/bin/chromium-browser", "/usr/bin/chromedriver"]
for p in paths:
    exists = os.path.exists(p)
    st.write(f"Path `{p}` exists: {'✅' if exists else '❌'}")

# --- THE ACTUAL FIX ---
def get_driver():
    options = Options()
    
    # 1. Essential Headless Flags
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    
    # 2. Tell Selenium where the Chromium browser is
    options.binary_location = "/usr/bin/chromium"
    
    # 3. Tell Selenium where the MATCHING driver is
    # (Installed via packages.txt to /usr/bin/chromedriver)
    service = Service("/usr/bin/chromedriver")
    
    return webdriver.Chrome(service=service, options=options)

if st.button("Attempt Connection"):
    try:
        with st.spinner("Starting Chrome..."):
            driver = get_driver()
            driver.get("https://www.google.com")
            st.success(f"Success! Page title: {driver.title}")
            driver.quit()
    except Exception as e:
        st.error("FAILED TO START CHROME")
        st.code(str(e))
        
        # Try to get version info to see what's installed
        try:
            v = subprocess.check_output(["chromium", "--version"]).decode()
            st.info(f"System Chromium Version: {v}")
        except:
            st.warning("Could not retrieve Chromium version.")
