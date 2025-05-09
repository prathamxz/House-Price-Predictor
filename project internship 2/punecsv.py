import requests
from bs4 import BeautifulSoup 
import pandas as pd

def fetch_magicbricks_data(city="pune", max_pages=5):
    base_url = "https://www.magicbricks.com/property-for-sale-rent-in-{}".format(city)
    all_properties = []
    
    for page in range(1, max_pages + 1):
        url = f"{base_url}/page-{page}"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        
        if response.status_code != 200:
            print(f"Failed to fetch data from MagicBricks on page {page}")
            continue
        
        soup = BeautifulSoup(response.text, "html.parser")
        listings = soup.find_all("div", class_="mb-srp__list")
        
        for listing in listings:
            try:
                location = listing.find("span", class_="mb-srp__card--locality").text.strip()
                sqft = listing.find("div", class_="mb-srp__card--size").text.strip()
                bhk = listing.find("span", class_="mb-srp__card--title").text.strip()
                bathrooms = listing.find("span", class_="mb-srp__card--bath").text.strip()
                price = listing.find("div", class_="mb-srp__card--price").text.strip()
                
                all_properties.append({
                    "Location": location,
                    "Square Feet": sqft,
                    "BHK": bhk,
                    "Bathrooms": bathrooms,
                    "Price": price
                })
            except AttributeError:
                continue
    
    return all_properties

def save_to_csv(data, filename="pune_house_prices.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

if __name__ == "__main__":
    house_data = fetch_magicbricks_data()
    if house_data:
        save_to_csv(house_data)
    else:
        print("No data found!")
