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
        sleep(random.randint(1,2)) 
        if items == 0:
            pages = y-1
            print(f'{pages} is the final pages of this product')
            return pages 
        else:
            print(f'{y-1} is not the final pages of this product')
    return pages

    
def crawling_product(url1,number_of_pages,pdn):
    """Scrape the page of product you want to
      Input: url to the webpage. Default: https://tiki.vn/*****/****.hamburger_menu_fly_out_banner
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
            d = {'Product-id':'','Seller-id':'','Product-SKU':'','Product-Title':'','Product-Brand':'','Author':'',
                 'URL':'','img_URL':'','Regular-Price':'','Final-Price':'','Comment':'','TIKI-NOW':'','Rating':'','Installment':'',
                 'Page':'','Location':''}
            #other optional : ,'Rating':''
            try:
                d['Product-id'] = product.a['data-id']
                d['Product-SKU'] = product['product-sku']
                d['Seller-id'] = product['data-seller-product-id']
                d['Product-Title'] = product.a['title']
                d['Product-Brand'] = product['data-brand']
                d['URL'] = (f"https://tiki.vn{product.a['href']}")
                d['img_URL'] = product.a.div.span.img['src']
                Finalprice = product.find('span',{'class':'final-price'})
                d['Final-Price'] = Finalprice.text.strip(" \n, ...")
                d['Location'] = products.index(product)
                d['Page'] = x-1
                
#Let's Check for somethings deeper
                #COMMENT
                try: 
                    Comment = product.find('p',{'class':'review'})
                    d['Comment'] = Comment.text.strip(" \n, ')' (... ")
                except:
                    print(f"No comment for {d['Product-Title']}")

                #AUTHOR for BOOKs
                try:
                    Author = product.find('p',{'class':'author'})
                    d['Author'] = Author.text
                except:
                    d['Author'] = None
                #REGULAR PRICE (sometime product has the same with final price)
                try:
                    #Some products doesn't have regular price
                    Regularprice = product.find('span',{'class':'price-regular'})
                    d['Regular-Price'] = Regularprice.text.strip(" \n, ...")
                except:
                    print(f"No Regular Price for {d['Product-Title']}")    
                    d['Regular-Price'] = d['Final-Price']
                #INSTALLMENT - For optional
                try:                          
                    #Or somethings like Installment
                    Installment = product.find('span',{'class':'installment-price-v2'})
                    d['Installment'] = Installment.text
                except:
                    print(f"No installment for {d['Product-Title']}")
                    d['Installment'] = None                

                    #RATING is somes of optionals
                try:
                    Rating = product.find('span',{'class':'rating-content'})
                    d['Rating'] = str(Rating.span['style']).strip("width:")
                except:
                    print(f"No Rating for {d['Product-Title']}")
                    d['Rating'] = None                       
                 #TIKI-NOW - aka Unique Value of TIKI
                try:                   
                    tikinow = product.find('div',{'class':'badge-service'})
                    badge_check = tikinow.div.img['src']
                    if str(badge_check) == "https://salt.tikicdn.com/ts/upload/9f/32/dd/8a8d39d4453399569dfb3e80fe01de75.png":
                        d['TIKI-NOW'] = "YES"
                except:
                    d['TIKI-NOW'] = "NO"
                    
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
        full_products.to_csv(f'./Output/Full_Products_{pdn}.csv', index=False)
        
        # Export to pickle file
        full_products.to_pickle("./TIKI_result.pkl")
        
    #visualization as Table(df) from Pandas       
    return full_products
    sleeptime = random.randint(1,2)
    sleep(sleeptime)



#FOR RUNNING EVERY CATALOGUEs:
catalogue = input(f"What's Products/Catalogues you want to crawl: ")
link = input(f"Instert the Url of the product(first page) :")
magic_number = random.randint(999,9999)
n = magic_number
crawling_product(link, Check_number_of_pages(link,n),catalogue)

#explain : https://gist.github.com/dannyng95/a88468ad92f7da3ec4db82c81ccf6adc