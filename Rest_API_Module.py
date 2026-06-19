# Import requests library to make API calls (HTTP requests)
import requests

# Import json to read/write data in JSON format
import json

# Import os to work with files (check if file exists, etc.)
import os


# Class responsible for fetching country data from REST Countries API
class CountryAPIClient:

    # Base URL for the API (endpoint for searching countries by name)
    BASE_URL = "https://restcountries.com/v3.1/name/"

    # Method to get country details using country name
    def get_country(self, country_name):

        # Check if input is empty or just spaces
        if not country_name or not country_name.strip():
            raise ValueError("Invalid country name.")  # Raise error if invalid

        try:
            # Create full API URL by adding the country name
            url = f"{self.BASE_URL}{country_name.strip()}"

            # Send GET request to the API (timeout prevents long waiting)
            response = requests.get(url, timeout=5)

            # Raise error if response status is not 200 (success)
            response.raise_for_status()

            # Convert API response to Python dictionary
            data = response.json()

            # Get the first result (API returns a list)
            country = data[0]

            # Get currencies dictionary (or empty if missing)
            currencies = country.get("currencies", {})

            # Get languages dictionary (or empty if missing)
            languages = country.get("languages", {})

            # Return cleaned and structured country data
            return {
                # Get country name safely (avoid missing key error)
                "name": country.get("name", {}).get("common", "N/A"),

                # Capital is a list → take first item
                "capital": country.get("capital", ["N/A"])[0],

                # Population value
                "population": country.get("population", "N/A"),

                # Region (Africa, Europe, etc.)
                "region": country.get("region", "N/A"),

                # Get currency name safely
                "currency": list(currencies.values())[0]["name"] if currencies else "N/A",

                # Join all languages into one string
                "languages": ", ".join(languages.values()) if languages else "N/A",

                # Get first timezone from list
                "timezone": country.get("timezones", ["N/A"])[0],

                # Get flag image URL
                "flag": country.get("flags", {}).get("png", "")
            }

        # If country is not found (404 error)
        except requests.exceptions.HTTPError:
            raise ValueError("Country not found.")

        # If network fails (no internet, timeout, etc.)
        except requests.exceptions.RequestException:
            raise ConnectionError("API request failed.")


# Import the LocalStorage class from the separate module
from local_storage import LocalStorage


# This block runs only when file is executed directly (not imported)
if __name__ == "__main__":

    # Create API client object
    api = CountryAPIClient()

    # Create storage object
    storage = LocalStorage()

    try:
        # Fetch country data from API
        country = api.get_country("Canada")

        # Print fetched data
        print(country)

        # Save country data locally
        storage.save("Canada", country)

        # Load saved data
        saved = storage.load("Canada")

        # Print loaded data
        print("Loaded:", saved)

    # Catch and print any errors
    except Exception as e:
        print(e)