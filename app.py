import subprocess
import streamlit as st
import tempfile
import os

st.subheader("Brute Force Browser Test")

# Create a unique temp directory for this specific run
# This fixes the 'Silent Exit' if Chromium can't write to the default profile
temp_dir = tempfile.mkdtemp()

cmd3 = [
    "/usr/bin/chromium",
    "--headless=old",           # <--- CHANGE: Use the legacy engine
    "--no-sandbox",
    "--no-zygote",
    "--disable-gpu",
    "--disable-dev-shm-usage",
    "--disable-setuid-sandbox", # <--- ADDED: Extra sandbox bypass
    f"--user-data-dir={temp_dir}", # <--- ADDED: Writable profile path
    "--remote-debugging-pipe",
    "--dump-dom",
    "https://www.example.com"
]

try:
    with st.spinner("Brute forcing launch..."):
        # We capture stdout and stderr separately
        result = subprocess.run(cmd3, capture_output=True, text=True, timeout=20)
        
        if result.stderr:
            st.warning("System Warnings:")
            st.code(result.stderr)
            
        if result.stdout:
            st.success("✅ SUCCESS! The Brute Force method worked.")
            st.code(result.stdout[:500])
        else:
            st.error("STILL EMPTY. Chromium is being killed by the Kernel.")
            
except Exception as e:
    st.error(f"Error: {e}")
