from flask import Flask, render_template, request
from scrapper import snapdeal, amazon, convert

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        product_name = request.form.get('product_name')
        
        sd_data = snapdeal(product_name)
        am_data = amazon(product_name)
        
        sd_price_int = convert(sd_data['price'])
        am_price_int = convert(am_data['price'])
        
        results = {}

        if am_price_int > 0:
            results['Amazon'] = {
                'price': am_price_int, 
                'url': am_data['url'],
                'display_price': am_data['price'],
                'rating': am_data['rating']
            }
        
        if sd_price_int > 0:
            results['Snapdeal'] = {
                'price': sd_price_int, 
                'url': sd_data['url'],
                'display_price': sd_data['price'],
                'rating' : sd_data['rating']
            }

        min_price = float('inf')
        min_source = "N/A"
        min_url = "#"

        for source, data in results.items():
            if data['price'] < min_price:
                min_price = data['price']
                min_source = source
                min_url = data['url']

        if min_price == float('inf'):
            min_price = 0

        return render_template('results.html', 
                               product_name=product_name,
                               min_price=min_price,
                               min_source=min_source,
                               min_url=min_url,
                               results=results)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)