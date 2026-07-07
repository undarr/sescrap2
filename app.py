import subprocess
import streamlit as st

st.subheader("New Silent Browser Test")

# This command attempts to render the page while silencing the errors you saw
cmd2 = [
    "/usr/bin/chromium",
    "--headless",              # Use headless mode
    "--no-sandbox",           # Required for Linux containers
    "--no-zygote",            # Fixes the 'Permission Denied' crash
    "--disable-gpu",          # Fixes graphics errors
    "--disable-software-rasterizer", # Fixes the CPU frequency errors
    "--disable-features=dbus", # Muzzles the D-Bus socket errors
    "--disable-dev-shm-usage", # Prevents memory crashes
    "--log-level=3",          # Tells Chromium: "Only show Fatal errors, hide warnings"
    "--silent",               # Even more noise reduction
    "--dump-dom",             # The goal: Print the HTML to our screen
    "https://www.example.com" # The target
]

try:
    with st.spinner("Executing Silent Launch..."):
        # We capture both output (HTML) and errors
        process = subprocess.run(cmd2, capture_output=True, text=True, timeout=15)
        
        # 1. Show the "Scream" (Even log-level 3 might show something)
        if process.stderr:
            st.warning("System Warnings (Can usually be ignored):")
            st.code(process.stderr)
            
        # 2. Show the "Success" (The HTML)
        if "Example Domain" in process.stdout:
            st.success("✅ SUCCESS! Chromium successfully reached the site and extracted HTML.")
            st.expander("View Extracted HTML").code(process.stdout[:1000] + "...")
        else:
            st.error("The command ran, but we didn't get the expected HTML.")
            st.write("Full Output:", process.stdout)

except subprocess.TimeoutExpired:
    st.error("⏰ Timeout: The browser hung for more than 15 seconds.")
except Exception as e:
    st.error(f"Unexpected Error: {e}")
