from bs4 import BeautifulSoup
import requests
header = {
    "user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36",
    'referer': 'https://www.google.com/'
}

page = requests.get("https://www.autoscout24.com/lst/mitsubishi/lancer/ve_evo")
soup = BeautifulSoup(page.content, 'html.parser')
prices = soup.findAll('p', attrs={"class":"Price_price__WZayw"})
names = soup.findAll('span', attrs={"class":"ListItem_version__jNjur"})

pricesList = []
namesList = []
pages = 0
total_pages = soup.findAll("li",{"class":"pagination-item"})
for data in total_pages:
    pages += 1

for price in prices:
    pricesList.append(price.get_text())

for name in names:
    namesList.append(name.get_text())
for i in range(len(namesList)):
    print("MODEL: ", namesList[i], " PRICE: ", pricesList[i])
