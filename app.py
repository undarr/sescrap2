import streamlit as st
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager

def get_driver():
    options = Options()
    options.add_argument("--headless")  # Standard headless mode
    
    # Firefox is much more stable in containers and 
    # usually doesn't need the 'no-sandbox' or 'no-zygote' hacks.
    
    service = Service(GeckoDriverManager().install())
    return webdriver.Firefox(service=service, options=options)

st.title("Stable Firefox Scraper")

if st.button("Run Scraper (Firefox ESR)"):
    try:
        with st.spinner("Launching Firefox ESR (Stable)..."):
            driver = get_driver()
            driver.get("https://www.example.com")
            st.success(f"Success! Page title: {driver.title}")
            
            # Show a snippet of the page to prove it works
            st.write("First 100 characters of page:")
            st.code(driver.page_source[:100])
            
            driver.quit()
    except Exception as e:
        st.error(f"Scraper Error: {e}")
