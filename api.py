from rich import print
from curl_cffi import requests
from typing import Optional, List, Any
import os
import time
import csv
from random import uniform, choice




def get_random_user_agent():
    """Return a random user agent string"""
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:120.0) Gecko/20100101 Firefox/120.0"
    ]
    return choice(user_agents)

def new_session():
    """Create a new session with random user agent and proxy rotation"""
    # get random user agent
    user_agent = get_random_user_agent()
    
    # create session with random user agent
    session = requests.Session(impersonate="chrome", proxy=os.getenv("stickyproxy"))
    session.headers.update({"User-Agent": user_agent})
    
    # add headers that mimic a real browser
    session.headers.update({
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
    })
    
    return session

def add_request_delay():
    """Add a random delay between 5-10 seconds between requests"""
    delay = uniform(2, 5)  # random delay between 2-5 seconds
    print(f"Adding delay of {delay:.2f} seconds between requests...")
    time.sleep(delay)


def _make_request(session: requests.Session, url: str, max_retries: int = 5) -> Any:
    """Make a request with retry logic and exponential backoff."""
    retry_count = 0
    while retry_count < max_retries:
        try:
            resp = session.get(url)
            resp.raise_for_status()
            return resp
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                # use the existing add_request_delay function for consistent delay handling
                add_request_delay()
                retry_count += 1
            else:
                raise
    raise Exception("Max retries reached")


def search_api(session: requests.Session, query: str, start_num: int = 1, max_pages: int = 20):
    """
    Search for products using web application API with pagination support.
    Will fetch multiple pages until all items are retrieved or max_pages is reached.
    """
    all_products = []
    current_page = start_num
    total_items = 0
    response_data = None  # Initialize response_data
    
    try:
        while current_page <= max_pages:
            # Add page parameter to URL
            url = f"https://www.adidas.co.uk/plp-app/api/search?q={query}&experiment=ATP-6806-1%2CATP-7900-01%2CATP-7981-01&start={current_page}"
            add_request_delay()
            resp = _make_request(session, url)
            
            try:
                response_data = resp.json()
                print(f"\nPage {current_page} response structure: {response_data.keys()}")
                
                if "products" in response_data and response_data["products"]:
                    products = response_data["products"]
                    num_items = len(products)
                    total_items += num_items
                    print(f"\nPage {current_page}: Found {num_items} products")
                    
                    # Add products to our list
                    all_products.extend(products)
                    
                    # Print only first product info for each page
                    if products:
                        product = products[0]
                        print(f"First product on page {current_page}:")
                        print(f"Title: {product.get('title', 'N/A')}")
                        print(f"Price: {product.get('priceData', {}).get('price', 'N/A')}")
                        print(f"Sale Price: {product.get('priceData', {}).get('salePrice', 'N/A')}")
                    
                    # If we got fewer items than expected, we've likely reached the end
                    if num_items < 48:  # Assuming 48 items per page
                        break
                    
                    current_page += 1
                else:
                    print(f"\nNo products found on page {current_page}")
                    break
                
            except Exception as e:
                print(f"Error parsing response on page {current_page}: {str(e)}")
                break

        # Create final response with all products
        final_response = {
            "info": response_data.get("info", {}),
            "querySuggestions": response_data.get("querySuggestions", []),
            "title": response_data.get("title", ""),
            "products": all_products,
            "breadcrumbs": response_data.get("breadcrumbs", []),
            "filters": response_data.get("filters", []),
            "sortRules": response_data.get("sortRules", []),
            "selectedFilters": response_data.get("selectedFilters", [])
        }
        
        print(f"\nTotal items retrieved: {total_items}")
        return final_response

    except Exception as e:
        print(f"Error in search_api: {str(e)}")
        raise
    

def convert_to_csv(response_data, filename="product_info.csv"):
    # convert response data to CSV format.
    if "products" not in response_data:
        print("No products found in response data")
        return
    
    # for debugging purpose - Get the keys from the first product to use as headers
    products = response_data["products"]
    if not products:
        print("No products found")
        return
    
    # get all possible keys from the first product
    headers = []
    first_product = products[0]
    for key in first_product:
        if isinstance(first_product[key], dict):
            # For nested dictionaries like priceData, get their keys
            for nested_key in first_product[key]:
                headers.append(f"{key}_{nested_key}")
        else:
            headers.append(key)
    
    # write to CSV
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)  # Write headers
        
        # write each product's data
        for product in products:
            row = []
            for header in headers:
                # Split header to handle nested keys
                parts = header.split('_')
                if len(parts) == 1:  # Simple key
                    row.append(str(product.get(header, 'N/A')))
                else:  # Nested key
                    base_key = parts[0]
                    nested_key = parts[1]
                    row.append(str(product.get(base_key, {}).get(nested_key, 'N/A')))
            writer.writerow(row)
    
    print(f"\nCSV file '{filename}' has been created with {len(products)} products")


def main():
    session = new_session()
    # search term goes here, value gets passed to search_api function above
    search = search_api(session, "shoes", start_num=0, max_pages=20)  # modify max_pages as needed
    # call CSV export function
    convert_to_csv(search, filename="product_info.csv")
    
if __name__ == "__main__":
    main()