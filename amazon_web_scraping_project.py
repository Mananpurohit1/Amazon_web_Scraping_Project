#!/usr/bin/env python
# coding: utf-8

# In[28]:


#importing all the libraries

from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np


# # Scraping Data from Amazon  to   .CSV

# In[29]:


#adding the url for extraction

URL = "https://www.amazon.in/s?k=playstation+5&crid=1SMY8BDWG68QX&sprefix=playstation+%2Caps%2C279&ref=nb_sb_ss_ts-doa-p_1_12"


# In[30]:


#adding the User-agent

HEADERS = ({"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36", "Accept-Language": "en-US, en;q=0.5"})


# In[31]:


#http request for connecting to the  website

webpage = requests.get(URL, headers=HEADERS)


# In[32]:


webpage


# In[33]:


type(webpage.content)


# In[18]:


#converting the data into readable html format.

soup = BeautifulSoup(webpage.content, "html.parser")


# In[19]:


soup


# In[20]:


#fetch links in list of tag objects 

links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})


#store the link
links_list=[]



#loop for extracting product details from each link 
for link in links:
    links_list.append(link.get('href'))


# # Creating functions for extraction

# In[21]:


#Functions to extract product Title 
def get_title(soup):
    
    try: 
        #outer tag object 
        title = soup.find("span", attrs={"id":"productTitle"})
        
        #inner navigatableString Object
        title_value=title.text
        
        #title as a string value
        title_string = title_value.strip()
        
    except AttributeError:
        title_string=""
        
    return title_string    


# Function to extract Product Price
def get_price(soup):

    
    try:
        price = soup.find("span", attrs={'id':'priceblock_ourprice'}).string.strip()

    except AttributeError:

        try:
            # If there is some deal price
            price = soup.find("span", attrs={'id':'priceblock_dealprice'}).string.strip()

        except:
            price = ""

    return price


# Function to extract Product Rating
def get_rating(soup):

    try:
        rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
    
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""	

    return rating



# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""	

    return review_count


# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id':'availability'})
        available = available.find("span").string.strip()

    except AttributeError:
        available = "Not Available"	

    return available


# # Appending values to the dictionary

# In[22]:


d={"Title":[], "Price":[], "Rating":[], "Reviews":[], "Availability":[]}

#loop for extracting product information from the links 
for link in links_list:
    new_webpage = requests.get("https://www.amazon.in" + link , headers=HEADERS)
    
    new_soup = BeautifulSoup(new_webpage.content, "html.parser")
    
    #function calls to display all necessary product information
    d['Title'].append(get_title(new_soup))
    d['Price'].append(get_price(new_soup))
    d['Rating'].append(get_rating(new_soup))
    d['Reviews'].append(get_review_count(new_soup))
    d['Availability'].append(get_availability(new_soup))
    


# In[23]:


amazon_df = pd.DataFrame.from_dict(d)
amazon_df['Title'].replace('', np.nan, inplace=True)
amazon_df = amazon_df.dropna(subset=['Title'])


# In[24]:


amazon_df


# In[ ]:




