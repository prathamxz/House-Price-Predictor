import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_olx_data(city="pune", max_pages=5):
    base_url = f"https://www.olx.in/{city}/q-house-for-sale"
    all_properties = []
    
    headers = {"User-Agent": "Mozilla/5.0"}
    
    for page in range(1, max_pages + 1):
        url = f"{base_url}?page={page}"
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Failed to fetch page {page}: Status code {response.status_code}")
            continue
        
        soup = BeautifulSoup(response.text, "html.parser")
        listings = soup.find_all("li", class_="EIR5N")  # May need to inspect the live site for correct class
        
        for listing in listings:
            try:
                title = listing.find("span", class_="_2tW1I").get_text(strip=True)
                location = listing.find("span", class_="tjgMj").get_text(strip=True)
                price = listing.find("span", class_="_89yzn").get_text(strip=True)
                details = listing.find("span", class_="xg1aie").get_text(strip=True)
                
                bhk, sqft, bathrooms = "N/A", "N/A", "N/A"
                
                tokens = details.split()
                for i, token in enumerate(tokens):
                    if "BHK" in token:
                        bhk = token
                    elif "sqft" in token and i > 0:
                        sqft = tokens[i - 1]
                
                all_properties.append({
                    "Title": title,
                    "Location": location,
                    "Square Feet": sqft,
                    "BHK": bhk,
                    "Bathrooms": bathrooms,
                    "Price": price
                })
            except Exception as e:
                print(f"Skipping listing due to error: {e}")
                continue
    
    return all_properties

def save_to_csv(data, filename="pune_house_prices_olx.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    house_data = fetch_olx_data()
    if house_data:
        save_to_csv(house_data)
    else:
        print("No data found or scraping blocked!")