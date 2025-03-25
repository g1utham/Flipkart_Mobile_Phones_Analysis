import pandas as pd
import requests
from bs4 import BeautifulSoup

product_name = []
product_prices = []
description = []
reviews = []

for i in range(1,30):
    url = f"https://www.flipkart.com/search?q=Mobiles+under+50000&page={i}"
    print(url)

    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        soup = BeautifulSoup(r.text, "lxml")

        try:
            box = soup.find("div", class_="DOjaWF gdgoEp")
            if box is not None:
                # Product Name
                names = box.find_all("div", class_="KzDlHZ")
                for i in names:
                    product_name.append(i.text if i.text else None)

                # Product Price
                prices = box.find_all("div", class_="Nx9bqj _4b5DiR")
                for i in prices:
                    product_prices.append(i.text if i.text else None)

                # Description
                desc = box.find_all("ul", class_="G4BRas")
                for i in desc:
                    description.append(i.text if i.text else None)

                # Ratings
                review = box.find_all("div", class_="XQDdHH")
                for i in review:
                    reviews.append(i.text if i.text else None)

        except AttributeError as e:
            print(f"Error while parsing HTML: {e}")

    except requests.exceptions.RequestException as e:
        print(f"Error while fetching data: {e}")

# Create DataFrame
try:
    df = pd.DataFrame({
        "Product Name": product_name,
        "Product Price": product_prices,
        "Description": description,
        "Ratings": reviews
    })

    # Remove rows with missing values
    df.dropna(inplace=True)

    # Reset index after dropping rows
    df.reset_index(drop=True, inplace=True)

    #print(df)
    df.to_csv("C:/Users/sriga/Desktop/flipkart_mobiles/flipkart_mobiles2.csv")


except Exception as e:
    print(f"Error while creating DataFrame: {e}")

