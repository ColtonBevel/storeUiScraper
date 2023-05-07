if __name__ == '__main__':
    exit()
else:
    import requests, json
    import threading
    from datetime import date
    from bs4 import BeautifulSoup
    class Amazon:
        def __init__(self, link=str()):
            self.link = link
            self.headers = {
                'Cookie': '', #removed
                'User-Agent': '', #removed
                'Accept-Encoding': '' #removed
            }
            if self.link:
                resp = requests.get(self.link, headers=self.headers)
                self.soup = BeautifulSoup(resp.content, 'html.parser')
                print(self.soup)
            

        def getPrice(self):
            if self.link:
                return self.soup.select_one('span.a-price-whole').text + self.soup.select_one('span.a-price-fraction').text
            else:
                raise Exception('Error: no link in Amazon object')
        
        def _getPrice(self):
            resp = requests.get(self.link, headers=self.headers)
            self.soup = BeautifulSoup(resp.content, 'html.parser')
            return self.soup.select_one('span.a-price-whole').text + self.soup.select_one('span.a-price-fraction').text

        def getName(self):
            if self.link:
                return self.soup.select_one('span#productTitle').text.strip()
            else:
                raise Exception('Error: no link in Amazon object')


        
        def addItem(self):
            with open('json\items.json', 'a+'): 
                pass
            with open('json\items.json', 'r') as jfile:
                begJ = json.load(jfile)


            today = str(date.today())
            price = self.getPrice()
            name = self.getName()
            link = self.link

            if today in begJ:
                begJ[today][name] = {
                    "price": price,
                    "link": link
                }
            else:
                begJ[today] = {
                    name: {
                        "price": price,
                        "link": link
                    }
                }

            with open('json\items.json', 'w') as jfile:
                json.dump(begJ, jfile, indent=4)
        
        def updateLinks(self):
            with open('json\items.json', 'r') as j:
                itemsList = dict(json.load(j))

            updatedLinks = list()
            for dates in itemsList.values():
                for items in dates.values():
                    link = items['link']
                    if link not in updatedLinks:
                        updatedLinks.append(link)
            
            with open('json\links.json', 'w') as linkFile:
                json.dump(updatedLinks, linkFile)

        def updateCurrentItems(self):
            def _():
                self.updateLinks()
            
                with open('json\links.json') as j:
                    linkList = json.load(j)
                
                for link in linkList:
                    self.link = link
                    self.addItem()

            tList = list()
            for i in range(2):
                t = threading.Thread(target=_)
                tList.append(t)
            
            for t in tList:
                t.start()
            
            for t in tList:
                t.join()

        def getPriceByDate(self, date=date.today):
            if not self.link:
                raise Exception('Error: no link in Amazon object')
                exit()

            with open('json\items.json', 'r') as j:
                itemsList = json.load(j)

            dates = [str(dates) for dates in itemsList] 
            
            if date not in dates:
                print(f'The date you have selected is not in the database\nAvalible dates: {dates}')
                exit()
            
            for item in itemsList[date].values():
                if item['link'] == self.link:
                    print(item)
                    print(item['price'])
                    break
                else:
                    continue