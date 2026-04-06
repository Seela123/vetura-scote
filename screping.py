import os
import psycopg2
import csv
from dotenv import load_dotenv
import requests

load_dotenv()

try:
    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )
    print("Successfully connected to scote_cars!")

except Exception as e:
    print(f"Error connected: {e}")



url = "https://api.veturascout.com/api/listings/advancedSearch"
headers = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
}

limit = 10
page = 1
all_cars = []
max_pages = 190


try:
    cursor = connection.cursor()
    # Define the table structure
    create_table_query = """
    CREATE TABLE IF NOT EXISTS cars_table (
        id INTEGER PRIMARY KEY,
        name VARCHAR(255),
        price NUMERIC,
        brand VARCHAR(100),
        subBrand VARCHAR(100),
        km NUMERIC,
        fuel VARCHAR(50),
        transmission VARCHAR(100),
        city VARCHAR(100),
        year INTEGER
    );
    """
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()
    print("Table 'cars_table' is ready!")
except Exception as e:
    print(f"Failed to create table: {e}")


while page <= max_pages:
    params = {
        "limit":  limit,
        "page":  page
    }

    r = requests.get(url, params=params, headers=headers)
    r.raise_for_status()

    payload = r.json()
    print(payload)
    cars = payload.get("results", [])

    if not cars:
        print(f"no more data on page{page}")
        break

    for car in cars:
        cleaned_cars = {
            "id" : car.get("id"),
            "name":car.get("name"),
            "price": car.get("price"),
            "brand": car.get("brand"),
            "subBrand":car.get("subBrand"),
            "km":car.get("km"),
            "fuel": car.get("fuel"),
            "transmission_name":car.get("transmission_name"),
            "city": car.get("city"),
            "year": car.get("year")
        }
    all_cars.append(cleaned_cars)
    print(f"pages : {page} scraped")

    try:
        cursor = connection.cursor()
        insert_query = """
                    INSERT INTO cars_table (id, name, price, brand, subBrand, km, fuel, transmission, city, year)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING;
                """
        cursor.execute(insert_query, (
            cleaned_cars["id"], cleaned_cars["name"], cleaned_cars["price"],
            cleaned_cars["brand"], cleaned_cars["subBrand"], cleaned_cars["km"], cleaned_cars["fuel"],
            cleaned_cars["transmission_name"], cleaned_cars["city"], cleaned_cars["year"]
        ))
        connection.commit()
        cursor.close()
    except Exception as db_error:
        print(f"Database error: {db_error}")
        connection.rollback()

    page += 1



print("All cars scaped")




with open("vetura_score.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=all_cars[0].keys()
    )
    writer.writeheader()
    writer.writerows(all_cars)
print("data save at vetura_score.csv")