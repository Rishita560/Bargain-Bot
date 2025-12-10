import requests
from bs4 import BeautifulSoup
import re 

headers = {'User-Agent' : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"}

EXCLUDE_KEYWORDS = ["CASE","SLEEVES", "COVER", "SCREEN PROTECTOR", "CHARGER", "CABLE", "ADAPTER", "GUARD", "BACK"]

def convert(a):
    try:
        cleaned_string = re.sub(r'[^\d.]', '', str(a))
        if not cleaned_string:
            return 0
        return int(float(cleaned_string))
    except (ValueError, TypeError):
        return 0

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

            if not title or not price:
                continue

            prod_name = title.getText().strip()
            prod_price = price.getText().strip().replace("Rs.","").replace("₹", "")
            prod_name_upper = prod_name.upper()

            is_match = name_upper in prod_name_upper
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
                return {'price': prod_price, 'url': found_url}
        
        return {'price': '0', 'url': ''}

    except Exception as e:
        print(f"Snapdeal Error: {e}")
        return {'price': '0', 'url': ''}

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
            link = container.select_one("span.a-size-base-plus > a.a-link-normal") 

            if not title or not price:
                continue

            prod_name = title.getText().strip()
            prod_price = price.getText().strip()
            prod_name_upper = prod_name.upper()

            is_match = name_upper in prod_name_upper
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
                return {'price': prod_price, 'url': final_url}
        
        return {'price': '0', 'url': ''}
        
    except Exception as e:
        print(f"Amazon Error: {e}")
        return {'price': '0', 'url': ''}