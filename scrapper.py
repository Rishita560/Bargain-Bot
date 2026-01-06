import requests
from bs4 import BeautifulSoup
import re 
from rapidfuzz import fuzz

headers = {'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
           'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.google.com/',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Connection': 'keep-alive',}

EXCLUDE_KEYWORDS = ["CASE","SLEEVES", "COVER", "SCREEN PROTECTOR", "CHARGER", "CABLE", "ADAPTER", "GUARD", "BACK", "TABLE", "STAND", "BAGS", "SKIN", "BATTERY", "BAG"]

def convert(a):
    try:
        cleaned_string = re.sub(r'[^\d.]', '', str(a))
        if not cleaned_string:
            return 0
        return int(float(cleaned_string))
    except (ValueError, TypeError):
        return 0

def smart_match(query, title, threshold=70):
    score = fuzz.token_set_ratio(query, title)
    return score >= threshold

def snapdeal(name):
    try:
        name_modified = name.replace(" ", "+")
        url = f"https://www.snapdeal.com/search?clickSrc=top_searches&keyword={name_modified}&categoryId=0&vertical=p&noOfResults=20&SRPID=topsearch&sort=rlvncy"
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        product_containers = soup.select(".product-tuple-listing") 
        
        name_upper = name.upper()
        strict_mode = not any(k in name_upper for k in EXCLUDE_KEYWORDS)
        
        for container in product_containers:
            title = container.select_one(".product-title")
            price = container.select_one(".lfloat.product-price") 
            link = container.select_one("a.dp-widget-link")
            stars = container.select_one(".filled-stars")

            if not title or not price:
                continue

            prod_rating = 0.0 

            if stars:
                style_value = stars.get('style') 
                
                if style_value:
                    try:
                        rating_percentage_str = style_value.replace("width:", "").replace("%", "").strip()
                        rating_percentage = float(rating_percentage_str)
                        prod_rating = rating_percentage / 20.0 
                    except ValueError:
                        prod_rating = 0.0 
                        

            prod_name = title.getText().strip()
            prod_price = price.getText().strip().replace("Rs.","").replace("₹", "")
            prod_name_upper = prod_name.upper()
            

            is_match = smart_match(name_upper, prod_name_upper)
            is_accessory = any(k in prod_name_upper for k in EXCLUDE_KEYWORDS)

            valid = False
            if strict_mode:
                if is_match and not is_accessory:
                    valid = True
            else:
                if is_match:
                    valid = True

            if valid:
                found_url = link['href'] if link else url
                return {'price': prod_price, 'url': found_url, 'rating': prod_rating}
        
        return {'price': '0', 'url': '', 'rating': 0.0}

    except Exception as e:
        print(f"Snapdeal Error: {e}")
        return {'price': '0', 'url': '', 'rating': 0.0}
    

def amazon(name):
    try:
        name_modified = name.replace(" ", "+")
        url = f"https://www.amazon.in/s?k={name_modified}"
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        
        product_containers = soup.select(".s-result-item[data-asin]")
        
        name_upper = name.upper()
        strict_mode = not any(k in name_upper for k in EXCLUDE_KEYWORDS)
        
        for container in product_containers:
            title = container.select_one(".a-text-normal")
            price = container.select_one(".a-price-whole")
            link = container.select_one("a.a-link-normal") 
            rating_element = container.select_one('a[aria-label*="out of 5 stars"]')

            if not title or not price:
                continue

            prod_rating = 0.0 

            if rating_element:
                try:
                    rating_label = rating_element['aria-label']
                    rating_str = rating_label.split(' ')[0]
                    prod_rating = float(rating_str)
                    
                except (KeyError, ValueError, IndexError):
                    prod_rating = 0.0

            prod_name = title.getText().strip()
            prod_price = price.getText().strip()
            prod_name_upper = prod_name.upper()

            is_match = smart_match(name_upper, prod_name_upper)
            is_accessory = any(k in prod_name_upper for k in EXCLUDE_KEYWORDS)

            valid = False
            if strict_mode:
                if is_match and not is_accessory:
                    valid = True
            else:
                if is_match:
                    valid = True

            if valid:
                relative_url = link['href'] if link else ""
                final_url = f"https://www.amazon.in{relative_url}" if relative_url else url
                return {'price': prod_price, 'url': final_url, 'rating': prod_rating}
        
        return {'price': '0', 'url': '', 'rating': 0.0}
        
    except Exception as e:
        print(f"Amazon Error: {e}")
        return {'price': '0', 'url': '', 'rating': 0.0}