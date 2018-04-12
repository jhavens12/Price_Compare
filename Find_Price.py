import requests
from bs4 import BeautifulSoup
from pprint import pprint
import credentials
import links
import yagmail
from pathlib import Path
import datetime
import pickle

gmail_user = credentials.gmail_user
gmail_password = credentials.gmail_password
yag = yagmail.SMTP( gmail_user, gmail_password)

from amazon.api import AmazonAPI
amazon = AmazonAPI(credentials.access_key, credentials.secret_key, credentials.ass_tag)

def nice_time(time):
    #return str(time.hour)+":"+str(time.minute)+":"+str(time.second)
    #return str(time.time().strftime("%I:%M:%S"))
    return str(time.year)+"/"+str(time.month)+"/"+str(time.day)

def open_file():
    dictionary_file = Path('./History.dict')
    if dictionary_file.is_file():
        pickle_in = open(str(dictionary_file),"rb")
        historical_dict = pickle.load(pickle_in)
        #dictionary already has a timestamp key
    else:
        f=open(str(dictionary_file),"w+") #create file
        f.close()
        historical_dict = {}

    return historical_dict

def close_file(historical_dict):
    historical_dict['timestamp'] = datetime.datetime.now()
    dictionary_file = Path('./History.dict')
    with open(str(dictionary_file), 'w') as outfile:
        #json.dump(history_dict, outfile)
        pickle_out = open(str(dictionary_file),"wb")
        pickle.dump(historical_dict, pickle_out) #save old_dict as it has all of the data
        pickle_out.close()

def extract_source(url):
    headers = {"User-Agent":"Mozilla/5.0"}
    source=requests.get(url, headers=headers).text
    return source

def bby(website):
    try:
        page = extract_source(website)
        soup = BeautifulSoup(page, 'html.parser')
        name_box = soup.find(attrs={'class': 'price-block priceblock-large'})
        price = name_box.get('data-customer-price')
        return price
    except:
        print("BBY ERROR")
        return 99999

def gs(website):
    try:
        page = extract_source(website)
        soup = BeautifulSoup(page, 'html.parser')
        name_box = soup.find('h3', attrs={'class': 'ats-prodBuy-price'})
        price1 = name_box.span
        price = price1.text
        return price
    except:
        print("GS Error")
        return 99999

def walmart(website):
    try:
        page = extract_source(website)
        soup = BeautifulSoup(page, 'html.parser')
        name_box = soup.find(attrs={'class': "Price-characteristic"})
        price = name_box.get('content')
        return price
    except:
        print("Walmart error")
        return 99999

def target(website):
    try:
        page = extract_source(website)
        soup = BeautifulSoup(page, 'html.parser')
        name_box = soup.find(attrs={'data-test': "product-price"})
        price1 = name_box.span
        price2 = price1.text
        price = str(price2).replace('$','')
        return price
    except:
        print("Target error")
        return 99999

def get_amazon(website):
    try:
        product = amazon.lookup(ItemId=website)
        price1 = product.price_and_currency[0]
        price = str(price1).replace("Decimal('')",'')
        return price
    except:
        print("amazon error")
        return 99999

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
        if entry == 'Best Buy':
            price_dict[entry] = bby(dict[entry])
        if entry == 'Game Stop':
            price_dict[entry] = gs(dict[entry])
        if entry == 'Walmart':
            price_dict[entry] = walmart(dict[entry])
        if entry == 'Target':
            price_dict[entry] = target(dict[entry])
        if entry == 'Amazon':
            price_dict[entry] = get_amazon(dict[entry])
        if entry == 'eShop':
            price_dict[entry] = eshop(dict[entry])
    return price_dict

def print_price_dict(item,msrp,dict):
    print(item)
    print("MSRP: "+str(msrp))
    print("*****")
    for entry in dict: #for each price listing for item
        if float(dict[entry]) < msrp:
            if entry == 'Best Buy':
                print("Best Buy: $"+dict[entry])
            if entry == 'Game Stop':
                print("Game Stop: $"+dict[entry])
            if entry == 'Walmart':
                print("Walmart: $"+dict[entry])
            if entry == 'Target':
                print("Target: $"+dict[entry])
            if entry == 'Amazon':
                print("Amazon: $"+dict[entry])
            if entry == 'eShop':
                print("eShop: $"+dict[entry])
    print()

def build_output(historical_dict,item,msrp,dict,link_dict): #this will be done for each item
    list1 = []
    #list1.append(item + " - "+"MSRP: "+str(msrp)+'\n*******')
    history = "Low: $"+str(historical_dict[item]['low_price'])+"\nAt: "+nice_time(historical_dict[item]['low_price_time'])+"\nOn: "+historical_dict[item]['location']+"\n"
    list1.append("<font size='+1'>"+ item + " - " + "MSRP: $" + str(msrp) + '\n</font>'+history+'************')

    for entry in dict: #for each price listing for item
        if float(dict[entry]) < msrp:
            if entry == 'Best Buy':
                list1.append('Best Buy: <a href='+link_dict[entry]+'>$'+dict[entry]+'</a>')
            if entry == 'Game Stop':
                list1.append('Game Stop: <a href='+link_dict[entry]+'>$'+dict[entry]+'</a>')
            if entry == 'Walmart':
                list1.append('Walmart: <a href='+link_dict[entry]+'>$'+dict[entry]+'</a>')
            if entry == 'Target':
                list1.append('Target: <a href='+link_dict[entry]+'>$'+dict[entry]+'</a>')
            if entry == 'Amazon':
                list1.append('Amazon: <a href=https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords='+link_dict[entry]+'>$'+dict[entry]+'</a>')
            if entry == 'eShop':
                list1.append('eShop: <a href='+link_dict[entry]+'>$'+dict[entry]+'</a>')
    list1.append('\n')

    if len(list1) > 2:
        return list1
    else:
        return None

def compare_historical(item,historical_dict,price_dict):
    #pprint(price_dict) #bby as key, price as value
    if item not in historical_dict:
        historical_dict[item] = {}
        historical_dict[item]['low_price'] = 99999
        historical_dict[item]['low_price_time'] = 0
    for value in price_dict: #for each  value
        if float(price_dict[value]) < float(historical_dict[item]['low_price']):
            historical_dict[item]['location'] = value
            historical_dict[item]['low_price'] = price_dict[value]
            historical_dict[item]['low_price_time'] = datetime.datetime.now()

historical_dict = open_file()

send_list = []
send_list.append("<b><font size='+2'>Joycons:</font></b>\n\n")

for item in links.joycons:
    price_dict = get_prices(links.joycons[item]['links'])
    #print_price_dict(item,links.joycons[item]['msrp'],price_dict) #msrp and price dict
    compare_historical(item,historical_dict,price_dict)
    print_list = build_output(historical_dict,item,links.joycons[item]['msrp'],price_dict,links.joycons[item]['links'])
    if print_list != None: #account for none return if list is None
        test_list = "\n".join(print_list)
        send_list.append(test_list)

send_list.append("<b><font size='+2'>Games:</font></b>\n\n")

for item in links.games:
    price_dict = get_prices(links.games[item]['links'])
    #print_price_dict(item,links.joycons[item]['msrp'],price_dict) #msrp and price dict
    compare_historical(item,historical_dict,price_dict)
    print_list = build_output(historical_dict,item,links.games[item]['msrp'],price_dict,links.games[item]['links'])
    if print_list != None: #account for none return if list is None
        test_list = "\n".join(print_list)
        send_list.append(test_list)

close_file(historical_dict) #save historical lows

real_send = "".join(send_list)

yag.send('jhavens12@gmail.com', 'SWITCH Pricing', [real_send])
