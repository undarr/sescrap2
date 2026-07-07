import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os

def get_driver():
    options = Options()
    
    # 1. SET THE BINARY PATH TO GOOGLE CHROME (NOT CHROMIUM)
    # When you install google-chrome-stable, it goes here:
    options.binary_location = "/usr/bin/google-chrome"
    
    # 2. STABLE FLAGS
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-zygote")
    options.add_argument("--remote-debugging-pipe")
    
    # 3. USE WEBDRIVER-MANAGER TO GET THE MATCHING STABLE DRIVER
    # This will automatically find version 131 (or current stable)
    try:
        driver_path = ChromeDriverManager().install()
        service = Service(driver_path)
        return webdriver.Chrome(service=service, options=options)
    except Exception as e:
        # Fallback to system driver if manager fails
        st.warning("Webdriver Manager failed, trying system path...")
        return webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=options)

st.title("Stable Chrome Scraper")

if st.button("Run Scraper (Version 131 Stable)"):
    try:
        with st.spinner("Launching Google Chrome Stable..."):
            driver = get_driver()
            driver.get("https://www.example.com")
            st.success(f"Success! Page title: {driver.title}")
            driver.quit()
    except Exception as e:
        st.error("Still crashing. This suggests the Debian 13 environment is blocking all browser binaries.")
        st.code(str(e))
