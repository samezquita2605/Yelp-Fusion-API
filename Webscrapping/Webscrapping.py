import requests
import csv
import time

def fetch_indian_restaurants(api_key, location, category, output_file, max_results=100):
    """
    Fetches Indian restaurants in the specified location and writes their names and addresses to a CSV file.

    Parameters:
    - api_key (str): Your Yelp Fusion API key.
    - location (str): The location to search in (e.g., "Toronto, ON").
    - category (str): Yelp category code for Indian restaurants (e.g., "indpak").
    - output_file (str): The name of the CSV file to save the data.
    - max_results (int): Maximum number of restaurants to fetch (Yelp allows up to 1000).
    """
    headers = {
        'Authorization': f'Bearer {api_key}',
    }
    url = 'https://api.yelp.com/v3/businesses/search'
    
    all_restaurants = []
    limit = 50  # Maximum number of results per request
    offset = 0
    
    while offset < max_results:
        params = {
            'term': 'Indian Restaurants',
            'location': location,
            'categories': category,
            'limit': limit,
            'offset': offset
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"Error fetching data: {response.status_code}")
            print(response.json())
            break
        
        data = response.json()
        businesses = data.get('businesses', [])
        
        if not businesses:
            print("No more businesses found.")
            break
        
        for business in businesses:
            name = business.get('name', 'N/A')
            address = ", ".join(business.get('location', {}).get('display_address', []))
            all_restaurants.append({'Name': name, 'Address': address})
        
        fetched = len(businesses)
        print(f"Fetched {fetched} businesses (Total: {offset + fetched})")
        
        offset += fetched
        
        # To respect rate limits (adjust sleep time if necessary)
        time.sleep(1)
    
    # Write to CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Name', 'Address']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(all_restaurants)
    
    print(f"Data successfully saved to {output_file}")

if __name__ == "__main__":
    # Replace 'YOUR_YELP_API_KEY' with your actual Yelp API key
    API_KEY = '2j_bueKy3e_LQOxtccF-k5QXy8WhKYcKLRBl6c7GOuytggMF1Nw1ClmhxHuaudBUYpKH5JTT9mRPLuk2ZU5f6UQwfnt-mQDO2hpYC4wPuoo_UJUaM5S09vB0PW8yZ3Yx'
    
    LOCATION = 'Toronto, ON'
    CATEGORY = 'indpak'  # Yelp category code for Indian/Pakistani
    OUTPUT_FILE = 'indian_restaurants_toronto.csv'
    MAX_RESULTS = 200  # You can set this up to 1000 as per Yelp's limit
    
    fetch_indian_restaurants(API_KEY, LOCATION, CATEGORY, OUTPUT_FILE, MAX_RESULTS)
