import math
import time
import requests
from lxml import html
import re
import json

class baconscraper:

    dict = {'Actors':{}, 'Movies':{}}

    def __init__(self):
        self._generateDict()

    def _generateDict(self):
        self._addActor(1)
        self._addMovie(1)
        with open('baconator.json', 'w', encoding='utf-8') as fp:
            json.dump(self.dict, fp, ensure_ascii=False, indent=4, sort_keys=True)

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
        tree = html.fromstring(page.content)
        name = tree.xpath('//*[@id="overview-top"]/h1/span[1]/text()')[0]
        birthday = int(tree.xpath('//*[@id="name-born-info"]/time/a[2]/text()')[0])
        movies = tree.xpath('//*[starts-with(@id, "actor-tt")]/b/a/text()')
        if name not in self.dict['Actors']:
            self.dict['Actors'][name] = {}
            self.dict['Actors'][name]['Birthday'] = birthday
            self.dict['Actors'][name]['Movies'] = movies

    def _addMovie(self, movie_id):
        start = time.time()
        url = 'https://www.imdb.com/title/tt'
        #adding the movie_id to url
        zeroes = 6 - math.floor(math.log10(movie_id)) #finding the number of zeroes in the movie_id
        for i in range(0, zeroes):
            url += '0'
        url += str(movie_id) + '/'
        #
        page = requests.get(url)
        end = time.time()
        print(str(end - start))
        tree = html.fromstring(page.content)
        title = tree.xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div/div[2]/div[2]/h1/text()')[0].replace('\xa0', '')
        rating = float(tree.xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div/div[1]/div[1]/div[1]/strong/span/text()')[0])
        reviews = int(tree.xpath('//*[@id="title-overview-widget"]/div[2]/div[2]/div/div[1]/div[1]/a/span/text()')[0].replace(',', ''))
        date = int(tree.xpath('//*[@id="titleYear"]/a/text()')[0])
        count = 2
        cast = []
        while True:
            try:
                cast.append(tree.xpath('//*[@id="titleCast"]/table/tr[{}]/td[2]/a/text()'.format(count))[0][1:-2]) #calling [0] on an empty array will cause an error and break
                count += 1
            except:
                break
        count = 1
        genres = []
        while True:
            try:
                genres.append(tree.xpath('//*[@id="titleStoryLine"]/div[3]/a[{}]/text()'.format(count))[0][1:]) #calling [0] on an empty array will cause an error and break
                count += 1
            except:
                break
        if title not in self.dict['Movies']:
            self.dict['Movies'][title] = {}
            self.dict['Movies'][title]['Rating'] = rating
            self.dict['Movies'][title]['Reviews'] = reviews
            self.dict['Movies'][title]['Genres'] = genres
            self.dict['Movies'][title]['Date'] = date

def main():
    b = baconscraper()

main()
