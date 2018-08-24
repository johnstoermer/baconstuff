import math
import requests
from bs4 import BeautifulSoup
import re

class baconscraper:

    dict = {'Actors':{}, 'Movies':{}}

    def __init__(self):
        self._generateDict()

    def _generateDict(self):
        for i in range(1,9):
            self._addActor(i)
            self._addMovie(i)

    def _addActor(self, actor_id):
        movies = []
        url = 'https://www.imdb.com/name/nm'
        #adding the actor_id to url
        zeroes = 6 - math.floor(math.log10(actor_id)) #finding the number of zeroes in the actor_id
        for i in range(0, zeroes):
            url += '0'
        url += str(actor_id) + '/'
        #
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        name = soup.find('span', class_='itemprop').get_text()
        movie1 = soup.find('div', class_='filmo-category-section')
        movie2 = movie1.findAll('b')
        for movie in movie2:
            movie3 = movie.find('a')
            if movie3.get_text() not in movies:
                movies.append(movie3.get_text())
        if name not in self.dict['Actors']:
            self.dict['Actors'][name] = {}
            self.dict['Actors'][name]['Movies'] = movies

    def _addMovie(self, movie_id):
        genres = []
        url = 'https://www.imdb.com/title/tt'
        #adding the movie_id to url
        zeroes = 6 - math.floor(math.log10(movie_id)) #finding the number of zeroes in the movie_id
        for i in range(0, zeroes):
            url += '0'
        url += str(movie_id) + '/'
        #
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        name1 = soup.find('div', class_='title_wrapper')
        name = name1.find('h1').get_text().replace('\xa0', '')
        date = name
        name = name[:-7]
        date = date[-6:-2]
        rating1 = soup.find('div', class_='ratingValue')
        rating2 = rating1.find('strong')
        rating = rating2.find('span').get_text()
        reviews1 = soup.find('div', class_='imdbRating')
        reviews2 = reviews1.find('a')
        reviews = reviews2.find('span').get_text().replace(',', '')
        genres1 = soup.findAll('div', class_='see-more inline canwrap')
        for genres2 in genres1:
            genres3 = genres2.find('h4')
            if genres3.get_text() == 'Genres:':
                genres4 = genres2.findAll('a')
                for genres5 in genres4:
                    genres.append(genres5.get_text()[1:])
        if name not in self.dict['Movies']:
            self.dict['Movies'][name] = {}
            self.dict['Movies'][name]['Rating'] = float(rating)
            self.dict['Movies'][name]['Reviews'] = int(reviews)
            self.dict['Movies'][name]['Genres'] = genres
            self.dict['Movies'][name]['Date'] = int(date)

def main():
    b = baconscraper()
    print(b.dict)

main()
