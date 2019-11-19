#!/usr/bin/python3

#example dataframe by PatZap Updated Oct 7 2019

import bs4, requests
import pandas as pd 

def wiki_parse():

    res = requests.get('https://en.wikipedia.org/wiki/List_of_Prime_Ministers_of_Canada_by_date_and_place_of_birth')
    src = res.content
    soup = bs4.BeautifulSoup(src, 'lxml')
    
    print('Parsing Data: ')

    code_ext = soup.find('div', attrs = {'id': 'content'})
    
    results = []
    table = code_ext.find('table')
    
    rows = table.find_all('tr')
    #section copied from Paul
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        results.append([ele for ele in cols if ele])

    return results


data = pd.DataFrame(wiki_parse(), columns = ['PRIME MINISTER', 'DOB', 'BIRTHPLACE', 'PROVINCE', 'IN OFFICE'])
#data.set_index('PRIME MINISTER', inplace = True)
a = data.tail(10)
final_data = a.iloc[3:10, 0:3]
#print(final_data)
final_data.to_csv('PM_DOB.xlsx', sheet_name = 'Prime Minister', index = False)










