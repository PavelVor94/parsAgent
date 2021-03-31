import requests
import lxml.html as html
from io import StringIO
from pandas import DataFrame
import time
import sys

BASE_URL = 'https://www.primelocation.com/find-agents/estate-agents/directory/'
URL_COMPANY = 'https://www.primelocation.com/find-agents/estate-agents/company'
CATEGORY = ['A','B' ,'C' ,'D' ,'E' ,'F' ,'G' ,'H' ,'I' ,'J' ,'K' ,'L' ,'M' ,'N' ,'O' ,'P' ,'Q' ,'R' ,'S' ,'T' ,'U' ,'V' ,'W' ,'X' ,'Y' ,'Z' ,'123']

list_result = []
start = time.time()
count=0

def load_category():
    for char in CATEGORY:
        response = requests.get(BASE_URL+char)
        main_page = html.parse(StringIO(response.content.decode()))
        links = main_page.xpath('//ul[contains(@class, "clearfix")]/li/a')
        for link in links:
            load_company(link.text.strip() , URL_COMPANY+link.attrib['href'].strip()+'?page_size=50')
            DataFrame(list_result).to_csv('./product.csv' , sep='\t' , index=False, encoding='utf-16')

    print(time.time()-start)

def load_company(main_name, url):
    global count
    try:
        response = requests.get(url)
        main_page = html.parse(StringIO(response.content.decode()))
        divs = main_page.xpath('//div[contains(@class, "clearfix agents-results-item")]')
        for div in divs:
            office_name = div.xpath('//h2/a')[0].text
            office_address = div.xpath('//div[contains(@class, "agents-results-copy")]/p/span/text()')[0].strip()
            office_telephone = div.xpath('//a[contains(@class, "agent_phone")]/text()')[0]
            stats = div.xpath('//div[contains(@class, "agents-stats")]')[2:]
            if stats:
                resident_for_sale = stats[0][0][0].text
                Avg_asking_price = stats[1][0].text
                Avg_sale_listing_age = stats[2][0].text
                if len(stats)>4:
                    resident_for_rent = stats[4][0][0].text
                else:
                    resident_for_rent = ""
                if len(stats) > 5:
                    Avg_asking_rent = stats[5][0].text
                else:
                    Avg_asking_rent = ""
                if len(stats) > 6:
                    Avg_rental_listing_age = stats[6][0].text
                else:
                    Avg_rental_listing_age =""
            else:
                resident_for_sale = ''
                Avg_asking_price = ''
                Avg_sale_listing_age = ''
                resident_for_rent = ''
                Avg_asking_rent = ""
                Avg_rental_listing_age =""

        list_result.append({
            'MAIN NAME' : main_name,
            "Office name": office_name,
            'office Address': office_address,
            'office Telephone': office_telephone,
            'Resident for sale': resident_for_sale,
            'Avg. asking price': Avg_asking_price,
            'Avg. sale listing age': Avg_sale_listing_age,
            'Resident for rent': resident_for_rent,
            'Avg asking rent': Avg_asking_rent,
            'Avg rental listing age': Avg_rental_listing_age
        })
        count+=1
        print(count)
    except:
        print('failed' , main_name, url)
        print(sys.exc_info())



load_category()