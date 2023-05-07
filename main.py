import emailSMS, requests, time, os, math
from bs4 import BeautifulSoup

url = 'https://account.ui.com/login?shopify=true&region=us'
header = {
    "user": "", #removed
    "password": "" #removed
}

def storeUI():
    global results
    page = requests.post(url=url, headers=header)
    url2 = 'https://store.ui.com/collections/routing-switching/products/edgeswitch-16-xg?_pos=1&_sid=3a43b460d&_ss=r'
    page = requests.get(url=url2)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id='titleSoldOutBadge').text
start = time.time()

while True:
    end = time.time()
    current_time = end - start
    current_time = math.trunc(current_time)
    minutes, seconds = divmod(current_time, 60)
    time.sleep(1)
    storeUI()
    os.system('cls')
    if "Sold Out" in results:
        print(f"Sold out, trying again.\nMinutes: {minutes}\nSeconds: {seconds}")
    elif "Sold Out" not in results:
        print("In Stock, sending email.")