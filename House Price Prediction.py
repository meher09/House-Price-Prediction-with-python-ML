#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os 
os.chdir(r'F:\Batch 02\Data Wrangelling')


# In[2]:


import pandas as pd


# In[3]:


df1 = pd.read_csv('house-price.csv')
df1.head()


# In[4]:


df1.shape


# In[5]:


df1.columns


# In[6]:


df1.area_type.unique()


# In[7]:


df1['society'].unique()


# In[8]:


df1.area_type.value_counts()


# In[9]:


df1.location.value_counts()


# In[10]:


df2 = df1.drop(['area_type','availability', 'society','balcony'], axis = 'columns')


# In[11]:


df2.shape


# In[12]:


df2.head()


# ### Handle Null Values

# In[13]:


df2.isnull().sum()


# In[14]:


df3 = df2.dropna()
df3.shape


# In[15]:


df3.isnull().sum()


# ## Featured Engineering

# In[16]:


x = '4 bhk'
int(x.split()[0])


# In[17]:


def extract_number(x):
    return int(x.split()[0])


# In[18]:


# df3['bhk'] = df3.size.apply(extract_number)


# In[19]:


df3['bhk'] = df3['size'].apply(lambda x:int(x.split()[0]) )


# In[20]:


df3.head()


# In[21]:


df3.bhk.unique()


# In[22]:


df3[df3.bhk ==19]


# In[23]:


df3.total_sqft.unique()


# In[24]:


df3.bath.unique()


# In[25]:


df3[df3.bath == 40]


# ## total_sqft Feature Engineering

# In[26]:


def is_float(x):
    try:
        float(x)
    except:
        return False
    return True


# In[27]:


is_float(10000)


# In[28]:


is_float('1000-10000')


# In[29]:


df3[~df3.total_sqft.apply(is_float)].head(10)


# In[30]:


def covert_sqfeet(x):
    tokens = x.split('-')
    if len(tokens) == 2:
        return (float(tokens[0])+float(tokens[1]))/2
    try:
        return float(x)
    except:
        return None


# In[31]:


df4 =df3.copy()
df4.total_sqft = df4.total_sqft.apply(covert_sqfeet)


# In[32]:


df4.isnull().sum()


# In[33]:


df4 = df4[df4.total_sqft.notnull()]


# In[34]:


df4.head()


# In[35]:


df4.loc[30]


# In[36]:


df4.shape


# ## Price Per Square Feet Features 

# In[37]:


df5 = df4.copy()


# In[38]:


df5['price_per_sqrft'] = df5['price']*100000 / df5['total_sqft']
df5.head()


# In[39]:


df5['price_per_sqrft'].describe()


# In[40]:


df5.to_csv('housePrice.csv', index=False)


# In[41]:


df5['location'].value_counts()


# In[43]:


df5[df5.total_sqft / df5.bhk <300].head(10)


# In[44]:


df5.shape


# In[47]:


df6 = df5[~(df5.total_sqft / df5.bhk <300)]


# In[48]:


df6.shape


# ## Dimension Removal

# In[49]:


df6.head()


# In[50]:


df6.location = df6.location.apply(lambda x: x.strip())


# In[56]:


location_state = df6.location.value_counts(ascending = False)
location_state


# In[57]:


location_state.values.sum()


# In[60]:


len(location_state)


# In[66]:


len(location_state[location_state < 10])


# In[64]:


location_stats_less_than_10 = location_state[location_state < 10]


# In[65]:


location_stats_less_than_10


# In[68]:


len(df6.location.unique())


# In[69]:


df6.location = df6.location.apply(lambda x: 'Others' if x in location_stats_less_than_10 else x)


# In[70]:


len(df6.location.unique())


# In[72]:


df6.head(20)


# In[74]:


df6[df6.bath >df6.bhk+2]


# In[76]:


df7 = df6[df6.bath < df6.bhk+2]
df7.shape

