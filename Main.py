import requests
from bs4 import BeautifulSoup
from pprint import pprint
import credentials
import links

from amazon.api import AmazonAPI
amazon = AmazonAPI(credentials.access_key, credentials.secret_key, credentials.ass_tag)

joycon_price = 79
game_price = 59

def extract_source(url):
    headers = {"User-Agent":"Mozilla/5.0"}
    source=requests.get(url, headers=headers).text
    return source

def print_bby_price(item,website):
    #for best buy
    page = extract_source(website)
    soup = BeautifulSoup(page, 'html.parser')
    name_box = soup.find(attrs={'class': 'price-block priceblock-large'})
    price = name_box.get('data-customer-price')
    if float(price) >= joycon_price and item == 'joycons':
        return
    if float(price) >= game_price and item == 'games':
        return
    else:
        print("Best Buy: $"+str(price))

def print_gs_price(item,website):
    #for gamestop
    page = extract_source(website)
    soup = BeautifulSoup(page, 'html.parser')
    name_box = soup.find('h3', attrs={'class': 'ats-prodBuy-price'})
    price1 = name_box.span
    price = price1.text
    if float(price) >= joycon_price and item == 'joycons':
        return
    if float(price) >= game_price and item == 'games':
        return
    else:
        print("Gamestop: $"+str(price))

def print_wal_price(item,website):
    #for walmart
    page = extract_source(website)
    soup = BeautifulSoup(page, 'html.parser')
    name_box = soup.find(attrs={'class': "Price-characteristic"})
    price = name_box.get('content')
    if float(price) >= joycon_price and item == 'joycons':
        return
    if float(price) >= game_price and item == 'games':
        return
    else:
        print("Walmart: $"+str(price))

def print_tar_price(item,website):
    #for target
    page = extract_source(website)
    soup = BeautifulSoup(page, 'html.parser')
    name_box = soup.find(attrs={'data-test': "product-price"})
    price1 = name_box.span
    price2 = price1.text
    price = str(price2).replace('$','')
    if float(price) >= joycon_price and item == 'joycons':
        return
    if float(price) >= game_price and item == 'games':
        return
    else:
        print("Target: $"+str(price))

def print_amazon_price(item,website):
    product = amazon.lookup(ItemId=website)
    price1 = product.price_and_currency[0]
    price = str(price1).replace("Decimal('')",'')
    if float(price) >= joycon_price and item == 'joycons':
        return
    if float(price) >= game_price and item == 'games':
        return
    else:
        print("Amazon: $"+str(price))

def print_dictionary(item,dict):
    for entry in dict:
        if entry == 'bby':
            print_bby_price(item,dict[entry])
        if entry == 'gs':
            print_gs_price(item,dict[entry])
        if entry == 'wal':
            print_wal_price(item,dict[entry])
        if entry == 'tar':
            print_tar_price(item,dict[entry])
        if entry == 'amazon':
            print_amazon_price(item,dict[entry])

print("Joycons:")
print("********")

for item in links.joycons:
    print(item)
    type = 'joycons'
    print_dictionary(type,links.joycons[item])
    print()

print("Games:")
print("******")

for item in links.games:
    print(item)
    type = 'games'
    print_dictionary(type,links.games[item])
    print()
