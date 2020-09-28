pages = np.arange(1,100)

for page in pages:
  page = requests.get("https://tiki.vn/laptop/c8095/asus?src=static_block&page="+str(page))

  soup = BeautifulSoup(page.text,"html.parser")

  # Find all div tags with class: product-item
  product_div = soup.find_all('div', {'class':'product-item'})

  # List containing data of all product info
  products = []

  # print(page)
  for div in product_div:

  # Create dictionary to store info
      d = {'Product-id':'', 'Seller-id':'','Product-title':'' ,'image_url':'', 'Product-price':'','Original-price':'',
        'Sales-percentage':''}

    # assigning product info to dictionary
      try:
        d['Product-id'] = div['data-id']
        d['Seller-id'] = div['data-seller-product-id']
        d["Product-title"] = div.a['title']
        d["image_url"] = div.a.div.span.img['src']
        d['Product-price'] = div['data-price']
        o_p = div.find('span',{'class':'price-regular'})
        s_p = div.find('span',{'class':'sale-tag sale-tag-square'})
        d['Original-price'] = o_p.text.strip('đ')
        d['Sales-percentage'] = s_p.text

        products.append(d)
      except:
        # Skip if error and print error message
        print("We got one div error!")

# pandas dataframe
product_tiki = pd.DataFrame(data = products,columns = products[0].keys())

product_tiki.to_csv('Tiki_Laptop_Asus_new.csv')

  # return product_tiki
print(product_tiki)
