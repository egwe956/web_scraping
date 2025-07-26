from playwright.sync_api import sync_playwright
import json

def extract_currency_values(page):
    """Extract all span.currency-value elements and their text content."""
    currency_spans = page.query_selector_all("span.currency-value")
    # print(f"Found {len(currency_spans)} currency value spans")
    
    currency_values = []
    for span in currency_spans:
        text = span.text_content().strip()
        if text:
            # print(f"Found currency value: {text}")
            currency_values.append(text)
    return currency_values

def extract_h3_elements(page):
    """Extract all h3 elements and their text content."""
    h3_elements = page.query_selector_all("h3")
    # print(f"Found {len(h3_elements)} h3 elements")
   
    headings = []
    for h3 in h3_elements:
        text = h3.text_content().strip()
        if text:
            # print(f"Found h3 heading: {text}")
            headings.append(text)
    return headings

def scrape_etsy_text():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Add URL to navigate to
        page.goto("https://www.etsy.com/sg-en/featured/hub/back-to-school")  # Replace with actual Etsy URL
        
        # Extract currency values and headings
        currency_values = extract_currency_values(page)
        headings = extract_h3_elements(page)
        
        # Create dictionary to store the merged data
        merged_data = []
        
        # Pair currency values with headings
        min_length = min(len(currency_values), len(headings))
        for i in range(min_length):
            merged_data.append({
                "heading": headings[i],
                "price": currency_values[i]
            })
        
        # Handle any remaining items
        if len(currency_values) > len(headings):
            for i in range(len(headings), len(currency_values)):
                merged_data.append({
                    "heading": "",  # Empty heading for unmatched price
                    "price": currency_values[i]
                })
        elif len(headings) > len(currency_values):
            for i in range(len(currency_values), len(headings)):
                merged_data.append({
                    "heading": headings[i],
                    "price": ""  # Empty price for unmatched heading
                })
        
        # Convert to JSON and print
        print(json.dumps(merged_data, indent=2))
        
        browser.close()
        return merged_data
        # Launch browser with default settings
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navigate to Etsy
        url = "https://www.etsy.com/sg-en/featured/hub/back-to-school"
        print(f"Navigating to: {url}")
        page.goto(url, wait_until="networkidle")
        
        # Extract currency values
        currency_values = extract_currency_values(page)
        print("\nCurrency Values:")
        print(json.dumps(currency_values, indent=2))
        
        # Extract h3 headings
        h3_headings = extract_h3_elements(page)
        print("\nH3 Headings:")
        print(json.dumps(h3_headings, indent=2))
        
        # Extract all paragraph text
        # paragraphs = page.query_selector_all("p")
        # print(f"Found {len(paragraphs)} paragraph elements")
        
        # Extract text content from each paragraph
        # text_content = []
        # for p in paragraphs:
        #     text = p.text_content().strip()
        #     if text:
        #         print(f"Found paragraph: {text}")
        #         text_content.append(text)
        
        # Output results
        print("\nExtracted Data:")
        # print("Paragraph Text:")
        # print(json.dumps(text_content, indent=2))
        print("\nCurrency Values:")
        print(json.dumps(currency_values, indent=2))
        print("\nH3 Headings:")
        print(json.dumps(h3_headings, indent=2))
        
        browser.close()
        
        # Output results
        print("\nExtracted Text:")
        # print(json.dumps(text_content, indent=2))
        # return text_content

if __name__ == "__main__":
    scrape_etsy_text()
