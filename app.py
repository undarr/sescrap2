import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import subprocess

st.title("Deep Debugger")

def get_driver_debug():
    log_path = "/tmp/chromedriver.log" # Use /tmp/ as it is always writable
    
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.binary_location = "/usr/bin/chromium"

    service = Service(
        executable_path="/usr/bin/chromedriver",
        log_path=log_path
    )
    # This environment variable forces more detail from the driver
    os.environ["WDM_LOG_LEVEL"] = "0" 

    return webdriver.Chrome(service=service, options=options), log_path

if st.button("Run Deep Debug"):
    try:
        driver, log_file = get_driver_debug()
        st.success("Started!")
        driver.quit()
    except Exception as e:
        st.error("Crash detected.")
        
        # 1. Show the Python Error
        st.subheader("Python Error Message")
        st.code(str(e))
        
        # 2. Try to read the log file from /tmp/
        st.subheader("Driver Log (/tmp/chromedriver.log)")
        if os.path.exists("/tmp/chromedriver.log"):
            with open("/tmp/chromedriver.log", "r") as f:
                st.code(f.read())
        else:
            st.warning("Log file was not created in /tmp/. This means the binary failed to start entirely.")

        # 3. THE SMOKING GUN: Manual Startup Test
        st.subheader("System Error (Manual Probe)")
        try:
            # Try to run the driver manually and capture its 'scream'
            cmd = ["/usr/bin/chromedriver", "--version"]
            out = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode()
            st.write("Manual probe output:", out)
        except subprocess.CalledProcessError as err:
            st.error("The binary itself is broken:")
            st.code(err.output.decode())
