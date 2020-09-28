## weekend project : 1/12

![](https://i.imgur.com/UyaO2r6.png)

#### Dinh Nguyen & Thai Pham

### A.What's the workflow?
**Getting information of 1 product on a webpage. (Tittle, price, ID, url, url img…)**


![](https://i.imgur.com/1aOrSHZ.png)


- **How do we do it?**
=> Using web scraping function, crawling data.
- **Project Purpose**
=> Getting data to analyze.
- **Project Requirement**
=> Infomation of product from catalogue in tiki.vn
- **Which tools need for this project?**
=>   Python, VS Code, Jupyter Notebook, Conda Env


## Problem solve : 

1. How to get infomation of one product => using BS4, dict, pandas
2. How to append them to 1 df => using Dictionary to loop and save the "Value" of it into "Key".
3. Then, find a way to loop all the products on that single page.
4. Collect (append) them to 1 DataFrame (of a single page)
5. What if products from other catagories had different shape of info? => using **"try"** and **"except"** to loop through them.
6. Find a way to automatically loop to all the pages.
7. How many **pages** of products if you dont care and lazy to figure out? => using a **function** to check the final page first.
8. Anything else? Yup, dont forget using **sleep()** for disblock access from TIKI.VN


## Explain:
Look at one product in one single page:

![](https://i.imgur.com/E3dkiWW.png)

The elements that we need is already here ('class':'product-item')

![](https://i.imgur.com/cpO1Ax8.png)

So, with *n* pages, we need to find out how many pages?

![](https://i.imgur.com/C70lSAC.png)

Using a function to check, with the end depend on number of items there (len(product)): 

![](https://i.imgur.com/b8Avge4.png)

Then we need to used both function to check and crawling:

![](https://i.imgur.com/erzJBTd.png)

And save them into a CSV file has name of product.

![](https://i.imgur.com/EH7o9ju.png)

Printout the dataFrame, we got this.

![](https://i.imgur.com/EXxiaXZ.png)




## Example & Note: 

#### 1. Different products has different values and structure & elements.
**BOOKS vs Electrics Devices:**
![](https://i.imgur.com/KslAjei.png)

![](https://i.imgur.com/SrxhZ9W.png)

**So, writing a function to looping through all of product we need to use Try and Except for more optional**

![](https://i.imgur.com/MrSVPUQ.png)

#### 2. Using #sleep for more "HUMAN".

![](https://i.imgur.com/sa6c1vK.png)




