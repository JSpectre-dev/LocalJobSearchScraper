import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define search query
search_query = "Boise Idaho Software Companies"

# Base URL for Google Search (use with caution due to scraping limitations)
google_url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"



# Headers to mimic a browser (avoid getting blocked)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win6S4; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
}

# Fetch search results
response = requests.get(google_url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Extract company names and links from search results
companies = []
for result in soup.find_all("div", class_="tF2Cxc"):
    name = result.find("h3").text
    link = result.find("a")["href"]
    companies.append({"Company Name": name, "Website": link})

# Convert to DataFrame and save to Excel
df = pd.DataFrame(companies)
df.to_excel("companies.xlsx", index=False)
print("Scraping complete. Data saved to companies.xlsx")
