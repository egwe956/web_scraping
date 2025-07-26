# Web Application Product API Scraper

This Python script scrapes product information from the Adidas UK website using their API endpoints.

## Creator
Evans Wu


## Features

- Uses API endpoints to scrape product information from a web application
- Pagination support (fetches multiple pages of results, can be specified as argument "max_pages")
- Overcome rate limiting protection with random delays
- CSV export of product information
- Detailed product information 

## Requirements

- Python 3.10 or higher (tested with Python 3.12.5)
- Required Python packages:
  - curl_cffi/requests
  - rich
  - time
  - csv
  - random
  - os
  - typing


## Installation

1. Create a virtual environment (****skip if you are familiar with setting up Python virtual environments****):
```bash
mkdir ~/.venv
python3 -m venv ~/.venv
#activate virtual env
source ~/.venv/bin/activate #or you can specify whereever your virtual env is located
```

2. Install dependencies in virtual env:
```bash
pip3 install curl_cffi rich time csv random os typing requests
```

## Usage

1. Find the correct API endpoint:
   - Open the target website in your browser
   - Open Developer Tools/Developer Console
   - Go to the "Network" tab
   - On the front end of the website, navigate around or search for products on the website, with the key goal of locating API requests
   - Look for API requests in the network tab
   - Copy the API endpoint URL and any required parameters
   - Paste the API endpoint URL and find the indirected parameter, for example: "https://www.adidas.co.uk/plp-app/api/search?q={query}&experiment=ATP-6806-1%2CATP-7900-01%2CATP-7981-01&start={current_page}"
   - Replace the {query} and {current_page} with the actual values, for example: "https://www.adidas.co.uk/plp-app/api/search?q=shoes&experiment=ATP-6806-1%2CATP-7900-01%2CATP-7981-01&start=0"

2. - Note: Some websites may use 1-based indexing for pagination rather than 0-based. Check the actual API requests to determine the correct start index.
Modify the start_num parameter in the search_api() function to match the correct start index.

2. Run the script:
```
python3 api.py
```

The script will:
1. Search for products using the specified query
2. Fetch multiple pages of results using pagination
3. Export the results to a CSV file in the same directory as the script


## Output

The script generates a CSV file named `adidas_products.csv` containing all retrieved product information. Each row includes:
- id
- modelNumber
- title
- subTitle
- url
- image asset link
- price
- salePrice
- colourVariations
- customer ratings

## Note
- As different API's are created differently, the script may need to be modified to work with different API's.
