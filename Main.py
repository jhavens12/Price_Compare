import requests
from bs4 import BeautifulSoup
from pprint import pprint
import credentials
import links

from amazon.api import AmazonAPI
amazon = AmazonAPI(credentials.access_key, credentials.secret_key, credentials.ass_tag)

joycon_price = 79
game_price = 59

joycon_dict = links.joycons.copy()

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
    if float(price) >= joycon_price and item == 'joycon':
        return
    if float(price) >= game_price and item == 'games':
        return
    else:
        return("Best Buy: $"+str(price))

def print_gs_price(item,website):
    #for gamestop
    page = extract_source(website)
    soup = BeautifulSoup(page, 'html.parser')
    name_box = soup.find('h3', attrs={'class': 'ats-prodBuy-price'})
    price1 = name_box.span
    price = price1.text
    if float(price) >= joycon_price and item == 'joycon':
        return
    if float(price) >= game_price and item == 'games':
        return
    else:
        return("Gamestop: $"+str(price))

def print_wal_price(item,website):
    #for walmart
    page = extract_source(website)
    soup = BeautifulSoup(page, 'html.parser')
    name_box = soup.find(attrs={'class': "Price-characteristic"})
    price = name_box.get('content')
    if float(price) >= joycon_price and item == 'joycon':
        return
    if float(price) >= game_price and item == 'games':
        return
    else:
        return("Walmart: $"+str(price))

def print_tar_price(item,website):
    #for target
    page = extract_source(website)
    soup = BeautifulSoup(page, 'html.parser')
    name_box = soup.find(attrs={'data-test': "product-price"})
    price1 = name_box.span
    price2 = price1.text
    price = str(price2).replace('$','')
    if float(price) >= joycon_price and item == 'joycon':
        return
    if float(price) >= game_price and item == 'games':
        return
    else:
        return("Target: $"+str(price))

def print_amazon_price(item,website):
    product = amazon.lookup(ItemId=website)
    price1 = product.price_and_currency[0]
    price = str(price1).replace("Decimal('')",'')
    if float(price) >= joycon_price and item == 'joycon':
        return
    if float(price) >= game_price and item == 'games':
        return
    else:
        return("Amazon: $"+str(price))

def print_dictionary(dict):
    print_dict = {}
    for entry in dict: #need to give functions website
        for link in dict[entry]['links']:
            if entry == 'bby':
                print_list['bby_price'] = print_bby_price(dict[entry]['type'],dict[entry]['links'][link]) #give 'joycons' and link dictionary
            if entry == 'gs':
                print_list['gs_price'] = print_gs_price(dict[entry]['type'],dict[entry]['links'][link])
            if entry == 'wal':
                print_list['wal_price'] = print_wal_price(dict[entry]['type'],dict[entry]['links'][link])
            if entry == 'tar':
                print_list['tar_price'] = print_tar_price(dict[entry]['type'],dict[entry]['links'][link])
            if entry == 'amazon':
                print_list['amazon_price'] = print_amazon_price(item,dict[entry])
    if bby_price == None and gs_price == None and wal_price == None and tar_price == None and amazon_price == None:
        return
    else:
        print(dict)
        for price in print_dict:
            if print_dict[price] != None:
                print(price+": "+str(print_dict[price]))


# print("Joycons:")
# print("********")

for item in joycon_dict:
    #print(item)
    print_dictionary(joycon_dict[item])#['type'],joycon_dict[item]['links'])
    print()

# print("Games:")
# print("******")
#
# for item in links.games:
#     print(item)
#     type = 'games'
#     print_dictionary(type,links.games[item])
#     print()
