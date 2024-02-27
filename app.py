from bs4 import BeautifulSoup
import requests
import pandas as pd
import time  # Add time module for delay

# Function to extract Product Title
def get_title(soup):
    try:
        title = soup.find("span", attrs={"id": 'productTitle'})
        title_value = title.text.strip()
    except AttributeError:
        title_value = ""
    return title_value

# Function to extract Product Price
def get_price(soup):
    try:
        price = soup.find("span", attrs={'id': 'priceblock_ourprice'}).text.strip()
    except AttributeError:
        try:
            price = soup.find("span", attrs={'id': 'priceblock_dealprice'}).text.strip()
        except:
            price = ""
    return price

# Function to extract Product Rating
def get_rating(soup):
    try:
        rating = soup.find("i", attrs={'class': 'a-icon a-icon-star'}).text.strip()
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class': 'a-icon-alt'}).text.strip()
        except:
            rating = ""
    return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id': 'acrCustomerReviewText'}).text.strip()
    except AttributeError:
        review_count = ""
    return review_count

# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id': 'availability'}).text.strip()
    except AttributeError:
        available = "Not Available"
    return available

def scrape_page(url, headers):
    webpage = requests.get(url, headers=headers)
    soup = BeautifulSoup(webpage.content, "html.parser")

    links = soup.find_all("a", class_='a-link-normal')  # Use a more generic class
    links_list = [link.get('href') for link in links]

    product_details_list = []

    for link in links_list:
        time.sleep(2)  # Add a delay to avoid being blocked
        new_webpage = requests.get("https://www.amazon.in" + link, headers=headers)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")
        product_details = {
            'title': get_title(new_soup),
            'price': get_price(new_soup),
            'rating': get_rating(new_soup),
            'reviews': get_review_count(new_soup),
            'availability': get_availability(new_soup)
        }
        product_details_list.append(product_details)
        print(product_details)

    return product_details_list

if __name__ == '__main__':
    base_url = "https://www.amazon.in/s?bbn=6612025031&rh=n%3A6612025031%2Cp_n_feature_four_browse-bin%3A48812450031&dc&qid=1708971254&rnid=48812332031&ref=lp_6612025031_nr_p_n_feature_four_browse-bin_0"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'}

    all_product_details = []

    for page in range(1, 20):  # Adjust the range according to the number of pages you want to scrape
        page_url = f"{base_url}&page={page}"
        product_details = scrape_page(page_url, headers)
        all_product_details.extend(product_details)

    df = pd.DataFrame(all_product_details)
    df.to_csv("amazon_product_data.csv", index=False)
