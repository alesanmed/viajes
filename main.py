# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs
import urllib.request
from tools.parse_travel import parse_travel
from tools.user_agent import get_user_agent
import time
from mongodb import transactions

def run():
    URL = "http://www.exprimeviajes.com/"
    
    while True:
        req = urllib.request.Request(
                            URL,
                            data=None,
                            headers= {
                                'User-Agent': get_user_agent()
                                }
                            )
        document = urllib.request.urlopen(req)
        
        # Only for the development stage
        with open('test.txt', 'r') as file:
            document = file.read()
        
        transactions.connect()
        web = bs(document, "html.parser")
        
        last_url = transactions.get_last_to_check()
        first = True
        
        for h2 in web.findAll('h2', class_="entry-title"):
            link = h2.a['href']
            if last_url is not None and link == last_url:
                transactions.disconnect()
                time.sleep(7200)
                break

                
            title = h2.a.text.strip().split()
            price = int(title[title.index("EUROS") - 1])
            transactions.save_travel(parse_travel(link, price))
            
            if first:
                first = False
                transactions.update_last_to_check(link)
            time.sleep(3)
        
if __name__ == "__main__":
    run()