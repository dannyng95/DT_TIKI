import pandas as pd
import requests
import random
import time
from time import sleep
from bs4 import BeautifulSoup
from random import randint
def Check_number_of_pages(link,n):
    # Parse HTML text
    for x in range(1,n):
        r = requests.get(f"{link}&page={x}")
        soup = BeautifulSoup(r.text, 'html.parser')
        products_check = soup.find_all('div',{'class':'product-item'})
        items = len(products_check)
        y = x
        if items == 0:
            pages = y-1
            print(f'{pages} is the final pages of this product')
            return pages 
        else:
            print(f'{y-1} is not the final pages of this product')
    return pages

    
def crawling_product(url1,number_of_pages,pdn):
    """Scrape the page of product you want to
      Input: url to the webpage. Default: https://tiki.vn/may-anh/c1801?src=c.1801.hamburger_menu_fly_out_banner
      Output: A list containing scraped data of all product & price
    """
    # Get parsed HTML
    dataall = []   
    x = 1
    while x <= number_of_pages:
        url=f"{url1}&page={x}"
        r = requests.get(url)
        # Parse HTML text
        soup = BeautifulSoup(r.text, 'html.parser')  
        # Find all products in the page
        products = soup.find_all('div',{'class':'product-item'}) 
        x += 1
        data = []
        # List containing data of all products 
        for product in products: 
            d = {'Product-id':'','Seller-id':'','Product-SKU':'','Product-Title':'','Product-Brand':'',
                 'URL':'','img_URL':'','Regular-Price':'','Final-Price':'','TIKI-NOW':'','Installment':'',
                 'Page':'','Location':''}
            #other optional : ,'Rating':''
            try:
                d['Product-id'] = product.a['data-id']
                d['Product-SKU'] = product['product-sku']
                d['Seller-id'] = product['data-seller-product-id']
                d['Product-Title'] = product.a['title']
                d['Product-Brand'] = product['data-brand']
                d['URL'] = (f"https://tiki.vn/{product.a['href']}")
                d['img_URL'] = product.a.div.span.img['src']
                Finalprice = product.find('span',{'class':'final-price'})
                d['Final-Price'] = Finalprice.text.strip(" \n, ...")
                d['Location'] = products.index(product)
                d['Page'] = x-1
                #Let's Check for somethings deeper
                try: 
                    #Some products doesn't have regular price
                    Regularprice = product.find('span',{'class':'price-regular'})
                    d['Regular-Price'] = Regularprice.text
                    #Or somethings like Installment
                    Installment = product.find('span',{'class':'installment-price-v2'})
                    d['Installment'] = Installment.text
                    #rating is somes of optional
                    # Rating = product.find('span',{'class':'rating-content'})
                    # d['Rating'] = Rating.text.strip("width:")
                    #TIKI-NOW - aka Unique Value of TIKI
                    tikinow = product.find('div',{'class':'badge-service'})
                    badge_check = tikinow.div.img['src']
                    if str(badge_check) == "https://salt.tikicdn.com/ts/upload/9f/32/dd/8a8d39d4453399569dfb3e80fe01de75.png":
                        d['TIKI-NOW'] = "YES"
                except:
                    d['Regular-Price'] = d['Final-Price']
                    d['Installment'] = None
                    d['TIKI-NOW'] = "NO"
                    # d['Rating'] = None
                #Then we appending all the Data from this page:       
                data.append(d)   
            #If missing some info let's the syntax warning back.
            except:
                print("We got one product missing somes info!")
        #Then let's bring all data of products from one page to extend one data name "dataall"   
        dataall.extend(data)
        #Use pandas to DF the dataall, with colums keys is"dataall[0]""     
        full_products = pd.DataFrame(data = dataall, columns = dataall[0].keys())
        #Then convert it to CSV for saving & visualization and name it by "pdn" = product-name
        full_products.to_csv(f'./Full_Products_{pdn}.csv', index=False)
#     sleeptime = random.randint(2,3)
#     sleep(sleeptime)  
           
    return full_products


link ='https://tiki.vn/linh-kien-may-tinh-phu-kien-may-tinh/c8129/asus?src=c.8095.hamburger_menu_fly_out_bannerr'
crawling_product(link, Check_number_of_pages(link,60), 'lkmt')