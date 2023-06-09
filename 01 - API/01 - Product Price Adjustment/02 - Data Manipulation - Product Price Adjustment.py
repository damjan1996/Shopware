import pandas as pd
import requests
import math
from datetime import datetime


# Define constants (Replace these with your own details)
ACCESS_KEY = 'YOUR_ACCESS_KEY'
SECRET_KEY = 'YOUR_SECRET_KEY'
URL = 'https://your-url.com/'
TAX = 1.19
FILE_PATH = 'product_price_data.xlsx'  # Path to the data file


# Function to log info messages
def log_info(text):
    now = datetime.now()
    line = "\n[" + now.strftime("%d/%m/%Y %H:%M:%S") + "] " + text + "\n"
    print(line)
    with open('log.txt', 'a') as f:
        f.writelines(line)


# Function to read the data from a file
def read_data():
    data = pd.read_excel(FILE_PATH)
    column_names = ['Art. Nr. \n', 'VK mit MwSt.']
    df = pd.DataFrame(data, columns=column_names)
    values = df[column_names].values.tolist()
    processed_data = []
    for element in values:
        if math.isnan(element[0]) or math.isnan(element[1]):
            continue
        processed_data.append((str(int(element[0])), element[1]))
    return processed_data


# Function to login and get the access token
def login():
    data = {
        "grant_type": "client_credentials",
        "client_id": ACCESS_KEY,
        "client_secret": SECRET_KEY
    }
    r = requests.post(url=URL+'api/oauth/token', data=data)
    res = r.json()
    return res['access_token']

TOKEN = login()


# Function to get all products
def get_all_product():
    header = {
        "Authorization": "Bearer " + TOKEN
    }
    data = {
        "includes": {
            "product": [ "id", "productNumber", "price" ]
        }
    }
    r = requests.post(url=URL + 'api/search/product', headers=header, json=data)
    products = r.json()
    return products


# Function to get a product by its number
def get_product_by_productNumber(productNumber):
    header = {
        "Authorization": "Bearer " + TOKEN
    }
    data = {
        "filter": [
            {
                "type": "equals",
                "field": "productNumber",
                "value": productNumber
            }
        ]
    }
    r = requests.post(url=URL+'api/search/product', headers=header, json=data)
    product = r.json()
    product_id = product['data'][0]['id']
    return product_id, product


# Function to update the price of a product
def update_product_price(product_id, new_gross):
    new_net = new_gross / TAX
    header = {
        "Authorization": "Bearer " + TOKEN
    }
    update_data = {
        "price-update": {
            "entity": "product",
            "action": "upsert",
            "payload": [
                {
                    "id": product_id,
                    "price": [
                        {
                            "currencyId": "b7d2554b0ce847cd82f3ac9bd1c0dfca",
                            "net": new_net,
                            "gross": new_gross,
                            "linked": False,
                            "extensions": []
                        }
                    ]
                }
            ]
        }
    }
    r = requests.post(url=URL+'api/_action/sync', headers=header, json=update_data)
    res = r.json()
    return res['success'] == True


# Main function to update product prices based on the data file
def main():
    data = read_data()  # [('productNumber', new_price)]
    products = get_all_product()
    for d in data:
        for p in products['data']:
            if d[0] == str(p['attributes']['productNumber']):
                if p['attributes']['price'] is None:
                    continue
                if d[1] != p['attributes']['price'][0]['gross']:
                    log_info('Product with id: ' + p['id'] + ' must be updated')
                    flag = update_product_price(p['id'], d[1])
                    info2 = 'Updated product with id:'+p['id']+', and productNumber:'+p['attributes']['productNumber']+' OLD price:'+str(p['attributes']['price'][0]['gross'])+' NEW price:'+str(d[1])
                    if flag:
                        log_info('Successfully ' + info2)
                    else:
                        log_info('Error ' + info2)
                else:
                    log_info('Price is same for product with id: ' + p['id'])


# Run the main function
if __name__ == '__main__':
    main()
