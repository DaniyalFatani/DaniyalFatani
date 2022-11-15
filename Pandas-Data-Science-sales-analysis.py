#!/usr/bin/env python
# coding: utf-8

# ### Import Necessary Libraries

# In[70]:


import pandas as pd
import os

# merging 12 months of sales data into a single CSV file
# In[50]:


df = pd.read_csv(R"C:\Users\DrC\OneDrive\Desktop\AAMD\Sales Analysis/Sales_April_2019.csv")

all_months_data = pd.DataFrame()

files = [file for file in os.listdir(R"C:\Users\DrC\OneDrive\Desktop\AAMD\Sales Analysis")]

for file in files:
    df = pd.read_csv(R"C:\Users\DrC\OneDrive\Desktop\AAMD\Sales Analysis/"+file)
    all_months_data = pd.concat([all_months_data, df])

all_months_data.to_csv('all_data.csv', index = False)



    
    
    


# ### Read in updated dataframe
# 

# In[54]:


all_data = pd.read_csv(R'C:\Users\DrC\OneDrive\Desktop\all_data_perman.csv')


# In[55]:


all_data.head()


# ### Clean up the Data

# ### Drop rows of NAN

# In[ ]:





# In[56]:


nan_df = all_data[all_data.isna().any(axis=1)]
nan_df.head()

all_data  = all_data.dropna(how='all')





# ### find 'Or' and delete it
# 

# In[57]:


all_data = all_data[all_data['Order Date'].str[0:2] != 'Or']
all_data.head()


# ### convert columns to the correct type

# In[58]:


all_data['Quantity Ordered']= pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each']= pd.to_numeric(all_data['Price Each'])


# In[ ]:





# ### Adding New columns for Analysis

# ### Task 2: Add month column

# In[59]:


all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = all_data['Month'].astype('int32')
all_data.head()


# ### Task 3: Add sales column
# 

# In[67]:


all_data['Sales'] = all_data['Quantity Ordered'] * all_data['Price Each']
all_data.head()


# ###  Task 4: Add a city colums

# In[85]:


#apply method
def get_city(address):
    return address.split(',')[1]
def get_state(address):
    return address.split(',')[2].split(' ')[1]
all_data['City']= all_data['Purchase Address'].apply(lambda x: get_city(x)  + '('+ get_state(x) + ')')
all_data.head()


# In[ ]:





# In[ ]:





# In[ ]:





# ### Question 1: What was the best month for sales? How much was earned that month?

# In[61]:


result = all_data.groupby('Month').sum()


# In[71]:


import matplotlib.pyplot as plt

months = range(1,13)

plt.bar(months, result['Sales'])
plt.xticks(months)
plt.ylabel('sales in USD($)')
plt.xlabel('Month number')
plt.show()


# ### Questio 2:What city had the highest number of sales
# 

# In[90]:


result = all_data.groupby('City').sum('Sales')
result


# In[95]:


import matplotlib.pyplot as plt

cities = [city for city, df in all_data.groupby('City')]

plt.bar(cities, result['Sales'])
plt.xticks(cities, rotation='vertical', size=8)
plt.ylabel('sales in USD($)')
plt.xlabel('City name')
plt.show()


# ### Question 3: What time should we display advertisement to maximize likelihood of customer's buying product?

# In[98]:


all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])


# In[101]:


all_data['Hour'] = all_data['Order Date'].dt.hour
all_data['Minute']= all_data['Order Date'].dt.minute
all_data.head()


# In[113]:


hours = [hour for hour, df in all_data.groupby('Hour')]
plt.plot(hours, all_data.groupby(['Hour']).count())
plt.xticks(hours)
plt.grid()
plt.xlabel('Hour')
plt.ylabel('Number of Sales Txn')

plt.show()

#I Think 12Hr and 19Hr are best time to advertise as the store is most populated 


# In[114]:


all_data.head()


# ### Question 4: What products are most ofte sold together

# In[124]:


df = all_data[all_data['Order ID'].duplicated(keep=False)]
df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
df=df[['Order ID', 'Grouped']].drop_duplicates()
df.head(100)


# In[142]:


#used stackflow for it

from itertools import combinations
from collections import Counter

count = Counter()

for row in df['Grouped']:
    row_list = row.split(',')
    count.update(Counter(combinations(row_list, 2)))
count.most_common(10)


# ### What Product sold the most? why do you think its sold the most? 

# In[145]:


product_group = all_data.groupby('Product')


# In[176]:


Quantity_ordered = product_group.sum()['Quantity Ordered']


# In[173]:


products = [product for product, df in product_group]


# In[183]:


plt.bar(products, Quantity_ordered)
plt.xticks(products, rotation='vertical', size=8)
plt.ylabel('Quantity Ordered')
plt.xlabel('Product')
plt.show()


# In[186]:


Prices = all_data.groupby('Product').mean('Price Each')
print(Prices)


# In[201]:


# Referenced: https://stackoverflow.com/questions/14762181/adding-a-y-axis-label-to-secondary-y-axis-in-matplotlib

prices = all_data.groupby('Product').mean()['Price Each']

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(products, Quantity_ordered, color = 'g')
ax2.plot(products, prices, 'b-')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered', color='g')
ax2.set_ylabel('Price ($)', color='b')
ax1.set_xticklabels(products, rotation='vertical', size=8)

plt.show()


# In[ ]:


#There seems like a  negative coorelation between price and quantity

