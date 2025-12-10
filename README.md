🤖 Bargain Bot: E-commerce Price Comparison Tool
Bargain Bot is a simple, yet effective Flask web application that scrapes product prices from major Indian e-commerce sites (Amazon India and Snapdeal) and compares them to find the lowest price for the user.

🚀 Features
Price Comparison: Compares product prices between Amazon and Snapdeal.

Lowest Price Identification: Clearly displays the lowest price found and the source.

Direct Links: Provides direct links to the product pages for immediate purchase.

Accessory Filtering: Includes logic to filter out unwanted accessories (like cases, covers, etc.) to focus on the main product.

Simple Web Interface: Easy-to-use search and results pages built with Flask and Jinja2 templating.

📁 Project Structure
The project is divided into three main components: the main Flask application, the web scraping logic, and the user interface (HTML/CSS).

bargain-bot/
├── app.py                 # Main Flask application
├── scrapper.py            # Web scraping functions (snapdeal, amazon, convert)
├── templates/
│   ├── index.html         # Search input page
│   └── results.html       # Price comparison results page
└── static/
    └── style.css          # CSS styles for the web pages
🛠️ Installation and Setup
1. Prerequisites
You need Python 3.x installed on your system.

2. Dependencies
This project requires the following Python libraries:

Flask: For the web application framework.

requests: To make HTTP requests for web scraping.

BeautifulSoup4 (bs4): To parse the HTML content.

You can install all dependencies using pip:

Bash

pip install Flask requests beautifulsoup4
3. Running the Application
Make sure your project files are structured as shown in the Project Structure section.

Open your terminal or command prompt in the root directory of the project (bargain-bot/).

Run the main application file:

Bash

python app.py
The application will start, and you can access it in your web browser at the address provided in the terminal, usually: http://127.0.0.1:5000/

📝 Code Breakdown
app.py
This is the main entry point for the Flask application.

Imports: Imports Flask and the scraping functions from scrapper.py.

Route (/): Handles both GET (display initial search page index.html) and POST (process search query and display results results.html).

POST Logic:

Retrieves product_name from the form.

Calls snapdeal() and amazon() functions to get data.

Calls convert() to transform the raw price string (e.g., "₹1,23,456") into an integer.

Compares the integer prices to determine the absolute minimum price, source, and URL.

Renders results.html with all the data.

scrapper.py
This file contains the logic for making requests, parsing HTML, and cleaning data.

headers: A User-Agent header is used to mimic a real browser, which helps prevent blocks from the websites.

EXCLUDE_KEYWORDS: A list of keywords (e.g., "COVER", "CASE") used to filter out accessories from search results.

convert(a): A utility function using Python's re module to remove all non-digit/non-dot characters from a price string (like currency symbols and commas) and safely convert it to an integer.

snapdeal(name) / amazon(name):

Constructs the search URL.

Sends an HTTP GET request and parses the HTML with BeautifulSoup.

Iterates through search result containers.

Filtering Logic: Implements a matching system:

It checks if the search name is in the product title.

It uses strict_mode (based on whether the search term itself contains accessory keywords) to decide whether to exclude products that are accessories. This helps ensure that a search for "iPhone 13" doesn't return an "iPhone 13 Case."

Returns a dictionary with the raw price and the product url.

📄 HTML Templates (index.html & results.html)
The templates use Jinja2 to dynamically render content.

index.html: Contains a simple form to submit the product name.

results.html:

Displays the product name.

Highlights the best price in a prominent green box.

Iterates through the results dictionary to show a card for every source found, including the display price and a direct "Visit Site" link.

Displays an "No exact matches found" message if min_price is 0.

⚠️ Disclaimer
Web scraping is dependent on the target website's structure. Changes to the HTML of Amazon or Snapdeal (class names, element hierarchy) will likely break the scraping logic in scrapper.py. This project is for educational purposes and personal use. Always respect the terms of service of the websites you are scraping.
