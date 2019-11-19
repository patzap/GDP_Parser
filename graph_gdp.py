#!/usr/bin/python3

#parses the gdp nominal values from statisticstimes.com
#by PatZap 

"""
my attempt to construct two graphs using beautiful soup to parse the Result and Matplotlib to graph it. I made two fucntions
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
        gdp_share = row.find('td', class_ = 'data1').text
        #share = row.find('td', class_ = 'data1').text
        #ppp = row.find_all('td', class_ = 'data1')[6].text.strip() #indicated the row being parsed is the of the 6 index.
        #results.append([country, share]) #append each looped data and convert it to text readible. 
        results.append([country, gdp_share])
    return results


def gdp_ppp():
    results = []
    for row in parse_data():
        country = row.find('td', class_ = 'name').text
        gdp_share = row.find_all('td', class_ = 'data1')[4].text.strip() #indicate the row being parsed is the of the 6 index. 
        results.append([country, gdp_share])
    return results
  
data1 = pd.DataFrame(gdp_nominal(), columns = ['COUNTRY', 'SHARE NOMINAL'])
data1['SHARE NOMINAL'] = data1['SHARE NOMINAL'].str.replace(',', '').astype(float) #remove the commas from the string numbers and convert it into a float
print(data1.dtypes)
data1 = data1.sort_values('SHARE NOMINAL', ascending = False).head(10) #sort top 20 values by share.

#repeated the same thing as with GDP SHARE dataframe

data2 = pd.DataFrame(gdp_ppp(), columns = ['COUNTRY', 'SHARE PPP'])

if data2['SHARE PPP'] is 'Venuzuela':
    data2['SHARE PPP'] = data2['SHARE PPP'].str.replace('-', '0')#.astype('Int64')
else:
    data2['SHARE PPP'].astype(int)
#data2['SHARE PPP'] = data2['SHARE PPP'],
#data2.drop('COUNTRY', axis = 1)
print(data2.dtypes)
data2 = data2.sort_values('SHARE PPP', ascending = True).head(10) 
print(data2)

#data1.to_csv('SHARE_GDP.xlsx', sheet_name = 'DATA', index = False) #converts data into a csv file.
#data2.to_csv('PPP.xlsx', sheet_name = 'DATA1', index = False) 
"""
data1.plot(x ='COUNTRY', y='SHARE NOMINAL', kind = 'bar')
data2.plot(x ='COUNTRY', y='SHARE PPP', kind = 'bar')
plt.show()
"""

