import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import tempfile

def get_driver():
    options = Options()
    
    # 1. THE "ULTIMATE" HEADLESS FLAGS
    # Using --headless=old is often more stable in container environments than =new
    options.add_argument("--headless") 
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    
    # 2. FIX FOR CHROMIUM 140+ CRASHES
    # These flags disable features that often fail in Linux containers
    options.add_argument("--disable-software-rasterizer")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument("--single-process") # This is a heavy-duty fix for 'Exited' errors
    options.add_argument("--remote-debugging-pipe")

    # 3. SET WRITABLE USER DATA DIRECTORY
    # Chromium 150 often crashes if it can't write to the home directory
    user_data_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={user_data_dir}")

    # 4. PATHS (Confirmed from your previous check)
    options.binary_location = "/usr/bin/chromium"
    service = Service("/usr/bin/chromedriver")
    
    return webdriver.Chrome(service=service, options=options)

try:
    with st.spinner("Initializing Chrome (this may take a moment)..."):
        driver = get_driver()
        driver.get("https://www.google.com")
        st.success(f"Successfully connected! Title: {driver.title}")
        driver.quit()
except Exception as e:
    st.error(f"Chrome is still crashing.")
    st.info("Technical Error Details:")
    st.code(str(e))
