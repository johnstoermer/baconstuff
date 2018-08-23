import math
import requests
from bs4 import BeautifulSoup

class baconscraper:

    dict = {}

    def __init__(self):
        self._generateDict()

    def _generateDict(self):
        for i in range(1,9):
            self._addActor(i)

    def _addActor(self, actor_id):
        name = ''
        movies = []
        url = 'https://www.imdb.com/name/nm'
        #adding the actor_id to url
        zeroes = 6 - math.floor(math.log10(actor_id)) #finding the number of zeroes in the actor_id
        for i in range(0, zeroes):
            url += '0'
        url += str(actor_id) + '/'
        print(url)
        #
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        name = soup.find('span', class_='itemprop').get_text()
        movie1 = soup.find('div', class_='filmo-category-section')
        movie2 = movie1.findAll('b')
        for movie in movie2:
            movie3 = movie.find('a')
            movies.append(movie3.get_text())
        self.dict[name] = {}
        self.dict[name]['Movies'] = movies

def main():
    b = baconscraper()
    print(b.dict)

main()
