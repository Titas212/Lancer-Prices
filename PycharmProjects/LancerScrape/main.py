from bs4 import BeautifulSoup
import requests


class Scrape:
    def __init__(self, url):
        self.url = url
        self.page = requests.get(url)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')
        self.prices_list = []
        self.names_list = []
        self.pages = 0
        self.file = open("prices.txt", "a")

    def find_pages(self):
        total_pages = self.soup.findAll("li", {"class": "pagination-item"})
        for _ in total_pages:
            self.pages += 1

    def find_prices_names(self):
        for i in range(self.pages):
            url = "https://www.autoscout24.com/lst/mitsubishi/lancer/ve_evo?atype=C&page=" + str(i + 1)
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            prices = soup.findAll('p', attrs={"class": "Price_price__WZayw"})
            names = soup.findAll('span', attrs={"class": "ListItem_version__jNjur"})
            for price in prices:
                self.prices_list.append(price.get_text())

            for name in names:
                self.names_list.append(name.get_text())

    def write_to_file(self):
        for (name, price) in zip(self.names_list, self.prices_list):
            self.file.write(f"MODEL NAME: {name}\n")
            self.file.write(f"MODEL PRICE: {price}\n")
            self.file.write("\n")


scraper = Scrape("https://www.autoscout24.com/lst/mitsubishi/lancer/ve_evo?atype=C&page=1")
scraper.find_pages()
scraper.find_prices_names()

scraper.write_to_file()
