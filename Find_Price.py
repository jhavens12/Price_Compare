import requests
from bs4 import BeautifulSoup
from pprint import pprint
import credentials
import links
import yagmail

gmail_user = credentials.gmail_user
gmail_password = credentials.gmail_password
yag = yagmail.SMTP( gmail_user, gmail_password)

from amazon.api import AmazonAPI
amazon = AmazonAPI(credentials.access_key, credentials.secret_key, credentials.ass_tag)

#input link dictionary
#calculate prices - create new dictionary?
#compare prices to MSRP
#print if on sale
#possibly compare pricing to historical prices

def extract_source(url):
    headers = {"User-Agent":"Mozilla/5.0"}
    source=requests.get(url, headers=headers).text
    return source

def bby(website):
    page = extract_source(website)
    soup = BeautifulSoup(page, 'html.parser')
    name_box = soup.find(attrs={'class': 'price-block priceblock-large'})
    price = name_box.get('data-customer-price')
    return price

def gs(website):
    page = extract_source(website)
    soup = BeautifulSoup(page, 'html.parser')
    name_box = soup.find('h3', attrs={'class': 'ats-prodBuy-price'})
    price1 = name_box.span
    price = price1.text
    return price

def walmart(website):
    page = extract_source(website)
    soup = BeautifulSoup(page, 'html.parser')
    name_box = soup.find(attrs={'class': "Price-characteristic"})
    price = name_box.get('content')
    return price

def target(website):
    page = extract_source(website)
    soup = BeautifulSoup(page, 'html.parser')
    name_box = soup.find(attrs={'data-test': "product-price"})
    price1 = name_box.span
    price2 = price1.text
    price = str(price2).replace('$','')
    return price

def get_amazon(website):
    product = amazon.lookup(ItemId=website)
    price1 = product.price_and_currency[0]
    price = str(price1).replace("Decimal('')",'')
    return price

def eshop(website):
    page = extract_source(website)
    soup = BeautifulSoup(page, 'html.parser')
    name_box = soup.find(attrs={'class': 'sale-price'})
    test = str(name_box.text).replace("\n",'')
    test2 = test.replace("*",'')
    sale_price = test2.replace("$",'')
    if sale_price == '':
        soup = BeautifulSoup(page, 'html.parser')
        name_box = soup.find(attrs={'class': 'msrp'})
        test = str(name_box.text).replace("\n",'')
        test2 = test.replace("*",'')
        msrp = test2.replace("$",'')
        return msrp
    else:
        return sale_price


def get_prices(dict):
    price_dict = {}
    for entry in dict:
        if entry == 'bby':
            price_dict[entry] = bby(dict[entry])
        if entry == 'gs':
            price_dict[entry] = gs(dict[entry])
        if entry == 'wal':
            price_dict[entry] = walmart(dict[entry])
        if entry == 'tar':
            price_dict[entry] = target(dict[entry])
        if entry == 'amazon':
            price_dict[entry] = get_amazon(dict[entry])
        if entry == 'eshop':
            price_dict[entry] = eshop(dict[entry])
    return price_dict

def print_price_dict(item,msrp,dict):
    print(item)
    print("MSRP: "+str(msrp))
    print("*****")
    for entry in dict: #for each price listing for item
        if float(dict[entry]) < msrp:
            if entry == 'bby':
                print("Best Buy: $"+dict[entry])
            if entry == 'gs':
                print("Game Stop: $"+dict[entry])
            if entry == 'wal':
                print("Walmart: $"+dict[entry])
            if entry == 'tar':
                print("Target: $"+dict[entry])
            if entry == 'amazon':
                print("Amazon: $"+dict[entry])
            if entry == 'eshop':
                print("eShop: $"+dict[entry])
    print()

def build_output(item,msrp,dict,link_dict): #this will be done for each item
    list1 = []
    list1.append(item + " - "+"MSRP: "+str(msrp)+'\n*******')
    for entry in dict: #for each price listing for item
        if float(dict[entry]) < msrp:
            if entry == 'bby':
                list1.append('Best Buy: <a href='+link_dict[entry]+'>$'+dict[entry]+'</a>')
            if entry == 'gs':
                list1.append('Game Stop: <a href='+link_dict[entry]+'>$'+dict[entry]+'</a>')
            if entry == 'wal':
                list1.append('Walmart: <a href='+link_dict[entry]+'>$'+dict[entry]+'</a>')
            if entry == 'tar':
                list1.append('Target: <a href='+link_dict[entry]+'>$'+dict[entry]+'</a>')
            if entry == 'amazon':
                list1.append('Amazon: <a href=https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords='+link_dict[entry]+'>$'+dict[entry]+'</a>')
            if entry == 'eshop':
                list1.append('eShop: <a href='+link_dict[entry]+'>$'+dict[entry]+'</a>')
    list1.append('\n')

    if len(list1) > 2:
        return list1
    else:
        return None


send_list = []
send_list.append("<b><font size='+2'>Joycons:</b></font>\n")

for item in links.joycons:
    price_dict = get_prices(links.joycons[item]['links'])
    #print_price_dict(item,links.joycons[item]['msrp'],price_dict) #msrp and price dict
    print_list = build_output(item,links.joycons[item]['msrp'],price_dict,links.joycons[item]['links'])
    if print_list != None: #account for none return if list is None
        test_list = "\n".join(print_list)
        send_list.append(test_list)

send_list.append("<b><font size='+2'>Games:</b></font>\n")

for item in links.games:
    price_dict = get_prices(links.games[item]['links'])
    #print_price_dict(item,links.joycons[item]['msrp'],price_dict) #msrp and price dict
    print_list = build_output(item,links.games[item]['msrp'],price_dict,links.games[item]['links'])
    if print_list != None: #account for none return if list is None
        test_list = "\n".join(print_list)
        send_list.append(test_list)

real_send = "".join(send_list)

#jon_contents = 'Email Gropus: ' + '\n\n'
#html = '<a href="https://google.com">New Staff Process spreadsheet</a>'
yag.send('jhavens12@gmail.com', 'SWITCH Pricing', [real_send])
