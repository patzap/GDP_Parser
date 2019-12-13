#!/usr/bin/python3

#parses the gdp nominal values from statisticstimes.com
#by PatZap 

"""
my attempt to construct two graphs using beautiful soup to parse the Result and Matplotlib to graph it. I made two functions
of gdp_share are ppp to split the Results Sets so I can carefully organize each plot points for the two graphs 

"""

import requests, bs4
import pandas as pd
import matplotlib.pyplot as plt

def parse_data():
    res = requests.get('http://statisticstimes.com/economy/countries-by-projected-gdp.php')
    src = res.content
    soup = bs4.BeautifulSoup(src, 'lxml')    
    table = soup.find('tbody')  
    rows = table.find_all('tr') 
    return rows
    
def gdp_nominal():
    results = [] #put all data within the results lists
    for row in parse_data():
        country = row.find('td', class_ = 'name').text
        gdp_nominal = row.find('td', class_ = 'data1').text
        results.append([country, gdp_nominal])
    return results

def gdp_ppp():
    results = []
    for row in parse_data():
        country = row.find('td', class_ = 'name').text
        gdp_share = row.find_all('td', class_ = 'data')[3].text.strip() #indicate the row being parsed is the of the 3rd index. 
        results.append([country, gdp_share])
    return results
  
data1 = pd.DataFrame(gdp_nominal(), columns = ['COUNTRY', 'SHARE NOMINAL'])
data1['SHARE NOMINAL'] = data1['SHARE NOMINAL'].str.replace(',', '').astype(float) #remove the commas from the string numbers and convert it into a float
print(data1.dtypes)
data1 = data1.sort_values('SHARE NOMINAL', ascending = False).head(10) #sort top 20 values by share.

#repeated the same thing as with GDP PPP dataframe
data2 = pd.DataFrame(gdp_ppp(), columns = ['COUNTRY', 'GDP PPP'])
data2['GDP PPP'] = data2['GDP PPP'].str.replace('-', '0')
data2['GDP PPP'] = data2['GDP PPP'].str.replace(',', '').astype(float)
data2 = data2.sort_values('GDP PPP', ascending = False).head(10) 
print(data2.dtypes)

#converts dataset into a graph 
data1.plot(x ='COUNTRY', y='SHARE NOMINAL', kind = 'bar')
data2.plot(x ='COUNTRY', y='GDP PPP', kind = 'bar')
plt.show() 

data1.to_csv('SHARE_GDP.xlsx', sheet_name = 'DATA', index = False) #converts data into a csv file.
data2.to_csv('PPP.xlsx', sheet_name = 'DATA1', index = False) 


