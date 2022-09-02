import dateutil.utils
from bs4 import BeautifulSoup
import requests
import os.path
import filecmp


class Scrape:
    def __init__(self, url):
        self.data_path = "/home/titas01/Lancer-Prices/PycharmProjects/LancerScrape/data"
        self.dir_list = os.listdir(self.data_path)
        self.completeName = os.path.join(self.data_path, str(dateutil.utils.today()) + ".txt")
        self.url = url
        self.page = requests.get(url)
        self.soup = BeautifulSoup(self.page.content, 'html.parser')
        self.prices_list = []
        self.names_list = []
        self.pages = 0
        self.file = open(self.completeName, "a")

    def clean_dir(self):
        for i in range(len(self.dir_list)-1):
            f1 = os.path.join(self.data_path, self.dir_list[i])
            for j in range(len(self.dir_list)-1):
                f2 = os.path.join(self.data_path, self.dir_list[j])
                if filecmp.cmp(f1, f2) and i != j:
                    os.remove(f2)
                    self.dir_list.remove(self.dir_list[j])

    def close_file(self):
        self.file.close()

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


class Calculations:

    def __init__(self, names, prices):
        self.names = names
        self.prices = prices
        self.num_prices = None

    def price_to_number(self):
        num_prices = []
        for price in self.prices:
            price_parsed = price.replace(",", "")
            num_prices.append(float("".join(filter(str.isdigit, price_parsed))))
        self.num_prices = num_prices

    def average_price(self):
        return sum(self.num_prices) / len(self.num_prices)

    def most_expensive(self):
        return max(self.num_prices)

    def cheapest(self):
        return min(self.num_prices)

scraper = Scrape("https://www.autoscout24.com/lst/mitsubishi/lancer/ve_evo?atype=C&page=1")
scraper.find_pages()
scraper.find_prices_names()
calc = Calculations(scraper.names_list, scraper.prices_list)
calc.price_to_number()
print(calc.average_price())
print(calc.most_expensive())
print(calc.cheapest())
