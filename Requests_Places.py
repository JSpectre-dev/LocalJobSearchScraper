from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

def scrape_google_maps():
  # Path to the ChromeDriver executable
    chrome_driver_path = "H:\\Documents\\College Education and Independent Study\\Jordan_Casper_Portfolio\\Drivers\\chromedriver-win64\\chromedriver.exe"  # Replace with the actual path to your ChromeDriver
    
    # Headers to mimic a browser (avoid getting blocked)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win6S4; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }
    
    # Service object
    service = Service(chrome_driver_path)
    
    # Pass the Service object to the WebDriver
    driver = webdriver.Chrome(service=service)
    
    # Navigate to Google Maps
    driver.get("https://www.google.com/maps")

    # Search for "Software Company"
    search_box = driver.find_element(By.ID, "searchboxinput")
    search_box.send_keys("Software Company")
    search_box.send_keys(Keys.RETURN)
    time.sleep(10)  # Wait for results to load
    
    
    #google_url = 
    
    # Fetch search results
    #response = requests.get(google_url, headers=headers)
    #soup = BeautifulSoup(response.text, "html.parser")


    # Extract data
    companies = []
    results = driver.find_elements(By.CLASS_NAME, "section-result")
    for result in results:
        try:
            name = result.find_element(By.CLASS_NAME, "section-result-title").text
            address = result.find_element(By.CLASS_NAME, "section-result-location").text
            companies.append({"Name": name, "Address": address})
        except Exception as e:
            print(f"Error extracting data: {e}")

    # Save to Excel
    if companies:
        df = pd.DataFrame(companies)
        df.to_excel("software_companies_maps.xlsx", index=False)
        print("Data saved to software_companies_maps.xlsx")
    else:
        print("No results found.")

    driver.quit()

# Run the function
scrape_google_maps()
