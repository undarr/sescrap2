import subprocess
import streamlit as st

st.subheader("Manual Browser Probe")

cmd = ["/usr/bin/chromium", "--version"]
out = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode()
st.success(f"Browser version check: {out}")
    
st.info("Attempting mini-launch...")
cmd2 = ["/usr/bin/chromium", "--headless", "--no-sandbox", "--disable-gpu", "--no-zygote", "--disable-features=dbus", "--dump-dom", "https://www.google.com"]
out2 = subprocess.check_output(cmd2, stderr=subprocess.STDOUT, timeout=10).decode()
st.write("Browser successfully rendered Google HTML!")
    
