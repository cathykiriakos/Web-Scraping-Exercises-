#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests as req


# In[2]:


res = req.get('https://www.denvergov.org/content/denvergov/en/city-of-denver-home/news.html')


# In[3]:


res.content


# Specify html parser to use, then import beautiful soup to clean up the content, 

# In[4]:


get_ipython().run_line_magic('pinfo', 'bs')


# In[5]:


from bs4 import BeautifulSoup as bs
soup = bs(res.content, 'lxml')


# Now by utilizing beautiful soup, we have a clean version of our soup call as compared to the output of line 8

# In[6]:


soup


# Now we will move on to using the soup variable to obtain data from the website...  Navigating back to the Denver News website, we can right click on any of the links and click inspect.  This will allow us to view the html tags and code for the news articles.  Specifically we are looking for the date along with the associate title. Xpaths can be brittle and change frequently; so for this exercise we will be looking for <div class "Denver-list-item"> 
# 
# This is accomplished by utilizing the soup object, div being our first argument, and our second argument being a dictionary telling the class to be denver news list item
# 

# In[7]:


divs = soup.find_all('div', {'class': 'denver-news-list-item'})


# In[8]:


divs[0]


# Getting the numeber of articles on this page: 

# In[9]:


len(divs)


# We can see that these are beautiful soup tag objects, as shown below 

# In[10]:


type(divs[0])


# With this we can view the text inside of it

# In[11]:


divs[0].text


# We can get certain components as shown below: 

# In[13]:


divs[0].get('href')


# Looking at the element below we can see the date is noted in the second paragrahp tag with a class showing us dates.   A clean layout which is not typical of most websites 

# In[14]:


divs[0]


# In[15]:


divs[0].find('p', {'class': 'denver-news-list-date'})


# In[16]:


import pandas as pd


# In[17]:


pd.to_datetime(divs[0].find('p', {'class': 'denver-news-list-date'}).text)


# In[18]:


BASE_URL = 'https://www.denvergov.org'


# In[19]:


divs[0].find('a')


# In[20]:


divs[0].find('a').text #giving us the title 


# In[21]:


divs[0].find('a').get('href')


# In[22]:


BASE_URL + divs[0].find('a').get('href')


# Now we have all the different elements of the web page, so now we just need to loop through each of the divs 

# In[23]:


for d in divs:
    #get date 
    date = pd.to_datetime(d.find('p', {'class': 'denver-news-list-date'}).text)
    #get link
    link = d.find('a')
    #get href component 
    href = BASE_URL + link.get('href')
    #get title 
    title = link.text


# In[24]:


title


# In[25]:


date


# In[26]:


href


# The next thing to address is the number of pages, the url will change with the page number. So what we want to do is loop through all the pages, and this is accomplished by utilizing the curly brackets to incorporate all pages as shown below.  The call will fill in the curly brackets.  Format(2) identifies the page that we want.  Below we get a nice view of the url pattern. 

# In[27]:


for i in range(1,10):
    print('https://www.denvergov.org/content/denvergov/en/city-of-denver-home/news.html?page={}'.format(2))


# The last step is to find the last page, you can refernce the results x of x number.  We can accomplish this by setting the page in the url to a large one, 100 works for this example.  In my results p 29 was the last one. So we can rerun the loop with the updated parameters: 

# In[106]:


list(range(1,29)) #note it only goes from 1:28


# In[107]:


#to get to page 29 set range from 1:30, giving us all pages from the website
for i in range(1,30):
    print('https://www.denvergov.org/content/denvergov/en/city-of-denver-home/news.html?page={}'.format(i))


# Now we can combine all the elements into one consise loop as shown below: 

# In[108]:


for i in range(1,30):
    url = ('https://www.denvergov.org/content/denvergov/en/city-of-denver-home/news.html?page={}'.format(i))
    res = req.get(url)


# In[109]:


from pymongo import MongoClient
from tqdm import tqdm_notebook #getting a status bar

PAGE_URL = 'https://www.denvergov.org/content/denvergov/en/city-of-denver-home/news.html?page={}'

#Store in MongoDB
client = MongoClient()
#create db 
db = client['news']
#set up collection
coll = db['denver']

for page in tqdm_notebook(range(1,30)):
    if page==3:
        break
    url = PAGE_URL.format(page)
    res = req.get(url)
    soup = bs(res.content)
    divs = soup.find_all('div', {'class': 'denver-news-list-item'})
    
    for d in divs: 
        date = pd.to_datetime(d.find('p', {'class': 'denver-news-list-date'}).text)
        link = d.find('a')
        href = BASE_URL + link.get('href')
        title = link.text
        
        #giving keys and values using dictionary
        coll.insert_one({'date': date,
                        'link': href,
                        'title': title})
        
#Close connection MogoDb
client.close()


# In[110]:


from pymongo import MongoClient
from tqdm import tqdm_notebook #getting a status bar

PAGE_URL = 'https://www.denvergov.org/content/denvergov/en/city-of-denver-home/news.html?page={}'

#Store in MongoDB
client = MongoClient()
#create db 
db = client['news']
#set up collection
coll = db['denver']

for page in tqdm_notebook(range(1,30)):
    #if page==3:
      #  break
    url = PAGE_URL.format(page)
    res = req.get(url)
    soup = bs(res.content)
    divs = soup.find_all('div', {'class': 'denver-news-list-item'})
    
    for d in divs: 
        date = pd.to_datetime(d.find('p', {'class': 'denver-news-list-date'}).text)
        link = d.find('a')
        href = BASE_URL + link.get('href')
        title = link.text
        
        #giving keys and values using dictionary
        coll.insert_one({'date': date,
                        'link': href,
                        'title': title})
        
#Close connection MogoDb
client.close()


# In[111]:


from pprint import pprint 

client = MongoClient()
db = client['news']
coll = db['denver']

pprint(coll.find_one())


# For my web scraping deliverable I decided that I would scrape the colorado news at https://www.colorado.gov/news

# In[28]:


res2 = req.get('https://www.colorado.gov/news')


# In[29]:


res2.content


# In[30]:


get_ipython().run_line_magic('pinfo', 'bs')
from bs4 import BeautifulSoup as bs
soup2 = bs(res2.content)


# In[31]:


soup2


# Navigating back to the webpage we're looking for the div class tags for each article as shown below: 

# In[32]:


divs2 = soup2.find_all('div', {'class': 'view-page-item'})


# In[33]:


divs2[0]


# In[34]:


#Number of articles 
len(divs2)


# In[35]:


divs2[0].text


# In[36]:


import pandas as pd
divs2[0].find('span', {'class': 'date-display-single'}).text


# In[37]:


pd.to_datetime(divs2[0].find('span', {'class': 'date-display-single'}).text)


# In[38]:


BASE_URL2 = 'https://www.colorado.gov/news'


# In[39]:


divs2[0].find('a').text #title


# In[40]:


divs2[0].find('a').get('href')


# In[41]:


divs2[0].find('div', {'class': 'smaller-text-views'}).text.strip()


# In[42]:


BASE_URL2 + divs2[0].find('a').get('href')


# Now we have all the elements, so we will just need to loop through as shown below: 

# In[128]:


for d in divs2: 
    link = d.find('a')
    date = pd.to_datetime(divs2[0].find('span', {'class': 'date-display-single'}).text)
    href = BASE_URL2 + link.get('href') 
    title = link.text


# In[43]:


title


# In[44]:


link


# In[45]:


date


# In[46]:


href


# In[47]:


link


# In[135]:


for i in range(1,71): #70 is the last page with data within the colorado news website :
    print('https://www.colorado.gov/news?page={}'.format(i))


# In[ ]:


for i in range(1,71):
    url2 = ('https://www.colorado.gov/news?page?page={}'.format(i))
    res2 = req.get(url)


# In[50]:


import pandas as pd
from tqdm import tqdm_notebook
from pymongo import MongoClient

PAGE_URL2 = 'https://www.colorado.gov/news?page?page={}'

client = MongoClient()
db = client['news2']
coll = db['Colorado']

for page in tqdm_notebook(range(0, 71)):
#     for testing, we can stop it after a few iterations
#     if page == 3:
#         break      
    res2 = req.get(PAGE_URL2.format(page))
    soup2 = bs(res2.content, 'lxml')
    divs2 = soup2.find_all('div', {'class': 'views-row'})
    for d in divs2:
        date = pd.to_datetime(d.find('span', {'class': 'date-display-single'}).text)
        link = divs2[0].find('a')
        title = link.text
        href = link.get('href')
        subtitle = d.find('div', {'class': 'smaller-text-views'}).text.strip()
        
        coll.insert_one({'date': date,
                         'title': title,
                         'link': href,
                         'subtitle': subtitle})

client.close()


# In[51]:


from pprint import pprint 

client = MongoClient()
db = client['news2']
coll = db['Colorado']

pprint(coll.find_one())

